from aiogram.fsm.state import State, StatesGroup


class StartState(StatesGroup):
    choosing_language = State()
    waiting_for_phone = State()
