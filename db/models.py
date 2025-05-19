from datetime import datetime

from sqlalchemy import Column, Integer, String, JSON, Date, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import async_sessionmaker
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///db/users.db"

engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

Base = declarative_base()

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    birth_date = Column(Date)
    phone = Column(String, unique=True, index=True)
    interests = Column(JSON)
    telegram_id = Column(String, nullable=True)
    # Новые поля:
    timezone = Column(String, nullable=False)  # например, "Europe/Moscow"
    registered_at = Column(DateTime, default=datetime.utcnow)  # дата регистрации


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(String)  # Можно использовать UUID или уникальное поле из JSON
    answered_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="answers")

# В модели User:
User.answers = relationship("UserAnswer", back_populates="user")


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())