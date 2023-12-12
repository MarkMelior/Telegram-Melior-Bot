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
from var import add_cash, add_xp


# 1 - Бизнес
cursor.execute( "DROP TABLE IF EXISTS shop_business" )
cursor.execute( """CREATE TABLE IF NOT EXISTS shop_business (
    business_id SERIAL PRIMARY KEY,
    name TEXT,
    income BIGINT,
    cost BIGINT
)""" )
cursor.execute(f"INSERT INTO shop_business(name, income, cost) VALUES ('☕️ Кафе', {add_cash / 6}, {add_cash * 20})")
cursor.execute(f"INSERT INTO shop_business(name, income, cost) VALUES ('🚧 Логистика и доставка', {add_cash * 1.8 / 6}, {add_cash * 1.8 * 40})")
cursor.execute(f"INSERT INTO shop_business(name, income, cost) VALUES ('🏥 Аптека', {add_cash * 1.8 * 2 / 6}, {add_cash * 1.8 * 4 * 50})")
cursor.execute(f"INSERT INTO shop_business(name, income, cost) VALUES ('😎 Кинотеатр', {add_cash * 1.8 * 3 / 6}, {add_cash * 1.8 * 8 * 60})")
cursor.execute(f"INSERT INTO shop_business(name, income, cost) VALUES ('💻 Разработка ПО', {add_cash * 1.8 * 7 / 6}, {add_cash * 1.8 * 16 * 70})")
cursor.execute(f"INSERT INTO shop_business(name, income, cost) VALUES ('🚗 Автомобильный дилер', {add_cash * 1.8 * 14 / 6}, {add_cash * 1.8 * 32 * 80})")
cursor.execute(f"INSERT INTO shop_business(name, income, cost) VALUES ('📢 Рекламное агентство', {add_cash * 1.8 * 30 / 6}, {add_cash * 1.8 * 64 * 90})")
cursor.execute(f"INSERT INTO shop_business(name, income, cost) VALUES ('💎 Производство', {add_cash * 1.8 * 60 / 6}, {add_cash * 1.8 * 128 * 100})")


# 2 - Майнинг фермы
cursor.execute( "DROP TABLE IF EXISTS shop_farm" )
cursor.execute( """CREATE TABLE IF NOT EXISTS shop_farm (
    farm_id SERIAL PRIMARY KEY,
    name TEXT,
    income BIGINT,
    cost BIGINT
)""" )
cursor.execute(f"INSERT INTO shop_farm(name, income, cost) VALUES ('🎒 Ebang Ebit E12+', {add_cash / 5 / 37}, {add_cash * 1.8 * 30})")
cursor.execute(f"INSERT INTO shop_farm(name, income, cost) VALUES ('🎒 Whatsminer M32-70', {add_cash * 1.8 / 5 / 37}, {add_cash * 1.8 * 2 * 50})")
cursor.execute(f"INSERT INTO shop_farm(name, income, cost) VALUES ('🎒 StrongU STU-U8', {add_cash * 1.8 * 2 / 5 / 37}, {add_cash * 1.8 * 4 * 60})")
cursor.execute(f"INSERT INTO shop_farm(name, income, cost) VALUES ('🎒 Innosilicon A11 Pro', {add_cash * 1.8 * 4 / 5 / 37}, {add_cash * 1.8 * 8 * 70})")
cursor.execute(f"INSERT INTO shop_farm(name, income, cost) VALUES ('💎 Antminer S19 Pro', {add_cash * 1.8 * 8 / 5 / 37}, {add_cash * 1.8 * 16 * 80})")

# 3 - Дом
cursor.execute( "DROP TABLE IF EXISTS shop_house" )
cursor.execute( """CREATE TABLE IF NOT EXISTS shop_house (
    house_id SERIAL PRIMARY KEY,
    name TEXT,
    cost BIGINT
)""" )
cursor.execute(f"INSERT INTO shop_house(name, cost) VALUES ('Холодильник соседа', 180000)")
cursor.execute(f"INSERT INTO shop_house(name, cost) VALUES ('Квартира', 555000)")
cursor.execute(f"INSERT INTO shop_house(name, cost) VALUES ('Особняк', 7300000)")

# 4 - Транспорт
cursor.execute( "DROP TABLE IF EXISTS shop_car" )
cursor.execute( """CREATE TABLE IF NOT EXISTS shop_car (
    car_id SERIAL PRIMARY KEY,
    name TEXT,
    cost BIGINT
)""" )
cursor.execute(f"INSERT INTO shop_car(name, cost) VALUES ('Лада калина', 368000)")
cursor.execute(f"INSERT INTO shop_car(name, cost) VALUES ('Макларен', 5580000)")
cursor.execute(f"INSERT INTO shop_car(name, cost) VALUES ('Истребитель', 22700000)")


connection.commit()

#######

# 1 - Профессия





back_game_ikb = functions.set_back_button('game')

async def game_shop_func(call, shop_list):
    # проходим по списку: [[list1, 'business'], [list2, 'farm']]
    for shop in shop_list:
        ikb_list = '' # temp-лист
        data = shop[-1] # 'business'
        item_count = 0 # счётчик списков: [list1, 'business']
        # проходим по списку: [list1, 'business']
        for shop_item in shop[0]:
            item_count += 1

            check_income = shop_item[0]

            if check_income:
                title = shop_item[1]
                income = shop_item[2]
                cost = shop_item[3]
                symb = shop_item[4]
            else:
                title = shop_item[1]
                income = ''
                cost = shop_item[2]
                symb = ''


            ikb_list += f'[InlineKeyboardButton(f"{title} - {cost}$", callback_data = f"shop_item_{data}{item_count}")],'

            # элемент списка
            if call.data == f'shop_item_{data}{item_count}':
                ikb = InlineKeyboardMarkup(inline_keyboard = [
                    # [InlineKeyboardButton('Купить', callback_data = f'game_shop_buy_{data}{item_count}')] if functions.check_user_business(call) != True else [InlineKeyboardButton('Продать свой бизнес', callback_data = f'null')]
                    [InlineKeyboardButton('Купить', callback_data = f'game_shop_buy_{data}{item_count}')]
                ])
                functions.ButtonBack(ikb, f'game_shop_{data}')

                await call.message.delete()
                await call.message.answer_photo(eval(f'var.img_shop_{data}'), f'{title}\n\nСтоимость: {cost}$\n\nДоход: {income}{symb} в час\n\n💰 Ваш баланс составляет: {functions.get_balance(call)}$', reply_markup = ikb)

            # купить элемент из списка
            if call.data == f'game_shop_buy_{data}{item_count}':
                cursor.execute(f"SELECT cash FROM game WHERE id = {call.from_user.id}")
                balance_user = cursor.fetchone()[0]
                if cost > balance_user:
                    await call.message.delete()
                    await call.message.answer_photo(var.img_error, f'❌ У вас недостаточно средств! Нехаватает: {cost - balance_user}$\n\nСтоимость: {cost}$\n\n💰 Ваш баланс составляет: {balance_user}$', reply_markup = functions.set_back_button(f'game_shop_{data}'))
                
                else:
                    img = var.img_error

                    # TODO можно засунуть в лист
                    if data == 'business' and functions.check_user_business(call) == True:
                        description = f'❌ У вас уже есть бизнес! Чтобы приобрести новый бизнес - вам нужно продать свой старый'
                    
                    elif data == 'farm' and functions.check_user_farm(call) == True:
                        description = f'❌ У вас уже есть майнинг ферма! Чтобы приобрести новую ферму - вам нужно продать свою старую'

                    elif data == 'house' and functions.check_user_house(call) == True:
                        description = f'❌ У вас уже есть дом! Чтобы приобрести новый дом - вам нужно продать свой старый'

                    elif data == 'car' and functions.check_user_car(call) == True:
                        description = f'❌ У вас уже есть транспорт! Чтобы приобрести новый транспорт - вам нужно продать свой старый'

                    else:
                        buyed = f"(SELECT {data}_id FROM shop_{data} WHERE name = '{title}')"
                        cursor.execute(f"(SELECT cash FROM game WHERE id = {call.from_user.id})")
                        cash_info = cursor.fetchone()[0]
                        cursor.execute(f"UPDATE game SET cash = {cash_info} - {cost}, {data}_id = {buyed} WHERE id = {call.from_user.id}")
                        connection.commit()

                        img = var.img_buyed
                        description = f'✅ Вы приобрели "{title}". Поздравляем с успешной покупкой!\n\n{functions.get_new_balance(cash_info, call)}\n\n🍃 Теперь ваш доход составляет: {income}{symb} в час'
                    
                    await call.message.delete()
                    await call.message.answer_photo(img, description, reply_markup = back_game_ikb)

        # имущества (бизнесы, майнинг фермы...)
        if call.data == f'game_shop_{data}':

            # проверка: есть имущество у пользователя?
            cursor.execute(f"SELECT {data}_id FROM game WHERE id = {call.from_user.id}")
            business_id = cursor.fetchone()
            if business_id != None:
                business_id = business_id[0]

            # если бизнес
            if call.data == f'game_shop_business':
                ikb = eval(f'''InlineKeyboardMarkup(inline_keyboard=[
                    {ikb_list}
                    [InlineKeyboardButton(f'💸 Снять {functions.get_business_cash(call)}$', callback_data = 'game_take_business')] if functions.get_business_cash(call) != 0 else '',
                    [InlineKeyboardButton('‼️ Продать бизнес', callback_data = f'game_shop_sell_{data}')] if business_id != None else '',
                    functions.set_button_back_ikb('game')
                ])''')
                img = var.img_shop_business

                cursor.execute(f"SELECT name FROM shop_business WHERE business_id = (SELECT business_id FROM game WHERE id = {call.from_user.id})")
                name_select = cursor.fetchone()


                description = f"У вас нет бизнеса, который приносил бы доход" if functions.get_business_income(call) == None else f"У вас {name_select[0]}\n\nДоход: +{functions.get_business_income(call)[0]}{symb} в час"
            
            # если ферма
            elif call.data == f'game_shop_farm':
                ikb = eval(f'''InlineKeyboardMarkup(inline_keyboard=[
                    {ikb_list}
                    [InlineKeyboardButton('♻️ Обменять {functions.get_crypto(call)}✦ на $', callback_data = 'game_change_crypto')] if functions.get_crypto(call) != 0 else '',
                    [InlineKeyboardButton('‼️ Продать майнинг ферму', callback_data = f'game_shop_sell_{data}')] if business_id != None else '',
                    functions.set_button_back_ikb('game')
                ])''')
                img = var.img_shop_farm

                cursor.execute(f"SELECT name FROM shop_farm WHERE farm_id = (SELECT farm_id FROM game WHERE id = {call.from_user.id})")
                name_select = cursor.fetchone()

                description = f"У вас нет майнинг фермы, которая приносила бы доход" if functions.get_farm_income(call) == None else f"У вас {name_select[0]}\n\nДоход: +{functions.get_farm_income(call)[0]}{symb} в час"
            
            # если дом
            elif call.data == f'game_shop_house':
                ikb = eval(f'''InlineKeyboardMarkup(inline_keyboard=[
                    {ikb_list}
                    [InlineKeyboardButton('‼️ Продать дом', callback_data = f'game_shop_sell_{data}')] if business_id != None else '',
                    functions.set_button_back_ikb('game')
                ])''')
                img = var.img_bonus_yes # todo IMG
                description = 'None' # todo описание
            
            # если машина
            elif call.data == f'game_shop_car':
                ikb = eval(f'''InlineKeyboardMarkup(inline_keyboard=[
                    {ikb_list}
                    [InlineKeyboardButton('‼️ Продать транспорт', callback_data = f'game_shop_sell_{data}')] if business_id != None else '',
                    functions.set_button_back_ikb('game')
                ])''')
                img = var.img_bonus_yes # todo IMG
                description = 'None' # todo описание


            await call.message.delete()
            await call.message.answer_photo(img, description, reply_markup = ikb)



        # продажа имущества
        if call.data == f'game_shop_sell_{data}':
            idd = (f"(SELECT {data}_id FROM game WHERE id = {call.from_user.id})")
            cursor.execute(f"SELECT cost FROM shop_{data} WHERE {data}_id = {idd}")
            cost_data = cursor.fetchone()[0]
            cursor.execute(f"(SELECT cash FROM game WHERE id = {call.from_user.id})")
            cash_old = cursor.fetchone()[0]
            cursor.execute(f"UPDATE game SET {data}_id = Null, cash = {cash_old} + ({cost_data} / 2) WHERE id = {call.from_user.id}")
            connection.commit()

            await call.message.delete()
            await call.message.answer_photo(var.img_sell, f'✅ Вы продали имущество за: {int(cost_data / 2)}$\n\n{functions.get_new_balance(cash_old, call)}', reply_markup = back_game_ikb)
   





async def game_func(call: types.CallbackQuery):
    # обмен криптовалюты
    if call.data == 'game_change_crypto':
        old_balance = functions.get_balance(call)
        crypto = functions.get_crypto(call)
        cursor.execute(f"UPDATE game SET cash = cash + (crypto * 37), crypto = 0 WHERE id = {call.from_user.id}")
        connection.commit()
        balance_desc = functions.get_new_balance(old_balance, call)

        await call.message.delete()
        await call.message.answer_photo(var.img_sell, f'✅ {crypto}✦ были успешно проданы за {crypto * 37}$ и зачислены на ваш баланс! \n\n{balance_desc}', reply_markup = back_game_ikb)

    # вывести деньги со счёта бизнеса
    if call.data == 'game_take_business':
        old_balance = functions.get_balance(call)
        business_cash = functions.get_business_cash(call)
        cursor.execute(f"UPDATE game SET cash = cash + business_cash, business_cash = 0 WHERE id = {call.from_user.id}")
        connection.commit()
        balance_desc = functions.get_new_balance(old_balance, call)

        await call.message.delete()
        # todo IMG
        await call.message.answer_photo(var.img_sell, f'✅ Деньги <i>({business_cash}$)</i> были успешно сняты с счёта бизнеса и зачислены на ваш баланс! \n\n{balance_desc}', reply_markup = back_game_ikb)





async def game_shop(call: types.CallbackQuery):
    
    list1 = []
    cursor.execute("SELECT * FROM shop_business")
    for i in cursor.fetchall():
        list1.append([True, i[1], i[2], i[3], '$'])

    list2 = []
    cursor.execute("SELECT * FROM shop_farm")
    for i in cursor.fetchall():
        list2.append([True, i[1], i[2], i[3], '✦'])

    list3 = []
    cursor.execute("SELECT * FROM shop_house")
    for i in cursor.fetchall():
        list3.append([False, i[1], i[2]])

    list4 = []
    cursor.execute("SELECT * FROM shop_car")
    for i in cursor.fetchall():
        list4.append([False, i[1], i[2]])


    shop_list = [[list1, 'business'], [list2, 'farm'], [list3, 'house'], [list4, 'car']]
    
    await game_shop_func(call, shop_list)



def reg_game_shop(dp: Dispatcher):
    print('[COGS] game/shop - is connected')
    dp.register_callback_query_handler(game_shop, lambda c: c.data.startswith(('game_shop', 'shop_item')))
    dp.register_callback_query_handler(game_func, Text(['game_change_crypto', 'game_take_business']))