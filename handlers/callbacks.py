from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.create_user import CreateUser

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
async def handle_continue(callback: CallbackQuery):
    await callback.message.answer("Продолжаем путь 🚶🏻‍♂️")
    await callback.answer()