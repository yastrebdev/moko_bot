from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_phone_keyboard():
    # Создаем обычную клавиатуру с запросом контакта
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )