#!/usr/bin/env python3

import logging

from aiogram import Bot, Dispatcher, executor, types

from src.environment import API_TOKEN
from src.statemachine import next_state

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    state = next_state(message)
    await message.answer(
        state.get_message(), reply_markup=state.get_buttons(), disable_web_page_preview=True
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
