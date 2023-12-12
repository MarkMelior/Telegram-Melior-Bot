from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
import functions
from SQL import cursor, connection
from aiogram.dispatcher.filters.state import StatesGroup, State
import random
import var


class FSMCasino(StatesGroup):
    bet = State()



ikbCasino = functions.set_back_button('game')


async def game_casino(call: types.CallbackQuery, state: FSMContext):
    balance = functions.get_balance(call)
   
    await call.message.delete()
    msg = await call.message.answer_photo(var.img_casino, f'''
Добро пожаловать в казино!

💰 Твой баланс составляет: {balance}$

Укажи свою ставку... Например: 100
    ''', reply_markup = ikbCasino)

    # ЗАПОМНИЛИ СООБЩЕНИЕ
    async with state.proxy() as data:
        data['msg_content'] = msg

    await FSMCasino.bet.set()


async def game_casino_state(msg: types.Message, state: FSMContext):
    await msg.delete()

    # случайное число, на основе которого работает рандомизация
    number = random.randint(1, 1000)

    balance_user = functions.get_balance(msg)

    amount = msg.text

    lose = var.img_lose
    win = var.img_win

    # ЗАПОМНЕННОЕ СООБЩЕНИЕ
    async with state.proxy() as data:
        msg2 = data['msg_content']

        # КАЗИНО СТАВКА НА ВСЕ ДЕНЬГИ
        if amount.lower() in ['all', 'все', 'всё', 'вабанк', 'ва-банк']:
            amount = balance_user
        else:
            try:
                amount = int(amount)
            except:
                await msg2.edit_media(types.InputMediaPhoto(var.img_error))
                await msg2.edit_caption(f'''❌ Ошибка. Укажите сумму 🍃''', reply_markup = ikbCasino)
                return


        # ОШИБКА: СУММА МЕНЬШЕ 1$
        if amount < 1:
            await msg2.edit_media(types.InputMediaPhoto(var.img_error))
            await msg2.edit_caption(f'''❌ Ошибка. Укажите сумму больше 1$ 🍃''', reply_markup = ikbCasino)
            return

        # ОШИБКА: НЕДОСТАТОЧНО СРЕДСТВ
        elif balance_user < amount:
            await msg2.edit_media(types.InputMediaPhoto(var.img_error))
            await msg2.edit_caption(f'''❌ У вас недостаточно средств! 🍃
        
<em>Ваша ставка: {msg.text}$</em>

💰 Баланс: {balance_user}$
    ''', reply_markup = ikbCasino)
            return

        else:
            losee = random.randint(1, 4)

            if number > 700:
                add = amount
                text = f'🙂 Вы выиграли: {int(add)}$ 🍃 (x2)'
                cursor.execute(f'UPDATE game SET xp=xp+{random.randint(5, 20)} WHERE id={msg.from_user.id}')
                media = win
            
            elif number <= 30:
                add = amount * 5
                text = f'😄 Вы выиграли: {int(add)}$ 🍃 (x5)'
                cursor.execute(f'UPDATE game SET xp=xp+{random.randint(20, 100)} WHERE id={msg.from_user.id}')
                media = win
            
            elif number <= 5:
                add = amount * 50
                text = f'🤩 Вы выиграли: {int(add)}$ 🍃 (x50)'
                cursor.execute(f'UPDATE game SET xp=xp+{random.randint(100, 500)} WHERE id={msg.from_user.id}')
                media = win
            
            elif losee == 1:
                add = -(amount * 0.75)
                text = f'😯 Вы проиграли: {int(add)}$ 🍃 (x0.25)'
                media = lose
            
            elif losee == 2:
                add = -(amount * 0.5)
                text = f'😔 Вы проиграли: {int(add)}$ 🍃 (x0.50)'
                media = lose
            
            elif losee == 3:
                add = -(amount * 0.25)
                text = f'😕 Вы проиграли: {int(add)}$ 🍃 (x0.75)'
                media = lose
            
            elif losee == 4:
                add = -amount
                text = f'❌ Вы проиграли: {int(add)}$ 🍃 (x0)'
                media = lose


        cursor.execute(f"UPDATE game SET cash = cash + {int(add)} WHERE id = {msg.from_user.id}")
        connection.commit()
        balance_upd = functions.get_balance(msg)



        await msg2.edit_media(types.InputMediaPhoto(media = media))
        await msg2.edit_caption(f'''
{text}

<em>Ваша ставка: {msg.text}$</em>

💰 Баланс: {balance_user}$ -> <strong>{balance_upd}$</strong>
        ''', reply_markup = ikbCasino)



def reg_game_casino(dp: Dispatcher):
    print('[COGS] game/casino - is connected')
    dp.register_callback_query_handler(game_casino, Text('game_casino'))
    dp.register_message_handler(game_casino_state, state = FSMCasino.bet)