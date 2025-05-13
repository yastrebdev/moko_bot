from aiogram import html, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from pyexpat.errors import messages

from states.create_user import CreateUser, pilgrim
from db.database import SessionLocal, create_user
from states.login_user import LoginUser
from db.models import User

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
            f'{html.bold("Сколько тебе лет?")}\n\n'
            'Мне нужна эта информация для подбора более подходящих вопросов\n\n'
            f'Если не хотите указывать возраст, просто отправьте {html.code(0)}'
        )
        await state.set_state(CreateUser.age)


@router.message(CreateUser.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи число 🧮")
        return

    age = int(message.text)
    await state.update_data(age=age)

    await message.answer(f"Запомнил! тебе {age} лет.")
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
        'Благодарю за терпения, осталось последнее!'
        'Выберите из списка три категории, которые больше всего откликаются \n\n'
        'Впишите или вставьте категории через запятую'
    )

    await state.set_state(CreateUser.interests)


@router.message(CreateUser.interests)
async def get_interests(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Я жду от тебя только текст!')
        return

    # Разбор интересов
    interests = [i.strip() for i in message.text.lower().split(',') if i.strip()]
    await state.update_data(interests=interests)

    # Получение всех данных
    data = await state.get_data()

    # Сохраняем в глобальную переменную (если нужно для логики)
    pilgrim['username'] = data['username']
    pilgrim['age'] = data['age']
    pilgrim['phone'] = data['phone']
    pilgrim['interests'] = data['interests']

    # Сохраняем в БД
    db = SessionLocal()
    try:
        user = create_user(
            db,
            username=data['username'],
            age=data['age'],
            phone=data['phone'],
            interests=data['interests'],
            telegram_id=str(message.from_user.id)
        )
        await message.answer(
            'Спасибо! Давай проверим:\n\n'
            f'Ты: {user.username}\n'
            f'Тебе: {user.age}\n'
            f'Твой номер: {user.phone}\n'
            f'Интересы: {", ".join(user.interests)}'
        )
    except Exception as e:
        await message.answer(f'Произошла ошибка при сохранении в базу данных: {e}')
    finally:
        db.close()

    await state.clear()


@router.message(LoginUser.phone)
async def login_phone(message: Message, state: FSMContext):
    contact = message.contact

    phone = contact.phone_number.replace("+", "").lstrip("7")

    db = SessionLocal()
    user = db.query(User).filter(User.phone == phone).first()

    if user:
        # Сохраняем/обновляем telegram_id
        user.telegram_id = str(message.from_user.id)
        db.commit()
        await message.answer(
            f"✅ Добро пожаловать, {user.username}!\n"
            f"Твои интересы: {', '.join(user.interests)}"
        )
    else:
        await message.answer("Пользователь с таким номером не найден.")
    db.close()
    await state.clear()