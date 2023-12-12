from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import functions

add_cash = 750
add_xp = 80

ex_chat_id = "-1001886901797"
live_chat_id = "-1001864924460"
work_chat_id = "-1001965190255"
ex_chat_link = 'https://t.me/+Trn4KY9Q7OkyMjcy'

price_exclusive_rub = 800
price_neural_rub = 5000

neural_price = 4999
neural_discount = 2000
exclusive_discount = 500

'''IMAGE'''
############################
# game
img_game = 'AgACAgIAAxkBAAPPZD8KxUjgSrLgtBTN9_Ni9OQd4wUAAm_MMRtigflJftb-orLw2GgBAAMCAAN5AAMvBA'
img_profile = 'AgACAgIAAxkBAAIBH2Q_FEpj6oLPPs8rh8Kza52dRmrwAAKRzDEbYoH5Sa0LelTU3lZlAQADAgADeQADLwQ'
img_casino = 'AgACAgIAAxkBAAPsZD8ND-axxSU0mk7_eVzQFErcudUAAnfMMRtigflJcR6yQ-rkOJABAAMCAAN5AAMvBA'
img_lose = 'AgACAgIAAxkBAAICXWRABSUL0MDWxL603EGyeM2nVGW0AAItyDEbzYkAAUoAAb_KG2kJDE0BAAMCAAN5AAMvBA'
img_win = 'AgACAgIAAxkBAAICX2RABXuhCUGXLdSSrNJ55asIHBx7AAIuyDEbzYkAAUr0psdzqBigqgEAAwIAA3kAAy8E'
img_bonus_yes = 'AgACAgIAAxkBAAIBP2Q_s12OT4Nz7XuEe7btBfFioXjpAAJ9yjEbzYn4SWG07Jl9wU8UAQADAgADeQADLwQ'
img_bonus_no = 'AgACAgIAAxkBAAIBQWQ_s2A25xwF-YMR79MgaJUfXPSrAAJ-yjEbzYn4SUGQsOKGSiNxAQADAgADeQADLwQ'
img_buyed = 'AgACAgIAAxkBAAIN_mRP26pv7HaWa8V5MRIu2EcS-IUSAAIlyjEbNfR4SiAxy5KKITsPAQADAgADeQADLwQ'
img_sell = 'AgACAgIAAxkBAAIP9GRP9QX7GNJ2uLSnK7yQP_ldShx9AAL1xzEbNfSASh3Xv-ccXInuAQADAgADeQADLwQ'
img_shop_business = 'AgACAgIAAxkBAAIODWRP3IB-tSitKevl_fDsWPLKL-n7AAInyjEbNfR4Sp4xrMU095ljAQADAgADeQADLwQ'
img_shop_farm = 'AgACAgIAAxkBAAIOD2RP3IQxjUpniZhHzGxhz6-o6NM0AAIoyjEbNfR4SlKnBZx67EjdAQADAgADeQADLwQ'
img_job = 'AgACAgIAAxkBAAIYkmRU0Im_26pKjltfQ8Pcjb3bEaxyAAKMyzEb-ROoShG-liYpC4CGAQADAgADeQADLwQ'
img_income = 'AgACAgIAAxkBAAIZAmRU1iZsr5158Xx889nPuJ2ZYFc0AAKdyzEb-ROoShmH3zB6BkohAQADAgADeQADLwQ'

# neural
img_neural = 'AgACAgIAAxkBAAIEuGRCNDAqYKJihk6r7CBBGkThseTlAAITxjEbYGcRSuAtOUTMP4DIAQADAgADeQADLwQ'
img_neural_work = 'AgACAgIAAxkBAAIH5GRFmvecu8unNJ8TttfoHpyQA9W6AALlzTEbRr8wSmikpIdtQz0UAQADAgADeQADLwQ'

# course
img_lesson_finish = 'AgACAgIAAxkBAAIGYGRFM5h_ubRIBxvL1eFqlDbWmciyAAJZzjEbRr8oSge07G4SnB6ZAQADAgADeQADLwQ'

# main
img_start = 'AgACAgIAAxkBAAIHHGRFaq1X1VElhT-ZIogFiIeAY8WaAAJTzzEbRr8oSveco_sh5WnnAQADAgADeQADLwQ'
img_discord = 'AgACAgIAAxkBAAMuZDsO6K-4ByaPNqzZ-Ho7icNeZZAAAsjNMRsCq9lJltxsZBdx2H4BAAMCAAN5AAMvBA'
img_ex = 'AgACAgIAAxkBAAID42RAbtPW13UBAAF5tKeWhORKwO5A7QACCsoxG82JAAFK0hi-Xo2E3WsBAAMCAAN5AAMvBA'
img_accept_member = 'AgACAgIAAxkBAAIIaGRKtwrD2OxJDBpn-k6xGupZPrkGAAKCyjEbeglQSvcnkmbUgKaYAQADAgADeQADLwQ'
img_cancel_member = 'AgACAgIAAxkBAAIIamRKtw-sEsx1llmLA_j7b9CK6P5sAAKDyjEbeglQSkRARvuqeSgYAQADAgADeQADLwQ'
img_thanks = 'AgACAgIAAxkBAAICimRAEA7pGcArJ31rqPtWt_-2j4CUAAJeyDEbzYkAAUq4r-MjHIOKXgEAAwIAA3kAAy8E'
img_pay = 'https://downloader.disk.yandex.ru/preview/637e35d9c710f5625e49455ea4a83b8f5bdac741e72ac086330a73e8863ac702/6445a1d1/u5-fRkmZdTrA4LdkJNOyXhy_Z-pzEu1i3Vpp2xCPhbKHQACxqRttSsU0f4dU34NSY2drHbz37X-ep4al9SGCCw%3D%3D?uid=0&filename=pay.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048'
img_endEx = 'AgACAgIAAxkBAAIIVGRIIM0JDUxmcWP672VTt6_NvpGVAAKEyjEbEDtBStpFujBipAvAAQADAgADeQADLwQ'
img_sub_live = 'AgACAgIAAxkBAAIKVmROnuLH8WRYi91Ith3I1k_ug1vPAALIyDEbBrJ4SrS5Szwwb-pBAQADAgADeQADLwQ'
img_you_nosub = 'AgACAgIAAxkBAAIKbGROo-AnnAOZJ-zvJiltofe_m1fAAALYyDEbBrJ4Sg5yYf9P5Ty5AQADAgADeQADLwQ'
img_you_sub = 'AgACAgIAAxkBAAIKbmROo-IbNvKQSvZsoIPf9nhy6i--AALZyDEbBrJ4SlVB4qxbgR0eAQADAgADeQADLwQ'
img_additional = 'AgACAgIAAxkBAAIKWWROoLQBw42Eg91lgRwtiiew2I9lAALOyDEbBrJ4Sry4KUL-d6_1AQADAgADeQADLwQ'

# other
img_close = 'AgACAgIAAxkBAAIFYmRE1BFU1f6rncTyJcn4qh_qmrQuAAIUzTEbRr8oSibRkkUZV1YgAQADAgADeQADLwQ'
img_error = 'AgACAgIAAxkBAAICW2RABMMxtKD3F1HpOLsHlSStk0diAAIpyDEbzYkAAUqGo02xnBLw3AEAAwIAA3kAAy8E'
img_timeout = 'AgACAgIAAxkBAAICWGRABIJs5FOlKygT9U8PeLnuzPI7AAIoyDEbzYkAAUqLFKlKKvcRrwEAAwIAA3kAAy8E'
video_null = 'BAACAgIAAxkBAAIFj2RE3DSe7ZDQORkcfr-l20dlAV03AAKqJwACRr8oSslYKvggFMJ3LwQ'
############################



ikbClose = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton('❌ Скрыть сообщение', callback_data = 'close_msg')]
])







StartMainDesc = """
✨ Привет! Это бета-версия бота, который находится на стадии разработки. Функционал будет расти по мере того, как я буду развивать его

⭕️ <i>Сообщайте обо всех замеченных ошибках или недочётах: @MarkMelior</i>
"""
def ikb_Main(call):
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('💎 Подписка Melior Work', callback_data = 'exclusive')],
        [InlineKeyboardButton('⚡️ Возможности бота', callback_data = 'additional')],
        [InlineKeyboardButton('👾 Neural Dreaming 2023', callback_data = 'course_neural')],
        [InlineKeyboardButton('🌌 Gesway', callback_data = 'gesway')] if call.from_user.id == 997065671 else '',
        [InlineKeyboardButton('🤑 [Игра] Экономика', callback_data = 'game')] if functions.have_ex(call) == True else '',
    ])
    return ikb