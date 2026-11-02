from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Asia/Almaty", callback_data="asia_almaty"),
            InlineKeyboardButton(text="Europe/Moscow", callback_data="europe_moscow"),
        ],
        [
            InlineKeyboardButton(text="Europe/London", callback_data="europe_london"),
            InlineKeyboardButton(text="America/New_York", callback_data="america_newyork"),
        ],
        [
            InlineKeyboardButton(text="Asia/Tokyo", callback_data="asia_tokyo"),
            InlineKeyboardButton(text="UTC", callback_data="utc"),
        ],
        [
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
        ]
    ]
)

app = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Приложение", web_app=WebAppInfo(url="https://first-project-pop.web.app"))]
    ]
)