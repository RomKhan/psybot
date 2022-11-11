from aiogram.types import Message

from .database import session
from .models import ActionLog, User
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
    state = states_by_name[user.state_name]()
    name = state.next_state(message.text)

    if name in states_by_name:
        user.state_name = name
        next_state = states_by_name[name]()
        session.add(
            ActionLog(
                user_id=user.id,
                message_unix_time=user.message_unix_time,
                old_state_name=user.state_name,
                new_state_name=name,
            )
        )
    else:
        next_state = state
        state.message = "Что-то пошло нетак!"  # todo

    session.commit()
    return next_state
