from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    admin_active = State()
    waiting_for_make_id = State()
    waiting_for_delete_id = State()
    