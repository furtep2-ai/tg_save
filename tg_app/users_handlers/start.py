from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from tg_app.states.user_states import BotSession
from tg_app.database_tools.user_requests import select_user, save_user
from tg_app.keyboards.inline_boards import confirm_keyboard
from tg_app.menu.admin_menu import set_commands_admins
from tg_app.menu.users_menu import set_commands_users

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    print("START это старт работает")
    await state.clear()
    print("STEP 2")
    tg_user_name = message.from_user.username
    tg_user_id = message.from_user.id
    
    if not tg_user_name:
        print("STEP 3")
        await message.answer("⚠️ У вас не установлен username в настройках Telegram! Пожалуйста, создайте его, чтобы пользоваться ботом.")
        return
    
    user = await select_user(tg_user_id)
    chat_id = message.chat.id
    
    if user is None:
        print("STEP 4")
        await state.update_data(user_id=tg_user_id, user_name=tg_user_name)
        await state.set_state(BotSession.waiting_registration)
        await message.answer("Выберите удобный вам часовой пояс:", reply_markup=confirm_keyboard)
        return
    else:
        print("STEP 5")
        await state.set_state(BotSession.active)
        if user.is_admin:
            await message.answer(f"Приветствуем, Администратор {message.from_user.username}!")
            await set_commands_admins(message.bot, chat_id)
        else:
            await message.answer(f"Рад видеть тебя снова, {message.from_user.username}! Ты уже зарегистрирован.")
            await set_commands_users(message.bot, chat_id)



TIMEZONES = {
    "asia_almaty": "Asia/Almaty",
    "europe_moscow": "Europe/Moscow",
    "europe_london": "Europe/London",
    "america/new_york": "America/New_York",
    "asia_tokyo": "Asia/Tokyo",
    "utc": "UTC"
}

@router.callback_query(F.data.in_(TIMEZONES.keys()))
async def set_timezone(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    tg_user_id = data.get("user_id")
    tg_user_name = data.get("user_name")
    
    selected_timezone = TIMEZONES[callback.data]
    
    result = await save_user(tg_user_id, tg_user_name, selected_timezone)

    if not result:
        await callback.message.answer("❌ Произошла ошибка при сохранении. Попробуйте еще раз /start")
        return

    await state.set_state(BotSession.active)
    await callback.message.answer(f"✅ Успешно сохранено! Ваш часовой пояс: {selected_timezone}")
    await set_commands_users(
    callback.bot,
    callback.message.chat.id
    )

@router.callback_query(F.data == "cancel")
async def cancel_registration(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()  
    await callback.message.answer("❌ Регистрация отменена.")
    