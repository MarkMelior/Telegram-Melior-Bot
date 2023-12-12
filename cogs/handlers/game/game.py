from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from SQL import cursor, connection
import var
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import functions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


# cursor.execute( "DROP TABLE IF EXISTS game" )
cursor.execute("""CREATE TABLE IF NOT EXISTS game (
    id bigint,
    xp int,
    lvl int,
    cash BIGINT,
    business_id INT,
    business_cash BIGINT,
    farm_id INT,
    crypto BIGINT DEFAULT 0,
    bonus_time TIMESTAMP,
    work_time TIMESTAMP,
    work_id INT,
    car_id INT,
    house_id INT
    );""")
connection.commit()




async def game(call: types.CallbackQuery, state: FSMContext):
    await state.finish() # сбрасывает таймаут

    # ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ В БД
    cursor.execute(f"SELECT id FROM game WHERE id = {call.from_user.id}")
    if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO game VALUES ({call.from_user.id}, 0, 1, 500, Null, 0, Null, 0, Null, Null, 1, 0, 0)")
        connection.commit()

    # ИНЛАЙН КЛАВИАТУРА
    profile_ikb = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton('🎰 Играть в казино', callback_data = 'game_casino')],
        [InlineKeyboardButton('💼 Работать', callback_data = 'game_work'), InlineKeyboardButton('💰 Получить бонус', callback_data = 'game_bonus')],
        [InlineKeyboardButton(f'📊 Бизнес: {functions.get_business_cash(call)}$ (+{0 if functions.get_business_income(call) == None else functions.get_business_income(call)[0]}$ в час)', callback_data = 'game_shop_business')],
        [InlineKeyboardButton(f'⚡️ Крипта: {functions.get_crypto(call)}✦ (+{0 if functions.get_farm_income(call) == None else functions.get_farm_income(call)[0]}✦ в час)', callback_data = 'game_shop_farm')],
        # [InlineKeyboardButton('🏠 Дом: Холодильник соседа', callback_data = 'game_shop_house')],
        # [InlineKeyboardButton('🚗 Транспорт: Вертолёт', callback_data = 'game_shop_car')],
        functions.get_main_back_ikb('additional')
    ])

    # СООБЩЕНИЕ
    await call.message.delete()
    await call.message.answer_photo(var.img_game, f'Добро пожаловать в экономическую игру!\n\n💰 Ваш баланс составляет: {functions.get_balance(call)}$\n\n✨ Выш опыт: {functions.get_xp(call)} xp\n\n<i>За игровую валюты вы можете приобрести скидку на <strong>«Melior Exclusive»</strong></i>', reply_markup = profile_ikb)



from cogs.handlers.game.casino import FSMCasino

def reg_game(dp: Dispatcher):
    print('[COGS] game - is connected')
    dp.register_callback_query_handler(game, Text('game'), state = [None, FSMCasino.bet])


    from cogs.handlers.game.shop import reg_game_shop
    reg_game_shop(dp)

    from cogs.handlers.game.casino import reg_game_casino
    reg_game_casino(dp)

    from cogs.handlers.game.bonus import reg_game_bonus
    reg_game_bonus(dp)

    from cogs.handlers.game.work import reg_game_work
    reg_game_work(dp)