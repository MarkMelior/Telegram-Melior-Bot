import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
import functions
from SQL import cursor, connection
from aiogram.dispatcher.filters.state import StatesGroup, State
import random
from datetime import datetime, timedelta
import var
from var import add_cash, add_xp


cursor.execute( "DROP TABLE IF EXISTS work" )
cursor.execute( """CREATE TABLE IF NOT EXISTS work (
    work_id SERIAL PRIMARY KEY,
    name TEXT,
    income BIGINT,
    xp INT,
    cost_xp BIGINT
)""" )
cursor.execute(f"INSERT INTO work(name, income, xp, cost_xp) VALUES ('🧩 Junior', {add_cash}, {add_xp}, 0)")
cursor.execute(f"INSERT INTO work(name, income, xp, cost_xp) VALUES ('🔥 Jun-Middle', {add_cash * 1.8}, {add_xp * 2}, {add_xp * 30})")
cursor.execute(f"INSERT INTO work(name, income, xp, cost_xp) VALUES ('💥 Middle', {add_cash * 1.8 * 2}, {add_xp * 4}, {add_xp * 2 * 40})")
cursor.execute(f"INSERT INTO work(name, income, xp, cost_xp) VALUES ('😎 Mid-Senior', {add_cash * 1.8 * 4}, {add_xp * 8}, {add_xp * 4 * 50})")
cursor.execute(f"INSERT INTO work(name, income, xp, cost_xp) VALUES ('💎 Senior', {add_cash * 1.8 * 8}, {add_xp * 16}, {add_xp * 8 * 60})")
connection.commit()
 





async def game_work(call: types.CallbackQuery):

    # вызываем старый баланс пользователя
    old_balance = functions.get_balance(call)

    cursor.execute(f"SELECT * FROM work")
    result = cursor.fetchall()
    ikb_work = ''
    for work_item in reversed(result):
        work_id = work_item[0]
        name = work_item[1]
        income = work_item[2]
        xp = work_item[3]
        cost = work_item[4]

        ikb_work += f"[InlineKeyboardButton('{name} [+{income}$]', callback_data = 'game_work_{work_id}')],"


        cursor.execute(f"SELECT work_id FROM game WHERE id = {call.from_user.id}")
        user_work_id = cursor.fetchone()[0]
        
        if call.data == f'game_work_{work_id}' and user_work_id >= work_id:

            # ТАЙМАУТ
            cursor.execute(f"SELECT work_time FROM game WHERE id = {call.from_user.id}")
            bonus_time = cursor.fetchone()[0]
            if bonus_time != None:
                if bonus_time > datetime.now():
                    remains_time = bonus_time - datetime.now()
                    hours, remainder = divmod(remains_time.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    await call.message.delete()
                    await call.message.answer_photo(var.img_timeout, f"Работать можно через {minutes} минут {seconds} секунд <i>(в {bonus_time.strftime('%H:%M:%S')})</i>", reply_markup = functions.ButtonBack(callback = 'game_work'))
                    return
            
            date_finish = datetime.now() + timedelta(minutes = 10)
            cursor.execute(f"UPDATE game SET cash = cash + {income}, xp = xp + {xp}, work_time = '{date_finish}' WHERE id = {call.from_user.id}")
            connection.commit()
            await call.message.delete()
            await call.message.answer_photo(var.img_income, f'''
✅ Вы работали {name} и получили {income}$, {xp} xp

{functions.get_new_balance(old_balance, call)}

Повторно работать можно через 10 минут
            ''', reply_markup = functions.set_back_button('game_work'))

            return
        
        if call.data == f'game_work_{work_id}':
            # выбираем все данный с бд
            cursor.execute(f"SELECT name FROM work WHERE work_id = (SELECT work_id FROM game WHERE id = {call.from_user.id})")
            job_name = cursor.fetchone()[0]
            # выбирает стоимость
            user_xp = functions.get_xp(call)
            diff_xp = cost - user_xp
            await call.message.delete()
            await call.message.answer_photo(var.img_error, f'У тебя недостаточно навыков, чтобы работать {name}\n\nТвоя квалификация: {job_name}\n\n✨ До повышения осталось {diff_xp} xp\n\n<strong>[{user_xp} xp из {cost} xp]</strong>', reply_markup = functions.set_back_button('game_work'))
            return



    ikb_work = eval(f'''InlineKeyboardMarkup(inline_keyboard=[
        {ikb_work}
        functions.set_button_back_ikb('game')
    ])''')

    # главная: работы
    if call.data == 'game_work':

        # проверка на новый уровень
        cursor.execute(f"SELECT cost_xp FROM work WHERE work_id = (SELECT work_id FROM game WHERE id = {call.from_user.id}) + 1")
        cost_xp = cursor.fetchone()[0]
        user_xp = functions.get_xp(call)
        if cost_xp < user_xp:
            cursor.execute(f"UPDATE game SET work_id = work_id + 1 WHERE work_id = (SELECT work_id FROM game WHERE id = {call.from_user.id})")
            connection.commit()
            print('Уровень повышен!')

        # выбираем все данный с бд
        cursor.execute(f"SELECT * FROM work WHERE work_id = (SELECT work_id FROM game WHERE id = {call.from_user.id})")
        work_item = cursor.fetchone()
        work_id = work_item[0]
        name = work_item[1]
        income = work_item[2]
        xp = work_item[3]
        cost = work_item[4]

        # выбирает стоимость
        cursor.execute(f"SELECT cost_xp FROM work WHERE work_id = (SELECT work_id FROM game WHERE id = {call.from_user.id}) + 1")
        cost_xp = cursor.fetchone()[0]
        user_xp = functions.get_xp(call)
        diff_xp = cost_xp - user_xp


        await call.message.delete()
        await call.message.answer_photo(var.img_job, f'Ваша квалификация: <strong>{name}</strong>\n\n✨ До повышения осталось {diff_xp} xp\n\n<strong>[{user_xp} xp из {cost_xp} xp]</strong>', reply_markup = ikb_work)
        return







def reg_game_work(dp: Dispatcher):
    print('[COGS] game/work - is connected')
    dp.register_callback_query_handler(game_work, lambda c: c.data.startswith('game_work'))