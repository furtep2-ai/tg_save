from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
async def set_commands_users(bot: Bot, chat_id: int):
    user_menu = [
        BotCommand(command="open", description="Открыть приложение")
    ]
    await bot.set_my_commands(commands=user_menu, scope=BotCommandScopeChat(chat_id=chat_id))