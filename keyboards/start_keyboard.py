from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✍🏻 Вести дневник пути", callback_data="start_diary")
    )
    builder.row(
        InlineKeyboardButton(text="❓ Узнать обо мне больше", callback_data="about_bot")
    )
    builder.row(
        InlineKeyboardButton(text="🚶🏻 Продолжить свой путь", callback_data="continue")
    )
    return builder.as_markup()