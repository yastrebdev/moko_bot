from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from db.models import User, engine
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, timezone, datetime

from questions.send_question import send_question_now
from utils.scheduler import scheduler

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def create_user(
        db: AsyncSession,
        username: str,
        birth_date: date,
        phone: str,
        interests: list,
        telegram_id: str,
        tz: str
):
    db_user = User(
        username=username,
        birth_date=birth_date,
        phone=phone,
        interests=interests,
        telegram_id=telegram_id,
        timezone = tz,
        registered_at = datetime.now(timezone.utc)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Отправка первого вопроса сразу
    await send_question_now(db_user)

    # Планирование ежедневной отправки вопроса в 14:00 по времени пользователя
    scheduler.add_job(
        send_question_now,
        'cron',
        hour=14,
        minute=0,
        timezone=tz,
        args=[db_user],
        id=f"daily_question_{db_user.id}",
        replace_existing=True
    )

    return db_user


async def find_user_by_tg_id(telegram_id):
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()
        if user is None:
            print("Пользователь не найден")
        return user