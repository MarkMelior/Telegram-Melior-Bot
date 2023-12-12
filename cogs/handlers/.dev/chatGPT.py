from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types


import openai
OPENAI_KEY = "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" # ключ устарел
openai.api_key = OPENAI_KEY




async def chatGPT(call: types.CallbackQuery):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=msg.content,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        # stop=["you:"]
    )

    await msg.channel.send(response['choices'][0]['text'])


async def chatGPT(call: types.CallbackQuery):
    if msg.channel.id == kGopnik and not msg.author.bot:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "Answer like a gopnik. "},
                {"role": "user", "content": msg.content},
            ]
        )
        await msg.channel.send(response['choices'][0]['message']['content'])


def reg_chatGPT(dp: Dispatcher):
    dp.register_callback_query_handler(chatGPT, Text(['chatGPT']))