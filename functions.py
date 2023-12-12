from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SQL import cursor, connection
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from datetime import datetime


""" EXCLUSIVE """

def check_user_db(message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO users VALUES ({message.from_user.id}, NULL)")
        connection.commit()

def get_date_ex(message):
    cursor.execute(f'SELECT exclusive FROM users WHERE id = {message.from_user.id}')

    db_date = cursor.fetchone()[0]
    days_left = (db_date - datetime.today().date()).days
    date_str = datetime.strftime(db_date, "%d.%m.%Y")
    days_left_str = str(abs(days_left)) if days_left < 0 else str(days_left)

    result = f'{date_str} <i>(осталось {days_left_str} дней)</i>'
    return result

# проверка, есть ли подписка у пользователя
def have_ex(message):
    cursor.execute(f"SELECT id FROM users WHERE exclusive > NOW() AND id = {message.from_user.id}")

    if cursor.fetchone() != None:
        return True # пользователь есть
    
    return None # пользователя нет


""" ADMIN """

async def send_admin(text):
     
    from bot import bot, config

    for admin in config.tg_bot.admin_ids:
        await bot.send_message(chat_id = admin, text = '[ ⭕️ ADMINS ]\n\n' + text)





def ButtonBack(ikbBack = None, callback = None):
    if ikbBack == None:
        ikbBack = InlineKeyboardMarkup()
    ikbBack.add(InlineKeyboardButton('📎 На главную', callback_data = 'start'))
    if callback:
        ikbBack.insert(InlineKeyboardButton('◀️ Назад', callback_data = callback))
    return ikbBack

def set_back_button(callback_data):
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Выйти', callback_data = callback_data)]
    ])
    return ikb

def get_main_back_ikb(callback_data):
    return [InlineKeyboardButton('📎 На главную', callback_data = 'start'), InlineKeyboardButton('◀️ Назад', callback_data = callback_data) if callback_data else '']

def set_button_back_ikb(callback_data):
    return [InlineKeyboardButton('Выйти', callback_data = callback_data)]


"""GAME"""

def get_balance(call):
    cursor.execute(f"SELECT cash FROM game WHERE id = {call.from_user.id}")
    return cursor.fetchone()[0]

def get_xp(call):
    cursor.execute(f"SELECT xp FROM game WHERE id = {call.from_user.id}")
    return cursor.fetchone()[0]

def get_lvl(call):
    cursor.execute(f"SELECT lvl FROM game WHERE id = {call.from_user.id}")
    return cursor.fetchone()[0]

def get_business_cash(call):
    cursor.execute(f"SELECT business_cash FROM game WHERE id = {call.from_user.id}")
    return cursor.fetchone()[0]

def get_crypto(call):
    cursor.execute(f"SELECT crypto FROM game WHERE id = {call.from_user.id}")
    return cursor.fetchone()[0]

def get_new_balance(old_balance, call):
    cursor.execute(f"SELECT cash FROM game WHERE id = {call.from_user.id}")
    new_balance = cursor.fetchone()[0]
    result = f'💰 Ваш баланс: {old_balance}$ -> <strong>{new_balance}$</strong>'
    return result

def get_business_income(call):
    cursor.execute(f"SELECT income FROM shop_business WHERE business_id = (SELECT business_id FROM game WHERE id = {call.from_user.id})")
    return cursor.fetchone()

def get_farm_income(call):
    cursor.execute(f"SELECT income FROM shop_farm WHERE farm_id = (SELECT farm_id FROM game WHERE id = {call.from_user.id})")
    return cursor.fetchone()

def check_user_business(call):
    cursor.execute(f"SELECT id FROM game WHERE business_id != 0 AND id = {call.from_user.id}")
    result = cursor.fetchone()
    print(result)
    if result:
        return True
    return False

def check_user_farm(call):
    cursor.execute(f"SELECT id FROM game WHERE farm_id != 0 AND id = {call.from_user.id}")
    result = cursor.fetchone()
    print(result)
    if result:
        return True
    return False

def check_user_house(call):
    cursor.execute(f"SELECT id FROM game WHERE house_id != 0 AND id = {call.from_user.id}")
    result = cursor.fetchone()
    print(result)
    if result:
        return True
    return False

def check_user_car(call):
    cursor.execute(f"SELECT id FROM game WHERE car_id != 0 AND id = {call.from_user.id}")
    result = cursor.fetchone()
    print(result)
    if result:
        return True
    return False





""" OTHER """

# Кнопка закрытия сообщения
async def close_msg(msg: types.CallbackQuery):
    await msg.message.delete()






def reg_functions(dp: Dispatcher):
    print('[COGS] functions - is connected')
    dp.register_callback_query_handler(close_msg, Text('close_msg'))
