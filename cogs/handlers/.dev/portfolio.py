from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram import types




ikbPortfolio = InlineKeyboardMarkup(row_width=2)
ikbPortfolio.add(InlineKeyboardButton('Подробнее про портфолио', callback_data = 'portfolio'))

@dp.message_handler(Text(['🧩 Портфолио']))
async def echo(msg: types.Message):
    await msg.answer('Портфолио', reply_markup = ikbPortfolio)