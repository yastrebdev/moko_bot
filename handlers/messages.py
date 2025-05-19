import re
from datetime import datetime, date, timedelta

from aiogram import html, Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.timezone_keyboard import timezone_keyboard
from states.create_user import CreateUser

router = Router()


@router.message(CreateUser.username)
async def get_username(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(
            'Я понимаю что творчески подходишь к задаче,\n'
            'но я жду просто текст с именем или прозвищем 🫂'
        )
    else:
        await state.update_data(username=message.text)
        await message.answer(f'Хорошо, я буду называть тебя {html.bold(message.text)}!')

        await message.answer(
            f'{html.bold("Введи дату рождения в формате - 08.09.1994")}\n\n'
            'Мне нужна эта информация для подбора более подходящих вопросов\n\n'
            f'Если не хотите указывать дату, просто отправьте {html.code(0)}',
        )
        await state.set_state(CreateUser.birth_date)


@router.message(CreateUser.birth_date)
async def get_birth_date(message: types.Message, state: FSMContext):
    text = message.text.strip()

    if text == "0":
        birth_date = date.today() - timedelta(days=365*17)
        await state.update_data(birth_date=birth_date)
        await message.answer(f"Запомнил! Твоя дата рождения — {birth_date.strftime('%d.%m.%Y')}.")
    else:
        text = re.sub(r'[-/,]', '.', text)

        parts = text.split('.')
        if len(parts) != 3:
            await message.answer("Пожалуйста, введи дату в формате ДД.ММ.ГГГГ")
            return

        day, month, year = parts

        if len(day) == 1 and day.isdigit():
            day = '0' + day
        if len(month) == 1 and month.isdigit():
            month = '0' + month

        if not (year.isdigit() and len(year) == 4):
            await message.answer("Год должен быть из 4 цифр, например 1994")
            return

        try:
            birth_date = datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y").date()
        except ValueError:
            await message.answer("Похоже, дата некорректна. Попробуй еще раз в формате ДД.ММ.ГГГГ")
            return

        await state.update_data(birth_date=birth_date)
        await message.answer(f"Запомнил! Твоя дата рождения — {birth_date.strftime('%d.%m.%Y')}.")

    await message.answer(
        f'{html.bold("Введите номер телефона в формате: 9237835676")}\n\n'
        'Обещаю никогда и ничего не писать на номер\n'
        'Он нужен только для уникальной идентификации, что бы ты мог войти с любого аккаунта телеграмм'
    )
    await state.set_state(CreateUser.phone)


@router.message(CreateUser.phone)
async def get_phone(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите номер в формате: 9237835676')
        return

    phone = message.text
    await state.update_data(phone=phone)

    await message.answer(f"Я сохранил этот номер: {phone}")
    await message.answer(
        'Благодарю за терпения, еще пара вопросов!'
        'Выберите из списка три категории, которые больше всего откликаются \n\n'
        'Впишите или вставьте категории через запятую'
    )

    await state.set_state(CreateUser.interests)


@router.message(CreateUser.phone)
async def get_phone(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите номер в формате: 9237835676')
        return

    phone = message.text
    await state.update_data(phone=phone)

    await message.answer(f"Я сохранил этот номер: {phone}")
    await message.answer(
        'Благодарю за терпения, еще пара вопросов!'
        'Выберите из списка три категории, которые больше всего откликаются \n\n'
        'Впишите или вставьте категории через запятую'
    )

    await state.set_state(CreateUser.interests)


@router.message(CreateUser.interests)
async def get_interests(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Я жду от тебя только текст!')
        return

    interests = [i.strip() for i in message.text.lower().split(',') if i.strip()]
    await state.update_data(interests=interests)

    await state.set_state(CreateUser.tz)  # 👉 переходим к выбору часового пояса

    await message.answer(
        "Выбери свой часовой пояс, чтобы я мог присылать вопросы в удобное время:\n\n"
        "Если ты не уверен, просто выбери ближайший город.",
        reply_markup=timezone_keyboard()
    )

    # data = await state.get_data()
    #
    # pilgrim['username'] = data['username']
    # pilgrim['birth_date'] = data['birth_date']
    # pilgrim['phone'] = data['phone']
    # pilgrim['interests'] = data['interests']
    #
    # try:
    #     async with SessionLocal() as db:  # ✅ Асинхронный контекст
    #         user = await create_user(
    #             db,
    #             username=data['username'],
    #             birth_date=data['birth_date'],
    #             phone=data['phone'],
    #             interests=data['interests'],
    #             telegram_id=str(message.from_user.id)
    #         )
    #         await message.answer(
    #             'Спасибо! Давай проверим:\n\n'
    #             f'Ты: {user.username}\n'
    #             f'Дата: {user.birth_date}\n'
    #             f'Твой номер: {user.phone}\n'
    #             f'Интересы: {", ".join(user.interests)}'
    #         )
    # except Exception as e:
    #     await message.answer(f'Произошла ошибка при сохранении в базу данных: {e}')
    #
    # await state.clear()