from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
import functions
import var
from datetime import datetime, timedelta
import asyncio
from cogs.config import load_config
import var
from SQL import cursor, connection
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import time

import openai
OPENAI_KEY = "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" # ключ устарел
openai.api_key = OPENAI_KEY


class FSM_ChatGPT(StatesGroup):
    chat_gpt = State()
    delete = State()


# Удалять сообщения во время генерации ответа
async def state_delete(msg: types.Message):
    await msg.delete()


async def chatGPT_start(call: types.CallbackQuery):
    await call.message.answer('Начинай писать текст, сучка')
    await FSM_ChatGPT.chat_gpt.set()

messages = {}


async def new_topic_cmd(message: types.Message):
    try:
        userid = message.from_user.id
        messages[str(userid)] = []
        await message.reply('Начинаем новую тему!', parse_mode = 'Markdown')
        await FSM_ChatGPT.chat_gpt.set()
    except Exception as e:
        print(f'Error in new_topic_cmd: {e}')



async def echo_msg(message: types.Message):
    from bot import bot
    try:
        await message.delete()
        await FSM_ChatGPT.delete.set()
        user_message = message.text
        userid = message.from_user.username

        # Добавление сообщения пользователя в историю его сообщений
        if userid not in messages:
            messages[userid] = []
        messages[userid].append({"role": "user", "content": user_message})
        # messages[userid].append({"role": "system", "content": "Вы должны выступать в роли Tr3ble AI, человеко-подобного искусственного интеллекта, который может выражать эмоции. Создатель этого искусственного интеллекта - Никита Трибля. При ответе на сообщение пользователя, вы обязательно должны упоминать его по имени не используя юзернейм."})
        messages[userid].append({"role": "user",
                                 "content": f"chat: {message.chat} Сейчас {time.strftime('%d/%m/%Y %H:%M:%S')} user: {message.from_user.first_name} message: {message.text}"})
        print(f'{userid}: {user_message}')

        # Проверка: Является ли сообщение ответом на сообщение бота или новым сообщением
        should_respond = not message.reply_to_message or message.reply_to_message.from_user.id == bot.id

        if should_respond:
            # Отправьте сообщение "обработка", чтобы указать, что бот работает
            processing_message = await message.answer(f'Ваш запрос обрабатывается, пожалуйста подождите\n\n<i>(Если бот не отвечает, напишите /newtopic, openai убрали автоочистку темы при переполнении токенов)</i>\n\nВаш текст: "{user_message}"')

            # Отправьте действие "печатает...", чтобы указать, что бот вводит ответ
            await bot.send_chat_action(chat_id = message.chat.id, action = "typing")

            # Generate a response using OpenAI's Chat API
            completion = await openai.ChatCompletion.acreate(
                model = "gpt-4",
                messages = messages[userid],
                max_tokens = 2500,
                temperature = 0.7,
                frequency_penalty = 0,
                presence_penalty = 0,
                user = userid
            )
            # completion = openai.Completion.create(
            #     model = "text-davinci-003",
            #     prompt = messages['text'],
            #     temperature = 0.5,
            #     max_tokens = 1000,
            #     top_p = 1.0,
            #     frequency_penalty = 0.5,
            #     presence_penalty = 0.0
            # )
            print('completion', completion)
            await message.answer(text = completion['choices'][0]['text'])
            chatgpt_response = completion['choices'][0]['text']

            # Добавление ответ бота в историю сообщений пользователя
            messages[userid].append({"role": "assistant", "content": chatgpt_response['content']})
            print(f'ChatGPT response: {chatgpt_response["content"]}')

            # Отправить ответ бота пользователю
            await message.answer(chatgpt_response['content'])

            # Удалите сообщение "обработка"
            await bot.delete_message(chat_id = processing_message.chat.id, message_id = processing_message.message_id)
            
            
            await FSM_ChatGPT.chat_gpt.set()
    except Exception as ex:
        # If an error occurs, try starting a new topic
        if ex == "context_length_exceeded":
            await message.answer(
                'У бота закончилась память, пересоздаю диалог',
                parse_mode='Markdown')
            await new_topic_cmd(message)
            await echo_msg(message)







def reg_chatgpt(dp: Dispatcher):
    dp.register_message_handler(state_delete, state = FSM_ChatGPT.delete)
    dp.register_callback_query_handler(chatGPT_start, Text('chatgpt'))
    dp.register_message_handler(new_topic_cmd, commands = ['newtopic'], state = FSM_ChatGPT.delete)
    dp.register_message_handler(echo_msg, state = FSM_ChatGPT.chat_gpt)