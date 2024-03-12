#!/usr/bin/env python3

import asyncio
import logging
import re

# from dotenv import load_dotenv
# load_dotenv('.env')

from aiogram import Bot, Dispatcher, executor, types
from src.environment import API_TOKEN
from src.util import markdown_fix
from src.statemachine import next_state_msg, process_event, session

# multiple_messages = []

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
    parse_mode = types.ParseMode.MARKDOWN if re.match(r"\ACourse*", state.name) is not None \
                                             or re.match(r"\AFacts*", state.name) is not None else types.ParseMode.HTML
    if parse_mode == types.ParseMode.MARKDOWN:
        text = markdown_fix(text)

    if state.need_recommendation and state.recommendation_message != "":
        await bot.send_message(msg.chat.id, state.recommendation_message, disable_web_page_preview=True)
        return

    if isinstance(keyboard, types.InlineKeyboardMarkup) or keyboard is None:
        if msg.text != text and text:
            actions.append(msg.edit_text(text, reply_markup=keyboard, parse_mode=parse_mode))
        else:
            actions.append(msg.edit_reply_markup(keyboard))
        # if state.need_recommendation and state.recommendation_message != "":
        #     actions.append(
        #         bot.send_message(msg.chat.id, state.recommendation_message, disable_web_page_preview=True))
    else:
        actions.append(bot.send_message(msg.chat.id, text, reply_markup=keyboard, parse_mode=parse_mode))
        actions.append(msg.edit_reply_markup(state.inactive_buttons()))
    await asyncio.gather(*actions)


@dp.message_handler()
async def handle_message(message: types.Message):
    state = next_state_msg(message)
    text = state.get_message()
    parse_mode = types.ParseMode.MARKDOWN if re.match(r"\ACourse*", state.name) is not None \
                                             or re.match(r"\AFacts*", state.name) is not None else types.ParseMode.HTML
    text = markdown_fix(text)
    if len(text) > 4096:
        texts = text.split('\n')
        messages = []
        i = 1
        while i < len(texts):
            messages.append(texts[i-1])
            while len(messages[-1]) + len(texts[i]) <= 4096:
                messages[-1] += '\n' + texts[i]
                i += 1
                if i >= len(texts):
                    break
            messages[-1].strip()

        for i in range(len(messages)):
            await message.answer(messages[i], parse_mode=parse_mode)
        # await message.answer(messages[-1], reply_markup=state.get_buttons(), parse_mode=parse_mode)
    elif not state.need_quiz_message:
        await message.answer(
                text, reply_markup=state.get_buttons(), parse_mode=parse_mode)
    else:
        await message.answer(text, parse_mode=parse_mode)

    if state.need_quiz_message:
        await bot.send_message(message.chat.id, "Предлагаем также пройти тест, чтобы закрепить пройденный материал ",
                               reply_markup=state.get_buttons(), disable_web_page_preview=True)

    if state.need_recommendation and state.recommendation_message != "":
        await bot.send_message(message.chat.id, state.recommendation_message, disable_web_page_preview=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
