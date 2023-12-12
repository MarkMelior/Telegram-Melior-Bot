from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram import Dispatcher, types
import functions
import var
from datetime import datetime, timedelta
import var
from SQL import cursor, connection
from datetime import datetime
from aiogram.dispatcher import FSMContext
from cogs.handlers.course.neural import add_course, courseBack_ikb


# предварительный заказ (ответ должен быть получен в течение 10 секунд)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery, state: FSMContext):
    # async with state.proxy() as data:
    #     if data['state_pay'] == 'exclusive':
    from bot import bot
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


ikbBuyed = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('📎 На главную', callback_data = 'start_save')]
])

# УСПЕШНАЯ ОПЛАТА
async def successful_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['state_pay'] == 'exclusive':
            # ПРОВЕРКА НА СУЩЕСТВО В БД
            functions.check_user_db(message)

            # ДОБАВЛЕНИЕ 30 ДНЕЙ ПОДПИСКИ
            date_sub = (datetime.now() + timedelta(days = 30)).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(f"UPDATE users SET exclusive = '{date_sub}' WHERE id = {message.from_user.id}")
            connection.commit()
            
            # ИНФЙОРМАЦИЯ О ПЛАТЕЖЕ
            payment_info = message.successful_payment.to_python()
            for k, v in payment_info.items():
                print(f"{k} = {v}")

            await functions.send_admin(f'Пользователь {message.from_user.id} оформил подписку <strong>«Melior Exclusive»</strong> \n\n Информация о платеже: {payment_info}')


            # ОТПРАВКА СООБЩЕНИЯ
            await message.answer_photo(photo = var.img_thanks, caption = f'''
✅ Оллата на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошла успешно!

Подписка <strong>«Melior Exclusive»</strong> действует до {functions.get_date_ex(message)}

Ссылка: {var.ex_chat_link}

<i>* Ваша заявка будет принята автоматически, т.к. вы являетесь подписчиком</i>
            ''', reply_markup = ikbBuyed)

        if data['state_pay'] == 'neural_course':
            # инфо о платеже
            payment_info = message.successful_payment.to_python()
            for k, v in payment_info.items():
                print(f"{k} = {v}")

            await functions.send_admin(f'Пользователь {message.from_user.id} купил курс <strong>Neural Dreaming 2023</strong> \n\n Информация о платеже: {payment_info}')
            add_course(message)
            await message.answer_photo(photo = var.img_thanks, caption = f'✅ Оллата на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошла успешно! \n \n Доступ к <strong>«Neural Dreaming 2023»</strong> получен!', reply_markup = courseBack_ikb)


ikbExclusive3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('💎 Купить подписку', callback_data='buy')]
])
functions.ButtonBack(ikbExclusive3)



def reg_pay(dp: Dispatcher):
    print('[COGS] pay - is connected')
    # Оплата
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)
    dp.register_message_handler(successful_payment, content_types = ContentType.SUCCESSFUL_PAYMENT)