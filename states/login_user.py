from aiogram.fsm.state import State, StatesGroup

class LoginUser(StatesGroup):
    phone = State()