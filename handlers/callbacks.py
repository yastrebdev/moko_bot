from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.contact_keyboard import get_phone_keyboard
from states.create_user import CreateUser
from states.login_user import LoginUser

router = Router()


@router.callback_query(F.data == "start_diary")
async def handle_start_diary(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CreateUser.username)
    await callback.message.answer(
        "Ты сделал правильный выбор, я помогу тебе узнать себя лучше ✨\n\n"
        "Давай немного познакомимся. Как я буду к тебе обращаться?"
    )
    await callback.answer()


@router.callback_query(F.data == "about_bot")
async def handle_about_bot(callback: CallbackQuery):
    await callback.message.answer("Я — бот-проводник по твоему внутреннему пути ✨")
    await callback.answer()


@router.callback_query(F.data == "continue")
async def handle_continue(callback: CallbackQuery, state: FSMContext):
    # Объединяем все сообщения в одну строку
    message_text = (
        "Продолжаем путь 🚶🏻‍♂️\n"
        "Для входа отправьте номер телефона через кнопку ниже:"
    )

    await callback.message.answer(
        message_text,
        reply_markup=get_phone_keyboard(),  # Убедись, что эта переменная определена
    )
    await state.set_state(LoginUser.phone)
    await callback.answer()