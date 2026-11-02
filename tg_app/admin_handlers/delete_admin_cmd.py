from aiogram import Router, types
from aiogram.filters import Command
from tg_app.database_tools.database import AsyncSessionLocal, User
from tg_app.database_tools.user_requests import delete_admin
from tg_app.states.admin_states import AdminStates
from aiogram.fsm.context import FSMContext
from tg_app.states.user_states import BotSession
router = Router()

@router.message(Command("delete_admin"))
async def delete_admin_func(message: types.Message, state: FSMContext):  
    await state.set_state(BotSession.active) 

    try:

        data = await state.get_data()

        current_user = data.get("current_user")

    except AttributeError as e:

        current_user = None

    try:

        is_admin = current_user.is_admin

    except AttributeError as e:

        is_admin = None

    if not current_user:
        await message.answer("Ошибка: данные пользователя не найдены.")
        return 
    if not is_admin:
        await message.answer("У вас нет прав")
        return
    await message.answer("Введите ID пользователя, которого хотите лишить админских прав.")
    await state.set_state(AdminStates.waiting_for_delete_id)

@router.message(AdminStates.waiting_for_delete_id)
async def delete_process_id_user(message: types.Message, state: FSMContext):
    data = await state.get_data()

    current_user: User = data.get("current_user")

    if not current_user or not current_user.is_admin:
        await message.answer("У вас нет прав для выполнения этой команды.")
        await state.clear()
        return
    
    try:
        user_id = int(message.text)
    except ValueError as e:
        await message.answer("ID должен быть числом. Попробуйте снова.")
        return 
    
    result = await delete_admin(user_id)
    
    if result == "success":
        await message.answer(f"✅ Пользователь {user_id} успешно лишен админских прав!")

    elif result == "error":
        await message.answer("❌ Вы не зарегестрированы. Регистрация /start")

    elif result == "Already user":
        await message.answer("❌ Пользователь уже лишен админских прав.")

    await state.clear()
    await state.set_state(BotSession.active)