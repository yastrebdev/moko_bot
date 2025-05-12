from aiogram import html, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.create_user import CreateUser, pilgrim

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

    interests = message.text.lower().strip().split()
    print(interests)
    await state.update_data(interests=interests)

    data = await state.get_data()
    pilgrim['username'] = data['username']
    pilgrim['age'] = data['age']
    pilgrim['phone'] = data['phone']
    pilgrim['interests'] = data['interests']

    await message.answer(
        'Спасибо! Давай проверим:\n\n'
        f'Ты {data['username']}'
        f'Тебе {data['age']}'
        f'Твой номер {data['phone']}'
        f'Тебе ближе {data['interests']}'
    )

    await state.clear()