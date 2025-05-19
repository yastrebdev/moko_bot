import json
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from sqlalchemy import select

from db.models import UserAnswer, User, SessionLocal
from bot import bot

# Подгружаем вопросы один раз (или можешь делать это в каждый вызов)
with open("questions/questions.json", encoding='utf-8') as f:
    QUESTIONS = json.load(f)

def is_age_valid(user_birth_date, age_range):
    if not age_range:
        return True
    min_age, max_age = map(int, age_range.split("-"))
    today = datetime.utcnow().date()
    age = today.year - user_birth_date.year - ((today.month, today.day) < (user_birth_date.month, user_birth_date.day))
    return min_age <= age <= max_age

async def send_question_now(user: User):
    async with SessionLocal() as session:
        # Получаем id уже отправленных вопросов
        result = await session.execute(
            select(UserAnswer.question_id).where(UserAnswer.user_id == user.id)
        )
        answered_ids = {row[0] for row in result.all()}

        # Фильтрация по возрасту и уже отправленным вопросам
        valid_questions = [
            q for q in QUESTIONS
            if q["id"] not in answered_ids and is_age_valid(user.birth_date, q.get("age_range", ""))
        ]

        if not valid_questions:
            return  # Можно отправить сообщение "вопросы закончились"

        question = random.choice(valid_questions)

        # Формируем сообщение
        message_text = question["text"]
        if question.get("description"):
            message_text += f"\n\n_{question['description']}_"  # Курсив

        # Клавиатура для quick_answer
        reply_markup = None
        if question.get("quick_answer"):
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Да", callback_data=f"answer:{question['id']}:yes")],
                    [InlineKeyboardButton(text="Нет", callback_data=f"answer:{question['id']}:no")]
                ]
            )

        # Отправка сообщения
        await bot.send_message(
            chat_id=int(user.telegram_id),
            text=message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

        # Сохраняем в базу, что вопрос отправлен
        new_answer = UserAnswer(user_id=user.id, question_id=question["id"])
        session.add(new_answer)
        await session.commit()