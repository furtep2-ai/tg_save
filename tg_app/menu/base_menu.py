from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
async def set_commands(bot: Bot, chat_id: int = None):
    main_menu = [
        BotCommand(command="start", description="Запустить бота / Регистрация") 
    ]
    if chat_id:
        await bot.set_my_commands(commands=main_menu, scope=BotCommandScopeChat(chat_id=chat_id))
    else:
        await bot.set_my_commands(commands=main_menu, scope=BotCommandScopeDefault())