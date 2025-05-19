from aiogram import html, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards import get_start_keyboard

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    name = message.from_user.first_name

    welcome_text = (
        f"Привет, {html.bold(name)}! 👋🏻 Я Moko, твой карманный дух 👾\n\n"
        "Неважно, знаешь ли ты, куда идёшь. Главное — идти и замечать. Я буду твоим дневником, который не забудет.\n\n"
        "Выбери действие 👇🏻"
    )

    await message.answer(welcome_text, reply_markup=get_start_keyboard())