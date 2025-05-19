from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from db.database import find_user_by_tg_id
from states.create_user import CreateUser, pilgrim
from db.database import create_user, SessionLocal


router = Router()


@router.callback_query(F.data == "start_diary")
async def handle_start_diary(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    user = await find_user_by_tg_id(tg_id)

    if not user:
        await state.set_state(CreateUser.username)
        await callback.message.answer(
            "Ты сделал правильный выбор, я помогу тебе узнать себя лучше ✨\n\n"
            "Давай немного познакомимся. Напиши как я буду к тебе обращаться?"
        )
        await callback.answer()
    else:
        await callback.message.answer(
            f"Привет {user.username}!\n"
            "Рад что ты вернулся."
        )


@router.callback_query(F.data == "about_bot")
async def handle_about_bot(callback: CallbackQuery):
    await callback.message.answer("Я — бот-проводник по твоему внутреннему пути ✨")
    await callback.answer()


from aiogram.types import CallbackQuery

@router.callback_query(lambda c: c.data.startswith("tz:"), CreateUser.tz)
async def get_timezone(callback: CallbackQuery, state: FSMContext):
    tz = callback.data.split(":", 1)[1]
    await state.update_data(tz=tz)

    data = await state.get_data()

    try:
        async with SessionLocal() as db:
            user = await create_user(
                db,
                username=data['username'],
                birth_date=data['birth_date'],
                phone=data['phone'],
                interests=data['interests'],
                telegram_id=str(callback.from_user.id),
                tz=data['tz']
            )
            await callback.message.answer(
                f'Спасибо! Давай проверим:\n\n'
                f'Ты: {user.username}\n'
                f'Дата: {user.birth_date}\n'
                f'Номер: {user.phone}\n'
                f'Интересы: {", ".join(user.interests)}\n'
                f'Часовой пояс: {data["tz"]}'
            )
    except Exception as e:
        print(f'Ошибка при сохранении: {e}')

    await state.clear()
    await callback.answer()