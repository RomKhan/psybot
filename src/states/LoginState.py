import re

from werkzeug.security import check_password_hash

from ..database import session
from ..models import ActionLog, AndroidUser, User
from .BaseState import BaseState


class LoginState(BaseState):
    name = "Login"

    email: str | None = None
    android_user: AndroidUser | None = None

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)

    def check_password(self, password: str) -> bool:
        user = session.query(AndroidUser).filter_by(email=self.email).one_or_none()
        if user is None:
            return False

        self.android_user = user
        return check_password_hash(user._password, password)

    def set_substate(self, *args: str) -> None:
        assert len(args) == 1
        self.email = args[0]
        self.name = f"{self.name}/{self.email}"
        self.message = self.data["message2"].replace("{{EMAIL}}", self.email)

    def log(self, next_name: str | None = None) -> ActionLog:
        res = super().log(next_name)
        res.button_text = "{{SECRET}}"  # type: ignore
        return res

    def next_state(self) -> str | None:
        res = super().next_state()
        if res:
            return res

        if self.email:
            if self.check_password(self.text):
                self.user.linked_user = self.android_user
                return "SuccessfulLogin"
            else:
                return "FailedLogin"

        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.text):
            return f"{self.name}/{self.text}"

        return None
