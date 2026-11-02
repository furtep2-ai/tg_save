from aiogram.fsm.state import StatesGroup, State

class BotSession(StatesGroup):
    active = State()
    blocked = State()
    admin = State()
    user = State()
    waiting_topic = State()
    confirm_topic = State()
    ai_checking = State()
    waiting_new_context = State()
    waiting_registration = State()