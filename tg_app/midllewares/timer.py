from datetime import datetime, timedelta
from aiogram import BaseMiddleware
from aiogram.types import Message, BotCommandScopeChat
from typing import Any, Dict, Awaitable, Callable
from tg_app.database_tools.database import AsyncSessionLocal, User
from tg_app.database_tools.user_requests import select_timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tg_app.states.user_states import BotSession
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
import pytz



async def get_timezone(user_id: int) :
    timezone = await select_timezone(user_id)

    if not timezone:
        return "Error"

    return timezone


async def get_timer(bot, chat_id, state: FSMContext):
    try:
        print(f"⏰ Таймер іске қосылды! Чат ID: {chat_id}")
        await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=chat_id))
        await bot.send_message(
        chat_id=chat_id, 
        text=f"{chat_id} , ⏰ Ваше время вышло! /start нажмите для запуска.",
        reply_markup=ReplyKeyboardRemove())
        await state.set_state(BotSession.blocked)
    except Exception as e:
        await bot.send_message(chat_id, f"Ошибка {e}")


class TimeoutMenuMiddleware(BaseMiddleware):
    def __init__(self,scheduler):
        self.scheduler = scheduler
        super().__init__()
        
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        bot = event.bot
        chat_id = event.chat.id
        current_user = data.get("current_user")
        if not current_user:
            return await handler(event, data)
        else:
            job_id = f"timeout_{chat_id}"
            if current_user.is_admin:
                minutes_to_wait = 20
            else:
                minutes_to_wait = 10
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
            state = data.get("state")
            timezone = await get_timezone(current_user.user_id)
            if timezone == "Error":
                timezone = "Asia/Almaty"
            tz = pytz.timezone(timezone)
            run_time = datetime.now(tz) + timedelta(minutes=minutes_to_wait)
            self.scheduler.add_job(
                get_timer, 
                trigger="date", 
                run_date = run_time, 
                args = [bot, chat_id, state], 
                id = job_id, 
                replace_existing = True,
                misfire_grace_time=30
            )
            return await handler(event, data)
        