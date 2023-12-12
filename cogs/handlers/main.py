from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
import var
from aiogram.dispatcher import FSMContext
import functions


async def start(msg: types.Message):
    await msg.answer_photo(var.img_start, var.StartMainDesc, reply_markup = var.ikb_Main(msg))

async def start_call(call: types.CallbackQuery):
    if call.data == 'start':
        await call.message.delete()

    if call.data == 'start_save':
        from bot import bot
        await bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id = call.message.message_id)

    await call.message.answer_photo(var.img_start, var.StartMainDesc, reply_markup = var.ikb_Main(call))




additional_nosub_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('✅ Проверить подписку', callback_data = 'chech_sub')],
])
functions.ButtonBack(additional_nosub_ikb)

additional_sub_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('📌 Возможности бота', callback_data = 'additional')]
])
functions.ButtonBack(additional_sub_ikb)

additional_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('🤑 [Игра] Экономика', callback_data = 'game')],
    [InlineKeyboardButton('❇️ [Нейросеть] ChatGPT', callback_data = 'chatgpt')],
    # [InlineKeyboardButton('👾 [Фото] Демотиватор', callback_data = 'demotivator')],
    # [InlineKeyboardButton('🔉 [Озвучка] Сообщения', callback_data = 'voiceover')],
    # [InlineKeyboardButton('❤️ Онлайн знакомства', callback_data = 'online_dating')],
])
functions.ButtonBack(additional_ikb)


async def additional(call: types.CallbackQuery):
    from bot import bot
    user_channel_status = await bot.get_chat_member(chat_id = var.live_chat_id, user_id = call.from_user.id)
    if user_channel_status["status"] == 'left':
        await call.message.delete()
        await call.message.answer_photo(var.img_sub_live, '✨ Чтобы получить доступ к возможностям бота — нужно быть подписанным на @MeliorLive', reply_markup = additional_nosub_ikb)
        return
    
    await call.message.delete()
    await call.message.answer_photo(var.img_additional, '✨ Спасибо, что подписан на @MeliorLive \n\n <i>В будущем возможности бота будет расти</i>', reply_markup = additional_ikb)


async def chech_sub(call: types.CallbackQuery):
    from bot import bot
    user_channel_status = await bot.get_chat_member(chat_id = var.live_chat_id, user_id = call.from_user.id)
    if user_channel_status["status"] == 'left':
        await call.message.edit_media(types.InputMediaPhoto(var.img_you_nosub))
        await call.message.edit_caption(f'❌ Вы не подписаны на @MeliorLive', reply_markup = additional_nosub_ikb)
        return
    
    await call.message.edit_media(types.InputMediaPhoto(var.img_you_sub))
    await call.message.edit_caption(f'✅ Спасибо за подписку! \n\nТеперь для тебя доступны возможности бота', reply_markup = additional_sub_ikb)









# ! Техническая
# Фото -> ID фото
async def handle_photo(msg: types.Message):
    id_photo = msg.photo[-1].file_id
    user_id = msg.from_user.id
    current_chat_id = msg.chat.id
    reply_message_id = msg.reply_to_message.message_id if msg.reply_to_message else None
    await msg.reply( f'Photo ID: <code>{id_photo}</code>\n\nUser ID: <code>{user_id}</code>\n\nCurrent chat ID: <code>{current_chat_id}</code>\n\nReply message ID: <code>{reply_message_id}</code>', protect_content = False )

async def video_file_id(message: types.Message):
    await message.reply(message.video.file_id, protect_content = False)

# Удалять все сообщения, которые не попали в handlers
async def all_callback(msg: types.Message):
    await msg.delete()

async def callback_nope(_):
    pass




def reg_main(dp: Dispatcher):
    dp.register_message_handler(start, commands = ['start', 'help'])
    dp.register_callback_query_handler(start_call, Text(['start', 'start_save']))
    dp.register_callback_query_handler(additional, Text('additional'))
    dp.register_callback_query_handler(chech_sub, Text('chech_sub'))

    dp.register_callback_query_handler(callback_nope, Text(['nope', 'null', 'none']))
    dp.register_message_handler(handle_photo, content_types=['photo'])
    dp.register_message_handler(video_file_id, content_types=['video'])
    dp.register_message_handler(all_callback)