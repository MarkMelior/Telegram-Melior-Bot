from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType, LabeledPrice
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
import var
import functions
from SQL import cursor, connection
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State



# SQL БАЗА ДАННЫХ
# cursor.execute( "DROP TABLE  IF EXISTS course_neural" )
cursor.execute("""CREATE TABLE IF NOT EXISTS course_neural (
    id BIGINT,
    lesson1 BOOLEAN DEFAULT false,
    lesson2 BOOLEAN DEFAULT false,
    lesson3 BOOLEAN DEFAULT false,
    lesson4 BOOLEAN DEFAULT false,
    lesson5 BOOLEAN DEFAULT false,
    lesson6 BOOLEAN DEFAULT false,
    lesson7 BOOLEAN DEFAULT false,
    lesson8 BOOLEAN DEFAULT false,
    lesson9 BOOLEAN DEFAULT false
    );""")
connection.commit()



# ФУНКЦИИ
# добавляет пользователя в бд курса
def add_course(call):
    cursor.execute(f"SELECT id FROM course_neural WHERE id = {call.from_user.id}")
    if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO course_neural(id) VALUES ({call.from_user.id})")
        connection.commit()

# проверка, есть ли пользователь в бд
def check_course(call):
    cursor.execute(f"SELECT id FROM course_neural WHERE id = {call.from_user.id}")
    return cursor.fetchone()

# проверка, пройде ли урок
def check_lesson(call, lesson):
    cursor.execute(f"SELECT {lesson} FROM course_neural WHERE id = {call.from_user.id}")
    return cursor.fetchone()[0]

# количество пройденных уроков
def lesson_count(call):
    cursor.execute(f"SELECT * FROM course_neural WHERE id = {call.from_user.id}")
    results = cursor.fetchone()
    i = 0
    for result in results[1:]:
        if result == False:
            return i
        i += 1

# описание
def close_lesson_desc(call, chapter, lesson):
    text = f'''
<strong>[ Глава {chapter} / Урок {lesson} ]</strong>

❌ Урок ещё не доступен, ты не прошёл {lesson_count(call) + 1} урок!
    '''
    return text

# шаблон course_neural_more
async def course_more(call, data, text, img = None, ikb = None):
    if call.data == data:
        if img == None:
            img = var.img_neural
        if ikb == None:
            ikb = courseBack_ikb
        await call.message.delete()
        await call.message.answer_photo(img, caption = text, reply_markup = ikb)


# добавить главу
async def add_chapter(call, lesson_list):
    chapter_count = 0
    lesson_count = 0
    for lesson in lesson_list:
        chapter_count += 1

        ikbList1 = ''
        for i in lesson[0]:
            lesson_count += 1
            ikbList1 += f"[InlineKeyboardButton('Урок {lesson_count}. {i[0]}', callback_data = 'neural_lesson{lesson_count}')],"

            ikbList2 = ''
            if call.data == f'neural_lesson{str(lesson_count)}':
                from bot import bot

                if lesson_count - 1 != 0:
                    if check_lesson(call, f'lesson{str(int(lesson_count) - 1)}') == False:
                        # возврат к главам
                        BackChapter_ikb = InlineKeyboardMarkup(inline_keyboard = [
                            ])
                        functions.ButtonBack(BackChapter_ikb, f'neural_chapter{str(chapter_count)}')
                        
                        await call.message.delete()
                        await call.message.answer_photo(var.img_close, caption = close_lesson_desc(call, chapter_count, lesson_count), reply_markup = BackChapter_ikb)

                        return


                for n in lesson[0][0][3]:
                    ikbList2 += f'[InlineKeyboardButton("{n[0]}", url = "{n[1]}")],'

                finish_lesson = ''

                cursor.execute(f"SELECT lesson{str(lesson_count)} FROM course_neural WHERE id = {call.from_user.id}")
                if cursor.fetchone()[0] != True:
                    finish_lesson = f"[InlineKeyboardButton('✅ Завершить урок', callback_data = 'neural_lesson_finish{lesson_count}')]"

                ikb = eval(f"""InlineKeyboardMarkup(inline_keyboard = [
                    {ikbList2}
                    {finish_lesson}
                ])""")
                functions.ButtonBack(ikb, f'neural_chapter{str(chapter_count)}')

                await call.message.delete()      
                await bot.send_video(chat_id = call.message.chat.id, caption = f'<strong>[ Глава {chapter_count} / Урок {lesson_count} ]</strong> — {i[0]} \n \n' + i[2], video = i[1], reply_markup = ikb)
                
            
            if call.data == f'neural_lesson_finish{str(lesson_count)}':
                cursor.execute(f'UPDATE course_neural SET lesson{str(lesson_count)} = True WHERE id = {call.from_user.id}')
                connection.commit()
                
                await call.message.delete()
                await call.message.answer_photo(var.img_lesson_finish, caption = f'✅ <strong>[ Глава {chapter_count} / Урок {lesson_count} ]</strong> — «{i[0]}» успешно пройден! \n \n Так держать :D', reply_markup = courseFinish_ikb)


        if call.data == f'neural_chapter{str(chapter_count)}':
            ikb = eval(f"""InlineKeyboardMarkup(inline_keyboard=[
                {ikbList1}
            ])""")
            functions.ButtonBack(ikb, 'course_neural')
            
            await call.message.delete()
            await call.message.answer_photo(var.img_neural, caption = f'<strong>[ Глава {chapter_count} ]</strong> - ' + lesson[1], reply_markup = ikb)



# ГЛАВНАЯ СТРАНИЦА
async def course_neural(call: types.CallbackQuery):
    ikb = courseNeural_ikb
    desc = courseNeural_desc
    # если приобрёл курс
    if check_course(call) != None:
        list1 = []
        list2 = []
        
        list1.append(['Установка на компьютер', var.video_null, '''ОН САМЫЙ ПРОСТОЙ И ДЭФОЛТНЫЙ''', [['Python Release 3.10.6', 'https://www.python.org/downloads/release/python-3106/'], ['Git', 'https://git-scm.com/'], ['Stable Diffusion UI', 'https://github.com/AUTOMATIC1111/stable-diffusion-webui']]])
        list1.append(['Установка на Google Collab', var.video_null, 'Этот урок посложнее, но прикольный тоже', [['Colaboratory', 'https://colab.research.google.com/github/TheLastBen/fast-stable-diffusion/blob/main/fast_stable_diffusion_AUTOMATIC1111.ipynb']]])
        list1.append(['lesson_title3', var.video_null, 'Этот урок ещё более сложный. \n \n  Нужно постараться прям', [['Файл 1', 'https://telegra.ph/Course-FAQ-04-23']]])
        list2.append(['lesson_title4', var.video_null, 'Этот урок ещё более сложный. \n \n  Нужно постараться прям', [['Hello 2', 'https://telegra.ph/Course-FAQ-04-23'], ['Hi 2', 'https://telegra.ph/Course-FAQ-04-23']]])
        lesson_list = [[list1, 'Установка, Google Collab'], [list2, 'Генерация изображения по запросу (txt2img)']]
        
        await add_chapter(call, lesson_list)

        chapter_count = 0
        test = ''
        for lesson in lesson_list:
            chapter_count += 1
            test += f"[InlineKeyboardButton('[Глава {chapter_count}] - {str(lesson[1])}', callback_data = 'neural_chapter{str(chapter_count)}')],"

        ikb = eval(f"""InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('👾 О профессии', callback_data = 'inf_neural_profession'), InlineKeyboardButton('❓ FAQ', url='https://telegra.ph/Course-FAQ-04-23')],
            {test}
        ])""")
        functions.ButtonBack(ikb)

        desc = f'''
👾 Добро пожаловать на курс по Stable Diffusion. Спасибо за покупку!

✅ Ты сейчас на {lesson_count(call) + 1} уроке
        '''

    if call.data == 'course_neural':
        await call.message.delete()
        await call.message.answer_photo(photo = var.img_neural, caption = desc, reply_markup = ikb)

    if call.data == 'course_neural_pay':
        await call.message.answer_photo(photo = var.img_neural, caption = desc, reply_markup = ikb)






courseNeural_desc = f'👾 Курс <strong>«Neural Dreaming 2023»</strong> от Mark Melior \n\n<span class="tg-spoiler">🎁 Подписчикам <strong>«Melior Exclusive»</strong> скидка: <strong>-{var.exclusive_discount}₽</strong></span>\n \nВ рамках курса вы научитесь работать в Stable Diffusion — это нейросеть для создания изображений по текстовому описанию\n \nПосле прохождения курса вы с лёгкостью сможете воплотить любую картинку в реальность. Единственное ограничение — ваша фантазия'

# КЛАВИАТУРЫ
# если не приобрёл
courseNeural_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('👾 О профессии', callback_data = 'inf_neural_profession'), InlineKeyboardButton('❓ FAQ', url='https://telegra.ph/Course-FAQ-04-23')],
    [InlineKeyboardButton('Кому подойдёт?', callback_data = 'inf_neural_who')],
    [InlineKeyboardButton('Чему вы научитесь?', callback_data = 'inf_neural_learn')],
    # [InlineKeyboardButton('Содержание курса', callback_data = 'inf_neural_content')],
    [InlineKeyboardButton('Как проходит обучение?', callback_data = 'inf_neural_training')],
    [InlineKeyboardButton('❌ Курс недоступен', callback_data = 'nope')],
    # [InlineKeyboardButton('🤑 Приобрести курс', callback_data = 'course_neural_buy')],
])
functions.ButtonBack(courseNeural_ikb)

# кнопка назад на главную
courseBack_ikb = InlineKeyboardMarkup(inline_keyboard = [

])
functions.ButtonBack(courseBack_ikb, 'course_neural')

# оплата
coursePay_ikb = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(f"💵 Перейти к оплате", pay = True)]
])
functions.ButtonBack(coursePay_ikb)

# кнопка после завершения курса
courseFinish_ikb = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton('🧩 Вернуться к главам', callback_data = 'course_neural')]
])

# кнопка для course_more(call, 'inf_neural_training'...)
inf_neural_training_ikb = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(f"⭕️ Пробный урок", callback_data='course_neural_test')]
])
functions.ButtonBack(inf_neural_training_ikb, 'course_neural')


# О КУРСЕ
async def course_neural_more(call: types.CallbackQuery):

    await course_more(call, 'inf_neural_profession', '<strong>👾 О профессии</strong>' \
    '\n \nГенерация изображений в Stable Diffusion — это уникальная и востребованная профессия в области искусственного интеллекта и компьютерной графики. Если вы хотите стать экспертом в этой области, то курс по Stable Diffusion может помочь вам достичь ваших целей' \
    '\n \nСегодня многие компании и организации нуждаются в высококачественных и уникальных изображениях для своих проектов, таких как рекламные баннеры, иллюстрации, анимация и даже фильмы' \
    '\n \n<i>✅ Таким образом, профессия генератора изображений в Stable Diffusion — это многообещающая и перспективная карьера, которая может принести вам успех и прибыль в сфере искусственного интеллекта и компьютерной графики</i>')
    
    await course_more(call, 'inf_neural_who', '🧐 <strong>Кому подойдёт?</strong>' \
    '\n \n- Для профессионалов в области компьютерной графики, машинного обучения, искусственного интеллекта, а также для начинающих, которые хотят изучить новую и перспективную область'\
    '\n \n- Курс будет полезен для тех, кто работает в сфере маркетинга, рекламы, разработки игр, фильмов, анимации и других областей, где требуется создание качественных и уникальных изображений'\
    '\n \n- Кроме того, этот курс может быть полезен для студентов, аспирантов и научных работников, которые хотят изучить новые технологии и методы в области компьютерной графики и машинного обучения'\
    '\n \n<i>✅ Таким образом, курс по Stable Diffusion подойдет всем, кто хочет изучить новую и перспективную область искусственного интеллекта и компьютерной графики, и достичь успеха в своей карьере</i>')
    
    await course_more(call, 'inf_neural_learn', '⚡️ <strong>Чему вы научитесь?</strong>'\
    '\n \n- Генерировать высококачественные изображения любой сложности, используя технологии искусственного интеллекта'\
    '\n \n- Грамотно составлять prompt, то есть текстовые описания для генерации изображений, которые позволят вам получать нужные результаты'\
    '\n \n- Вы также подробно изучите интерфейс Stable Diffusion, чтобы получать наилучшие результаты'\
    '\n \n- Кроме того, на курсе вы научитесь правильной технике Upscale, то есть методам увеличения разрешения изображений без потери качества'\
    '\n \n- Вы также научитесь генерировать горячий 18+ материал, если эта тема для вас актуальна'\
    '\n \n<i>✅ Таким образом, вы научитесь обрабатывать любые изображения любой сложности, используя различные техники и инструменты, которые вы изучите на курсе</i>', var.img_neural_work)
    
    
    # await course_more(call, 'inf_neural_content', '🧩 <strong>Содержание курса</strong> \n \nОбучение проходит в телеграмм боте, который обеспечивает доступ к курсу и помогает вам изучать материал по шагам \n \nВы будете получать информацию о каждом уроке, выполнять практические задания и получать обратную связь от преподавателя \n \nБот также предоставляет возможность общения с другими студентами курса и задавать вопросы преподавателю')
    # кнопка назад на главную
    await course_more(call, 'inf_neural_training', '🎓 <strong>Как проходит обучение?</strong> \n \nОбучение проходит в телеграмм боте, который обеспечивает доступ к курсу и помогает вам изучать материал по шагам. Вы также получите возможность задать вопросы и обсудить уроки с другими участниками курса в чате' \
    '\n \nЧат-бот будет выдавать вам доступ к новым урокам по мере прохождения предыдущих. Таким образом, вы сможете проходить обучение в удобном для вас темпе, не перегружаясь информацией и постепенно углубляя свои знания и навыки' \
    '\n \nКаждый урок будет содержать подробные объяснения, примеры и практические задания, которые помогут вам лучше понимать тему и закреплять полученные знания на практике' \
    '\n \nКроме того, на курсе будут представлены дополнительные материалы и ресурсы, которые помогут вам углубить свои знания в области Stable Diffusion', ikb = inf_neural_training_ikb)



# ОПЛАТА
async def course_neural_buy(call: types.CallbackQuery, state: FSMContext):
    # ЗАПОМНИЛИ СООБЩЕНИЕ
    async with state.proxy() as data:
        data['state_pay'] = 'neural_course'

    cursor.execute(f"SELECT id FROM course_neural WHERE id = {call.from_user.id}")
    if cursor.fetchone() != None:
        await call.message.edit_media(types.InputMediaPhoto(var.img_error))
        await call.message.edit_caption(f'Ты уже приобрёл курс!', reply_markup = courseBack_ikb)
        return
    
    from bot import bot, config
    await call.message.delete()

    ex_discount = types.LabeledPrice(label='Скидка подписчика Melior Exclusive', amount = 0)
    cursor.execute(f"SELECT id FROM users WHERE exclusive IS NOT NULL AND id = {call.from_user.id}")
    if cursor.fetchone() != None:
        ex_discount = types.LabeledPrice(label='Скидка подписчика Melior Exclusive', amount = -var.exclusive_discount * 100)

    await bot.send_invoice(call.message.chat.id,
                            title = "Оплата курса «Neural Dreaming 2023»",
                            description = '🍃 Я знаю, что это может показаться дорогим, но поверь мне, это стоит каждой копейки \n \n📌 Как говорится, "купи дешево — купи дважды", а я обещаю, что после прохождения курса ты никогда не пожалеешь о своей инвестиции!',
                            provider_token = config.tg_bot.paymaster,
                            currency = "rub",
                            photo_url = var.img_pay,
                            prices = [
                                types.LabeledPrice(
                                    label = "Доступ к курсу",
                                    amount = var.neural_price * 100
                                ),
                                types.LabeledPrice(
                                    label = "Ваша скидка",
                                    amount = -var.neural_discount * 100
                                ),
                                ex_discount
                            ],
                            max_tip_amount = 2000 * 100,
                            suggested_tip_amounts = [50 * 100, 100 * 100, 200 * 100, 300 * 100],
                            photo_height = 1080,
                            photo_width = 1440,
                            is_flexible = False,
                            reply_markup = coursePay_ikb,
                            start_parameter = "neural-cource-app",
                            payload = {"payload_key": "testt-invoice-payload-neural"}
                            )



async def course_neural_test(call: types.CallbackQuery):
    from bot import bot
    await call.message.delete()      
    await bot.send_video(chat_id = call.message.chat.id, caption = f'<strong>[ Глава 2 / Урок 4 ]</strong> — Крутой урок \n \nОписание', video = var.video_null, reply_markup = courseBack_ikb)





# ПОДКЛЮЧЕНИЕ
def reg_neural(dp: Dispatcher):
    print('[COGS] neural - is connected')
    dp.register_callback_query_handler(course_neural, lambda c: c.data.startswith(('neural_lesson', 'neural_chapter')) or c.data in ['course_neural'])
    dp.register_callback_query_handler(course_neural_more, lambda c: c.data.startswith('inf_neural'))
    dp.register_callback_query_handler(course_neural_buy, Text(['course_neural_buy']))

    dp.register_callback_query_handler(course_neural_test, Text(['course_neural_test']))