from aiogram import BaseMiddleware
from aiogram.types import Message, BotCommandScopeChat, CallbackQuery
from typing import Any, Dict, Awaitable, Callable
from tg_app.database_tools.database import AsyncSessionLocal, User
from tg_app.database_tools.user_requests import select_user
from sqlalchemy import select
from tg_app.menu.base_menu import set_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tg_app.states.user_states import BotSession
from tg_app.states.admin_states import AdminStates

admin_commands = [
"/list_users",
"/make_admin",
"delete_admin"
]


class RegistrationCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        bot = event.bot
        chat_id = event.chat.id
        state = data.get("state")

        user = await select_user(user_id)
        if user:
            print("MIDDLEWARE WORK if user")
            print("USER:", user)
            print("TEXT:", event.text)
            if state:
                current_state = await state.get_state()
                await state.update_data(current_user = user)
                if current_state is None or current_state == BotSession.blocked.state:
                        if event.text == "/start":
                            return await handler(event, data)
                        else:
                            await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=chat_id))
                            await event.answer("Бот заблокирован введите /start для запуска бота")
                            return
            else:
                if event.text == "/start":
                    return await handler(event, data)
                else:
                    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=chat_id))
                    await event.answer("Бот заблокирован введите /start для запуска бота")
                    return
            if event.text and event.text.split()[0] in admin_commands:
                if not user.is_admin:
                    await event.answer("🛑 У вас нет прав доступа к этой команде.")
                    return
            return await handler(event, data)
        else:
            print("MIDDLEWARE WORK if not user")
            print("USER:", user)
            print("TEXT:", event.text)
            if event.text == "/start":
                print("отправил в sstart")
                return await handler(event, data)
            else:
                await event.answer("Пожалуйста, введите команду /start, чтобы пройти регистрацию.")
                await set_commands(bot, chat_id)
                return