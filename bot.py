import asyncio
from aiogram import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from cogs.config import load_config
from SQL import cursor, connection
import var
import functions

# Handlers
from cogs.filters.admin import AdminFilter
from cogs.handlers.exclusive import ikbExclusive2
from cogs.middlewares.environment import EnvironmentMiddleware



async def on_startup(_):
    print("Bot connected")


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config = config))

def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)

def register_all_handlers(dp): 

    from cogs.handlers.main import reg_main
    reg_main(dp)

    from cogs.handlers.exclusive import reg_exclusive
    reg_exclusive(dp)
    
    from cogs.handlers.course.neural import reg_neural
    reg_neural(dp)

    from functions import reg_functions
    reg_functions(dp)

    from cogs.handlers.pay import reg_pay
    reg_pay(dp)

    from cogs.handlers.game.game import reg_game
    reg_game(dp) 

    from cogs.handlers.gesway import reg_gesway
    reg_gesway(dp)

    # from cogs.handlers.chatgpt import reg_chatgpt
    # reg_chatgpt(dp) # ! Не работает

    # from cogs.handlers.demotivator import reg_demotivator
    # reg_demotivator(dp)





# Подключение бота 
config = load_config(".env")
storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
bot = Bot( token = config.tg_bot.token, parse_mode = 'HTML', protect_content = True )
dp = Dispatcher( bot, storage = storage )

register_all_middlewares(dp, config)
register_all_filters(dp)
register_all_handlers(dp)


null_ikb = InlineKeyboardMarkup(inline_keyboard=[
])
functions.ButtonBack(null_ikb)

@dp.callback_query_handler()
async def callback_all(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer_photo(var.img_error, '🛠 Функция находится в разработке. Попробуйте позже', reply_markup = null_ikb)




# ЦИКЛ НА ЕЖЕДНЕВНУЮ ПРОВЕРКУ
async def check_day():
    while True:
        try:
            cursor.execute("SELECT id FROM users WHERE exclusive < NOW()")
            records = cursor.fetchall()

            for record in records:

                await functions.send_admin(f'У пользователя {record} истекла подписка. Он был исключён!')

                await bot.kick_chat_member(chat_id = var.ex_chat_id, user_id = record[0])
                await bot.unban_chat_member(chat_id = var.ex_chat_id, user_id = record[0])
                await bot.send_photo(chat_id = record[0], photo = var.img_endEx, caption = "❌ Ваша подписка на <strong>«Melior Exclusive»</strong> истекла \n\nЧтобы вернуть все преимущества подписки — оплатите её повторно", reply_markup = ikbExclusive2)

            cursor.execute('UPDATE users SET exclusive = NULL WHERE exclusive < NOW()')
            connection.commit()

        except Exception as e:
            print("Error while checking for expired subscriptions:", e)

        await asyncio.sleep(60 * 60 * 24) # ЗАДЕРЖКА НА 1 СУТКИ
 


# ЦИКЛ НА ЕЖЕЧАСНУЮ ПРОВЕРКУ
async def check_hour():
    while True:
        from bot import bot

        # ДОХОД БИЗНЕСОВ
        cursor.execute(f"SELECT id FROM game WHERE business_id IS NOT NULL")
        records_business = cursor.fetchall()

        for record in records_business:
            user_channel_status = await bot.get_chat_member(chat_id = var.live_chat_id, user_id = record[0])
            if user_channel_status["status"] != 'left':
                cursor.execute(f"SELECT income FROM shop_business WHERE business_id = (SELECT business_id FROM game WHERE id = {record[0]})")
                business_income = cursor.fetchone()
                if business_income != None:
                    business = f"(SELECT business_id FROM game WHERE id = {record[0]})" # бизнес айди пользователя
                    business_income = f"(SELECT income FROM shop_business WHERE business_id = {business})" # доход бизнеса
                    cursor.execute(f"UPDATE game SET business_cash = business_cash + {business_income}")
        
        # ДОХОД КРИПТОВАЛЮТЫ
        cursor.execute(f"SELECT id FROM game WHERE farm_id IS NOT NULL")
        records_farm = cursor.fetchall()

        for record in records_farm:
            user_channel_status = await bot.get_chat_member(chat_id = var.live_chat_id, user_id = record[0])
            if user_channel_status["status"] != 'left':
                cursor.execute(f"SELECT income FROM shop_farm WHERE farm_id = (SELECT farm_id FROM game WHERE id = {record[0]})")
                crypto_income = cursor.fetchone()
                if crypto_income != None:
                    crypto = f"(SELECT farm_id FROM game WHERE id = {record[0]})" # крипта айди пользователя
                    crypto_income = f"(SELECT income FROM shop_farm WHERE farm_id = {crypto})" # доход крипты
                    cursor.execute(f"UPDATE game SET crypto = crypto + {crypto_income}")

        connection.commit()

        await asyncio.sleep(60 * 60) # ЗАДЕРЖКА НА 1 час




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_day())
    loop.create_task(check_hour())
    executor.start_polling(dp, loop = loop, skip_updates = False, on_startup = on_startup)