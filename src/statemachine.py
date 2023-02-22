import re
from datetime import datetime
from typing import Optional, TypeGuard

from aiogram.types import Message

from .database import session
from .models import User
from .states import BaseState, states_by_name
from .util import oops_message


def get_user(id: int, date: Optional[datetime] = None) -> User:
    timestamp = round((date or datetime.now()).timestamp())
    user: User | None = session.query(User).get(id)
    if user is not None:
        user.message_unix_time = timestamp
    else:
        user = User(id=id, message_unix_time=timestamp, state_name="Start")
        session.add(user)
    return user


def get_user_msg(message: Message) -> User:
    return get_user(message.from_id, message.date)


def is_valid_state(name: str | None) -> TypeGuard[str]:
    if not isinstance(name, str):
        return False

    return name.split("/")[0] in states_by_name


def deserialize_state(name: str, user: User, text: str):
    arr = name.split("/")
    res = states_by_name[arr[0]](user, text)
    if len(arr) > 1:
        res.set_substate(*arr[1:])
    return res


def next_state(text: str, from_id: int, date: Optional[datetime] = None):
    user = get_user(from_id, date)
    state = deserialize_state(user.state_name, user, text)
    name = state.next_state()
    if name is None:
        name = deserialize_state("Start", user, text).next_state()

    if is_valid_state(name):
        next_state = deserialize_state(name, user, text)
        next_state.inactive_buttons = state.inactive_buttons
        session.add(next_state.log())
    else:
        next_state = state
        state.message = oops_message
        session.add(next_state.log("/error"))

    user.state_name = next_state.name
    session.commit()
    return next_state


def next_state_msg(message: Message) -> BaseState:
    return next_state(message.text, message.from_id, message.date)


def process_event(request: str, from_id: int) -> BaseState:
    m = re.match(r"^([a-z]+(?:/[a-z0-9]+)*)/([a-z]+):([0-9]+)$", request, flags=re.IGNORECASE)
    if m:
        name, action, num = m.groups()
        state = deserialize_state(name, get_user(from_id), request)
        state.action(action, int(num))
        session.add(state.log(f"/{action}"))
        session.commit()
        return state
    else:
        return next_state(request, from_id)
