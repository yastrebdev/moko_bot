from sqlalchemy.orm import sessionmaker
from .models import User, engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_user(db, username: str, age: int, phone: str, interests: list, telegram_id: str):
    db_user = User(
        username=username,
        age=age,
        phone=phone,
        interests=interests,
        telegram_id=telegram_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user