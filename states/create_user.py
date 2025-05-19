from aiogram.fsm.state import StatesGroup, State

pilgrim = {}

class CreateUser(StatesGroup):
    username = State()
    birth_date = State()
    phone = State()
    interests = State()
    tz = State()