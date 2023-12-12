from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
import functions
import var
from datetime import datetime, timedelta
import asyncio
from cogs.config import load_config
import var
from SQL import cursor, connection
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


# cursor.execute( "DROP TABLE  IF EXISTS users" )
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id BIGINT,
    exclusive DATE
    );""")
connection.commit()



ExclusiveMainDesc = '''
💎 Преимущества подписки <strong>«Melior Work»</strong>:

✅ Доступ в приватный телеграм канал:
• Уроки, гайды и файлы по Нейросетям (Stabble Diffusion, ChatGPT)
• Уроки, гайды и файлы по 3D Графике (Blender, UE5)
• Уроки, гайды и файлы по Монтажу (After Effect, Premier Pro)
• Записи всех стримов

✅ Доступ на приватный Discord сервер:
• Возможность пообщаться со мной на стриме
• Доступ в закрытый чат ⁠Discord
• Возможности платных ролей: <i>2x бонусы, доступ к закрытым каналам, все специальности, возможность выиграть x5-x50 в казино</i>
'''

PriceDesc = f'''Если вам покажется что цена 800 рублей большая, то вспомните что неподалёку от вас стоит киоск, в котором школьник покупает себе HQD за эти же {var.price_exclusive_rub} рублей'''

ikbExclusive = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('✨ Discord сервер?', callback_data = 'discord'), InlineKeyboardButton('💎 Купить подписку', callback_data = 'buy')],
    # [InlineKeyboardButton('✨ Discord сервер?', callback_data = 'discord')],
    # [InlineKeyboardButton('❌ Подписка недоступна', callback_data = 'nope')]
])
functions.ButtonBack(ikbExclusive)



ikbExclusive2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('💎 Купить подписку', callback_data='buy')]
])
functions.ButtonBack(ikbExclusive2, 'exclusive_back')


DiscordMainDesc = '''
✨ Приватный Discord сервер

Наш сервер поддерживает Discord бота на основе ChatGPT, который добавит новый уровень взаимодействия в наши общие беседы. Бот также имеет встроенную экономику, где ты можешь играть на виртуальную валюту и прокачивать свой профиль. Так что, если ты любишь интересные дискуссии и игры, то присоединяйся к нам уже сегодня! 

❤️ <i>Сервер создан для общения с друзьями и подписчиками <strong>«Melior Work»</strong></i>
'''

ikbDiscord = InlineKeyboardMarkup(inline_keyboard=[
])
functions.ButtonBack(ikbDiscord, 'exclusive_back')



# ОСНОВА

async def exclusive(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer_photo(photo = var.img_ex, caption = ExclusiveMainDesc, reply_markup = ikbExclusive)
    
async def discord(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer_photo(photo = var.img_discord, caption = DiscordMainDesc, reply_markup = ikbNull)






ikbNull = InlineKeyboardMarkup(inline_keyboard=[
])
functions.ButtonBack(ikbNull, 'exclusive')


exPay_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(f"💵 Оплатить {var.price_exclusive_rub}₽ на месяц", pay = True)],
])
functions.ButtonBack(exPay_ikb)

# ОПЛАТА
async def buy(call: types.CallbackQuery, state: FSMContext):
    cursor.execute(f"SELECT id FROM users WHERE exclusive IS NOT NULL AND id = {call.from_user.id}")
    if cursor.fetchone() != None:
        await call.message.delete()
        await call.message.answer_photo(var.img_ex, f'''
У тебя уже есть подписка! Действует до {functions.get_date_ex(call)}

Ссылка: {var.ex_chat_link}

<i>* Ваша заявка будет принята автоматически, т.к. вы являетесь подписчиком</i>''', reply_markup = ikbNull)
        return
    
    # ЗАПОМНИЛИ СООБЩЕНИЕ
    async with state.proxy() as data:
        data['state_pay'] = 'exclusive'

    from bot import bot, config
    await call.message.delete()
    await bot.send_invoice(call.message.chat.id,
                            title = "Подписка «Melior Work» на месяц",
                            description = f'📌 Если вам покажется что цена {var.price_exclusive_rub} рублей в месяц большая, то вспомните что неподалёку от вас стоит киоск, в котором школьник покупает себе HQD за эти же {var.price_exclusive_rub} рублей',
                            provider_token = config.tg_bot.paymaster,
                            currency = "rub",
                            photo_url = var.img_pay,
                            prices = [
                                types.LabeledPrice(
                                    label = "Доступ к приватному телеграму",
                                    amount = var.price_exclusive_rub * 100
                                )
                            ],
                            max_tip_amount = 2000 * 100,
                            suggested_tip_amounts = [50 * 100, 100 * 100, 200 * 100, 300 * 100],
                            photo_height = 1080,
                            photo_width = 1440,
                            is_flexible = False,
                            reply_markup = exPay_ikb,
                            start_parameter = "one-month-subscription",
                            payload = {"payload_key": "testt-invoice-payload"}
                            )





# обработчик событий по подаче заявки на вступление
async def exclusive_app_member(update: types.ChatJoinRequest):
    cursor.execute(f"SELECT id FROM users WHERE exclusive IS NOT NULL AND id = {update.from_user.id}")
    from bot import bot
    if cursor.fetchone() != None:
        await bot.approve_chat_join_request(chat_id = var.ex_chat_id, user_id = update.from_user.id)
        await bot.send_photo(chat_id = update.from_user.id, photo = var.img_accept_member, caption = f"✅ Ваша заявка на вступление в <strong>«Melior Work»</strong> принята! \n\nПодписка действует до {functions.get_date_ex(update)}", reply_markup = var.ikbClose)
    else:
        msg = await bot.send_photo(chat_id = update.from_user.id, photo = var.img_cancel_member, caption = "⭕️ Чтобы вашу заявку на вступление приняли — нужно иметь подписку <strong>«Melior Work»</strong> \n\n<i>Сообщение автоматически исчезнет через 30 секунд</i>", reply_markup = var.ikbClose)
        await asyncio.sleep(30)
        await msg.delete()







# # ! РЕФЕРАЛЬНАЯ СИСТЕМА
# # создание таблицы пользователей
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                    user_id INTEGER,
#                    referral_link TEXT,
#                    subscribed INTEGER)''')


# # обработчик команды /start
# @dp.message_handler(commands=['start'])
# async def start_handler(message: types.Message):
#     from bot import bot

#     # получаем реферальный ID из команды /start (если он есть)
#     referral_link = await bot.create_chat_invite_link(var.live_chat_id, name = 'Referral link')

#     if message.chat.type == 'private' and referral_link.endswith(var.ex_chat_id):
#         # добавляем пользователя в базу данных
#         user_id = message.from_user.id
#         cursor.execute("INSERT INTO users (user_id, referral_link, subscribed) VALUES (?, ?, ?)",
#                         (user_id, referral_link, 0))
#         connection.commit()
#         # отправляем сообщение о подписке на канал
#         await message.reply("Чтобы получить доступ к контенту канала, пожалуйста, подпишитесь на него.")
#     else:
#         await message.reply("Неправильная реферальная ссылка.")


# # обработчик подписки на канал
# @dp.channel_post_handler()
# async def channel_post_handler(message: types.Message):
#     # обновляем статус подписки пользователя в базе данных
#     user_id = message.from_user.id
#     cursor.execute("UPDATE users SET subscribed = 1 WHERE user_id = ?", (user_id,))
#     connection.commit()








def reg_exclusive(dp: Dispatcher):
    print('[COGS] exclusive - is connected')

    dp.register_callback_query_handler(exclusive, Text('exclusive'))
    dp.register_callback_query_handler(discord, Text('discord'))

    dp.register_chat_join_request_handler(exclusive_app_member) # обработчик подачи заявки на вступление

    # Оплата
    dp.register_callback_query_handler(buy, Text('buy'))