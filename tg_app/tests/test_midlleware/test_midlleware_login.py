from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
import pytest
from tg_app.midllewares.check_user import RegistrationCheckMiddleware
from tg_app.database_tools.user_requests import User
from tg_app.states.user_states import BotSession
from aiogram.fsm.context import FSMContext


class Test_Midlleware_login():
    @pytest.mark.asyncio
    async def test_not_login(self, mocker):
        fake_user = AsyncMock(spec=types.User)
        fake_user.configure_mock(username = "TestUser", id = 345)

        mock_select = mocker.patch('tg_app.database_tools.user_requests.AsyncSessionLocal')

        fake_message = AsyncMock()
        fake_message.configure_mock(from_user = fake_user, text = "/help", id = 232, answer = AsyncMock(), bot = AsyncMock())

        middleware = RegistrationCheckMiddleware()
        fake_handler = AsyncMock()
        fake_data = {}
        fake_state = AsyncMock(spec=FSMContext)
        fake_state.get_state.return_value = BotSession.active.state
        fake_state.set_state = AsyncMock()

        fake_db = AsyncMock()
        mock_result = MagicMock()
        mock_select.return_value.__aenter__.return_value = fake_db
        mock_result.scalar_one_or_none.return_value = None
        fake_db.execute.return_value = mock_result

        await middleware(handler=fake_handler, event=fake_message, data=fake_data)

        fake_message.answer.assert_awaited_once()
        fake_message.answer.assert_awaited_with("Пожалуйста, введите команду /start, чтобы пройти регистрацию.")

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "fake_db_user",
        [
            (User(user_id=2, user_name="TestUser", is_admin=False)),
            (None)
        ]
    )
    async def test_login(self, mocker, fake_db_user):
        fake_user = AsyncMock(spec=types.User)
        fake_user.configure_mock(username = "TestUser", id = 2)

        mock_select = mocker.patch('tg_app.database_tools.user_requests.AsyncSessionLocal')

        fake_chat = AsyncMock(spec = types.Chat)
        fake_chat.configure_mock(id = 232)

        fake_state = AsyncMock(spec=FSMContext)
        fake_state.get_state.return_value = BotSession.active.state
        fake_state.set_state = AsyncMock()

        fake_message = AsyncMock()
        fake_message.configure_mock(from_user = fake_user, text = "/help", chat = fake_chat, answer = AsyncMock(), bot = AsyncMock())

        middleware = RegistrationCheckMiddleware()
        fake_handler = AsyncMock()
        fake_data = {"state": fake_state}

        fake_db = AsyncMock()
        
        mock_select.return_value.__aenter__.return_value = fake_db
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = fake_db_user
        fake_db.execute.return_value = mock_result

        await middleware(handler=fake_handler, event=fake_message, data=fake_data)

        if not fake_db_user:
            fake_message.answer.assert_awaited_with('Пожалуйста, введите команду /start, чтобы пройти регистрацию.')
        else:
            fake_message.answer.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_blocked(self, mocker):
        fake_user = AsyncMock(spec=types.User)
        fake_user.configure_mock(username = "TestUser", id = 2)

        mock_select = mocker.patch('tg_app.database_tools.user_requests.AsyncSessionLocal')

        fake_chat = AsyncMock(spec = types.Chat)
        fake_chat.configure_mock(id = 232)

        fake_state = AsyncMock(spec=FSMContext)
        fake_state.get_state.return_value = BotSession.blocked.state
        fake_state.set_state = AsyncMock()

        fake_message = AsyncMock()
        fake_message.configure_mock(from_user = fake_user, text = "/help", chat = fake_chat, answer = AsyncMock(), bot = AsyncMock())

        middleware = RegistrationCheckMiddleware()
        fake_handler = AsyncMock()
        fake_data = {"state": fake_state}

        await fake_handler()