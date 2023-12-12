import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
import functions
from SQL import cursor, connection
from aiogram.dispatcher.filters.state import StatesGroup, State
import random
import var


cursor.execute( "DROP TABLE IF EXISTS gesway" )
cursor.execute( """CREATE TABLE IF NOT EXISTS gesway (
    id BIGINT,
    xp BIGINT,
    lvl INT
)""" )
cursor.execute("""CREATE TABLE IF NOT EXISTS gesway_action (
    id BIGINT,
    task TEXT,
    xp INT,
    date TIMESTAMP
    )""")
connection.commit()


async def gesway(call: types.CallbackQuery):
    cursor.execute(f"SELECT id FROM gesway WHERE id = {call.from_user.id}") #проверка, существует ли участник в БД
    if cursor.fetchone() == None: #Если не существует
        expStart = 100
        cursor.execute(f"INSERT INTO gesway (id, xp, lvl) VALUES ({call.from_user.id}, 0, 1)")
        cursor.execute(f"INSERT INTO gesway_action (id, task, xp, date) VALUES ({call.from_user.id}, 'Зарегестрировался в Gesway', {expStart}, NOW())")
        cursor.execute(f"UPDATE gesway SET xp = xp + {expStart} WHERE id = {call.from_user.id}") #проверка, существует ли участник в БД
        connection.commit()

        await call.message.answer('Вы успешно были зарегистрированы в Gesway!')
    else:
        await call.message.answer('Вы уже зарегистрированы в Gesway. Выбирай:')
    


# async def gesway_add(msg: types.Message):
#     cursor.execute(f"INSERT INTO gesway_action (id, datetime, action, xp) VALUES ({ctx.author.id}, CURTIME(), '{desc}', {exp})")
#     cursor.execute(f"UPDATE gesway SET xp = xp + {exp} WHERE id = {ctx.author.id}") #проверка, существует ли участник в БД
#     connection.commit()




def reg_gesway(dp: Dispatcher):
    print('[COGS] gesway - is connected')
    dp.register_callback_query_handler(gesway, Text('gesway'))
    # dp.register_message_handler(gesway_add, Text('gesway_add'))
    # dp.register_message_handler(gesway, lambda c: c.data.startswith('gesway_'))