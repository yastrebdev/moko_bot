from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def timezone_keyboard():
    timezones = [
        ("Москва", "Europe/Moscow"),
        ("Калининград", "Europe/Kaliningrad"),
        ("Новосибирск", "Asia/Novosibirsk"),
        ("Владивосток", "Asia/Vladivostok"),
    ]
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"tz:{tz}")] for name, tz in timezones]
    return InlineKeyboardMarkup(inline_keyboard=buttons)