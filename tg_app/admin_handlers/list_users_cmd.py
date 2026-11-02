from aiogram import Router, types
from aiogram.types import BotCommand
from aiogram.filters import Command
from tg_app.menu.admin_menu import set_commands_admins
from tg_app.database_tools.database import AsyncSessionLocal, User
import aiomysql
from aiogram.fsm.context import FSMContext
from tg_app.database_tools.user_requests import list_users
from tg_app.states.user_states import BotSession


router = Router()

@router.message(Command("list_users"))
async def list_users_func(message: types.Message, state: FSMContext):
    await state.set_state(BotSession.active)
    data = await state.get_data()
    current_user = data.get("current_user")
    if not current_user:
        await message.answer("Данные пользователя не найдены! Запустите бота /start")
        return 
    if current_user.is_admin:
        result = await list_users()
        if result:
            response_text = "👥 **Список пользователей:**\n\n"
            for i in result:
                response_text += f"• ID: `{i.user_id}` | Имя: `{i.user_name}` | Админ: {'1' if i.is_admin else '0'}\n"
            await message.answer(response_text)
        else:
            await message.answer("Список пользователей отсуствует")
    else:
        await message.answer("У вас нету доступа")