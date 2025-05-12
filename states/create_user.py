from aiogram.fsm.state import StatesGroup, State

pilgrim = {}

class CreateUser(StatesGroup):
    username = State()
    age = State()
    phone = State()
    interests = State()