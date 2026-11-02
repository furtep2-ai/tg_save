import aiogram
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from dotenv import load_dotenv
from aiogram.filters import Command
import os
from tg_app.database_tools.database import Base, engine
import asyncio
from tg_app.menu.base_menu import set_commands
from tg_app.midllewares.check_user import RegistrationCheckMiddleware
from tg_app.users_handlers.start import router as start_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tg_app.midllewares.timer import TimeoutMenuMiddleware
import pytz
from tg_app.admin_handlers.delete_admin_cmd import router as delete_admin_router
from tg_app.admin_handlers.make_admin_cmd import router as make_admin_router
from tg_app.admin_handlers.list_users_cmd import router as list_user_router
from tg_app.users_handlers.open_app import router as open_app_router
import cryptography
load_dotenv()

import logging

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("bot.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

token_bot = os.getenv("BOT_TOKEN")
bot = Bot(token=token_bot)
dp = Dispatcher()
         
@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Отлично")

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    dp.message.middleware(RegistrationCheckMiddleware())
    scheduler = AsyncIOScheduler(timezone=pytz.UTC)
    scheduler.start()
    dp.message.middleware(TimeoutMenuMiddleware(scheduler))
    print("✅ Таблица 'users' успешно создана в MySQL!")
    await set_commands(bot)
    dp.include_router(start_router)
    dp.include_router(make_admin_router)
    dp.include_router(list_user_router)
    dp.include_router(delete_admin_router)
    dp.include_router(open_app_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Бот готов к запуску")
    asyncio.run(main())