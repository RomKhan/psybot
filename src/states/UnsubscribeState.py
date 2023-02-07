import asyncio
import re
from urllib.parse import urljoin

import aiohttp
from aiogram import Bot
from quizlib.environment import PAYFORM_LINK, SUBSCRIPTION_ID
from quizlib.models import Order
from quizlib.util import hmac_sign

from ..database import session
from ..models import User
from .BaseState import BaseState


class UnsubscribeState(BaseState):
    name = "Unsubscribe"

    active: bool = False
    email: str | None = None

    async def unsubscribe(self) -> None:
        data = {
            "subscription": SUBSCRIPTION_ID,
            "customer_email": self.email,
            "active_user": "0",
        }
        data["signature"] = hmac_sign(data)
        url = urljoin(PAYFORM_LINK, "/rest/setActivity/")

        cond = Order.user_id == self.user.id
        if self.user.linked_user:
            self.user.linked_user.is_subscribed = False
            cond |= Order.user_id == self.user.linked_user.id

        for order in session.query(Order).filter(cond).all():
            order.status = "unsubscribed"

        async with aiohttp.ClientSession() as httpsession:
            async with httpsession.post(url, data=data) as response:
                print("Unsubscribe Status:", response.status, flush=True)
                text = self.data["message200"]
                if response.status != 200:
                    text = self.data["message400"]
                    print("HTTP Error:", await response.text(), flush=True)
                await Bot.get_current().send_message(chat_id=self.user.id, text=text)

    def __init__(self, user: User, text: str) -> None:
        super().__init__(user, text)

        if user.linked_user:
            self.email = user.linked_user.email
        elif re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.text):
            self.email = self.text
        elif super().next_state() is None:
            self.message = self.data["message2"]

    def next_state(self) -> str | None:
        res = super().next_state()
        if res:
            return res

        if self.email:
            asyncio.ensure_future(self.unsubscribe())
            return "Start"

        return self.name
