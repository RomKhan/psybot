#!/usr/bin/env python3

import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, executor, types
from src.environment import API_TOKEN
from src.statemachine import next_state_msg, process_event, session


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
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
            if state.need_recommendation and state.recommendation_message != "":
                actions.append(
                    bot.send_message(msg.chat.id, state.recommendation_message, disable_web_page_preview=True))
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
    parse_mode = types.ParseMode.MARKDOWN if re.match(r"\ACourse*", state.name) is not None \
                                             or re.match(r"\AFacts*", state.name) is not None else types.ParseMode.HTML
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await message.answer(
                text[x:x + 4096], reply_markup=state.get_buttons(), parse_mode=parse_mode)
    else:
        await message.answer(
                text, reply_markup=state.get_buttons(), parse_mode=parse_mode)

    if state.need_recommendation and state.recommendation_message != "":
        await bot.send_message(message.chat.id, state.recommendation_message, disable_web_page_preview=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
