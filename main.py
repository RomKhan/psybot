#!/usr/bin/env python3

import asyncio
import logging
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types

from src.environment import API_TOKEN
from src.statemachine import next_state_msg, process_event, session

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.errors_handler()
async def rollback_transaction(update, error):
    # todo: retry
    session.rollback()


@dp.callback_query_handler()
async def handle_inline_keyboard(query: types.CallbackQuery):
    state = process_event(query.data, query.from_user.id)
    keyboard = state.get_buttons()
    text = state.get_message()
    msg = query.message

    actions = [query.answer()]
    if isinstance(keyboard, types.InlineKeyboardMarkup) or keyboard is None:
        if msg.text != text and text:
            actions.append(msg.edit_text(text, reply_markup=keyboard))
        else:
            actions.append(msg.edit_reply_markup(keyboard))
    else:

        actions.append(bot.send_message(msg.chat.id, text, reply_markup=keyboard))
        actions.append(msg.edit_reply_markup(state.inactive_buttons()))

    await asyncio.gather(*actions)


@dp.message_handler()
async def handle_message(message: types.Message):
    state = next_state_msg(message)
    text = state.get_message()
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await message.answer(
                text[x:x + 4096], reply_markup=state.get_buttons(), parse_mode=ParseMode.HTML)
    else:
        await message.answer(
            text, reply_markup=state.get_buttons(), parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
