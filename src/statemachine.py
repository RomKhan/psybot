from aiogram.types import Message

from .database import session
from .models import User
from .states import BaseState, states_by_name


def get_user(message: Message) -> User:
    id = message.from_id
    timestamp = round(message.date.timestamp())
    user: User | None = session.query(User).get(id)
    if user is not None:
        user.message_unix_time = timestamp
    else:
        user = User(id=id, message_unix_time=timestamp, state_name="Start")
        session.add(user)
    return user


def next_state(message: Message) -> BaseState:
    user = get_user(message)
    state = states_by_name[user.state_name](user, message.text)
    name = state.next_state()

    if isinstance(name, str) and name in states_by_name:
        next_state = states_by_name[name](user, message.text)
        session.add(next_state.log())
    else:
        next_state = state
        state.message = "Что-то пошло нетак!"  # todo
        session.add(next_state.log("/error"))

    user.state_name = next_state.name
    session.commit()
    return next_state
