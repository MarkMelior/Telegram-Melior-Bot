from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
import functions
from SQL import cursor, connection
import random
import time
import var
from datetime import datetime, timedelta


async def game_bonus(call: types.CallbackQuery):

    cursor.execute(f"SELECT bonus_time FROM game WHERE id = {call.from_user.id}")
    bonus_time = cursor.fetchone()[0]
    if bonus_time != None:
        if bonus_time > datetime.now():
            remains_time = bonus_time - datetime.now()
            hours, remainder = divmod(remains_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            await call.message.delete()
            await call.message.answer_photo(var.img_timeout, f"Следующий бонус можно получить через {minutes} минут {seconds} секунд <i>(в {bonus_time.strftime('%H:%M:%S')})</i>", reply_markup = functions.ButtonBack(callback = 'game'))
            return

    balance_user = functions.get_balance(call)

    bonus_cash = random.randint(1000, 3200)
    bonus_xp = random.randint(100, 320)
    bonn = random.randint(1, 10) # шанс получения бонуса

    if bonn > 1: # шанс получить бонус 90%
        media = var.img_bonus_yes
        text = f'✅ Вы получили бонус: {bonus_cash}$ + {bonus_xp} xp'
        date_finish = datetime.now() + timedelta(hours = 1)
        cursor.execute(f"UPDATE game SET cash = cash + {bonus_cash}, xp = xp + {bonus_xp}, bonus_time = '{date_finish}' WHERE id = {call.from_user.id}")
        connection.commit()
    else:
        media = var.img_bonus_no
        text = '❌ Тебе не дали бонус. Приходи в следующий раз'


    await call.message.delete()
    await call.message.answer_photo(media, f'''
{text}

{functions.get_new_balance(balance_user, call)}

Следуший бонус можно получить через 1 час
    ''', reply_markup = functions.set_back_button('game'))







def reg_game_bonus(dp: Dispatcher):
    print('[COGS] game/bonus - is connected')
    dp.register_callback_query_handler(game_bonus, Text('game_bonus'))