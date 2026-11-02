from aiogram import Router, types
from aiogram.filters import Command
from tg_app.database_tools.database import User, AsyncSessionLocal, Base, engine
from sqlalchemy import select
import asyncio
from tg_app.menu.admin_menu import set_commands_admins
from tg_app.menu.base_menu import set_commands
from tg_app.menu.users_menu import set_commands_users
router = Router()
from aiogram.fsm.context import FSMContext
from tg_app.states.user_states import BotSession
from tg_app.database_tools.user_requests import select_user
from tg_app.keyboards.inline_boards import confirm_keyboard
from aiogram import F
from tg_app.keyboards.inline_boards import app


@router.message(Command("open"))
async def open_app_cmd(message: types.Message, state: FSMContext):
    await message.answer("Приложение", reply_markup=app)