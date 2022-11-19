#!/usr/bin/env python3

import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types

from src.environment import API_TOKEN
from src.statemachine import next_state, next_state_msg

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.callback_query_handler()
async def handle_inline_keyboard(query: types.CallbackQuery):
    state = next_state(query.data, query.from_user.id, datetime.now())
    keyboard = state.get_buttons()
    text = state.get_message()
    if state.inline_buttons:
        await asyncio.gather(
            query.message.edit_text(text),
            query.message.edit_reply_markup(keyboard),
            query.answer(),
        )
    else:
        await asyncio.gather(
            bot.send_message(query.message.chat.id, text, reply_markup=keyboard),
            query.message.edit_reply_markup(),
            query.answer(),
        )


@dp.message_handler()
async def handle_message(message: types.Message):
    state = next_state_msg(message)
    await message.answer(
        state.get_message(), reply_markup=state.get_buttons(), disable_web_page_preview=True
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
