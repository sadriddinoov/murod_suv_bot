from aiogram.fsm.state import State, StatesGroup


class HelpState(StatesGroup):
    waiting_for_message = State()


class FeedbackState(StatesGroup):
    waiting_for_rating = State()
    waiting_for_comment = State()