from aiogram.fsm.state import State, StatesGroup


class SettingsState(StatesGroup):
    waiting_for_language_choice = State()


class FeedbackState(StatesGroup):
    waiting_for_feedback = State()