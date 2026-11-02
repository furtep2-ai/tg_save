from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from tg_app.users_handlers.start import cmd_start 
import pytest
from tg_app.database_tools.user_requests import delete_user, create_user
from tg_app.midllewares.check_user import RegistrationCheckMiddleware
from tg_app.database_tools.database import User
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from tg_app.states.user_states import BotSession

@pytest.mark.asyncio
async def test_check_case_1(mocker):
    mock_select = mocker.patch(
    'tg_app.users_handlers.start.select_user',
    new_callable=AsyncMock
    )
    mock_set_commands_users = mocker.patch('tg_app.users_handlers.start.set_commands_users', new_callable=AsyncMock)

    fake_tg_user = AsyncMock(spec=types.User)
    fake_tg_user.configure_mock(id=2, username="kgkgydj")
    
    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id=8816890796)

    fake_message = AsyncMock()
    fake_message.configure_mock( 
        from_user=fake_tg_user,
        text="/start",
        chat=fake_chat,
        answer=AsyncMock(),
        bot=AsyncMock())
    
    fake_db_user = User(user_id=2, user_name="kgkgydj", is_admin=False)

    mock_select.return_value = fake_db_user

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.configure_mock(clear = AsyncMock(), set_state = AsyncMock())

    await cmd_start(fake_message, fake_state) 

    fake_message.answer.assert_awaited_once()
    assert f"Рад видеть тебя снова, kgkgydj! Ты уже зарегистрирован." in fake_message.answer.call_args[0][0]

    mock_set_commands_users.assert_awaited_once()
    called_chat = mock_set_commands_users.call_args[0][1]
    assert called_chat == 8816890796

@pytest.mark.asyncio
async def test_check_case_2(mocker):
    mock_select_user = mocker.patch(
        "tg_app.users_handlers.start.select_user",
        new_callable=AsyncMock
    )

    mock_select_user.return_value = None

    fake_user = AsyncMock(spec=types.User)
    fake_user.configure_mock(
        username="Rertet",
        id=23232442
    )

    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id=325252)

    fake_message = AsyncMock()
    fake_message.configure_mock(
        from_user=fake_user,
        text="/start",
        chat=fake_chat,
        answer=AsyncMock(),
        bot=AsyncMock()
    )

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.clear = AsyncMock()
    fake_state.set_state = AsyncMock()
    fake_state.update_data = AsyncMock()

    await cmd_start(fake_message, fake_state)

    fake_state.update_data.assert_awaited_once_with(
        user_id=23232442,
        user_name="Rertet"
    )

    fake_state.set_state.assert_awaited_once_with(
        BotSession.waiting_registration
    )

    fake_message.answer.assert_awaited_once()

    assert (
        fake_message.answer.call_args[0][0]
        == "Выберите удобный вам часовой пояс:"
    )

@pytest.mark.asyncio
async def test_check_case_3(mocker):
    mock_select_user = mocker.patch(
        "tg_app.users_handlers.start.select_user",
        new_callable=AsyncMock
    )
    
    mock_set_commands_admins = mocker.patch('tg_app.users_handlers.start.set_commands_admins', new_callable=AsyncMock)

    fake_user = AsyncMock(spec=types.User)
    fake_user.configure_mock(id = 131313, username = "dsdsd")

    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id = 325252) 

    fake_message = AsyncMock()
    fake_message.configure_mock(
        from_user = fake_user,
        text = "/start",
        answer = AsyncMock(),
        bot = AsyncMock())

    fake_db_user = User(user_id=131313, user_name="dsdsd", is_admin=True)
    mock_select_user.return_value = fake_db_user

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.configure_mock(clear = AsyncMock(), set_state = AsyncMock())

    await cmd_start(fake_message, fake_state)

    fake_message.answer.assert_awaited_with("Приветствуем, Администратор dsdsd!")

    mock_set_commands_admins.assert_called_once()
    











    

    




    



    
    




    

