from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from aiogram.dispatcher.filters import Text





ikbWork = InlineKeyboardMarkup(row_width=2)
ikbWork.add(InlineKeyboardButton('Подробнее про услуги', callback_data = 'work'))

@dp.message_handler(Text(['✨ Услуги']))
async def echo(msg: types.Message):
    await msg.answer('Услуги', reply_markup = ikbWork)