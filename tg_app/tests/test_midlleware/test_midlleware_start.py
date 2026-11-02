from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
import pytest
from tg_app.midllewares.check_user import RegistrationCheckMiddleware
from tg_app.database_tools.user_requests import User
from tg_app.states.user_states import BotSession
from aiogram.fsm.context import FSMContext


class Test_Midlleware_Start():
    @pytest.mark.asyncio
    async def test_check_midlleware_start(self, mocker):
        fake_user = AsyncMock(spec=types.User)
        fake_user.configure_mock(username="Test", id=45)

        fake_message = AsyncMock()
        fake_message.configure_mock(from_user=fake_user, text="/start", answer=AsyncMock(), bot=AsyncMock())

        fake_state = AsyncMock(spec=FSMContext)
        fake_state.get_state.return_value = None
        fake_state.set_state = AsyncMock()

        middleware = RegistrationCheckMiddleware()
        fake_handler = AsyncMock()
        fake_data = {"state": fake_state}

        mock_session = mocker.patch("tg_app.database_tools.user_requests.AsyncSessionLocal")
        fake_db = AsyncMock()
        mock_session.return_value.__aenter__.return_value = fake_db
        mock_result = MagicMock()
        fake_db.execute.return_value = mock_result
        mock_result.scalar_one_or_none.return_value = None 

        await middleware(fake_handler, fake_message, fake_data)

        fake_handler.assert_awaited_once()


    @pytest.mark.asyncio
    async def test_check_midlleware_start_invalid_type(self, mocker):
        fake_db = AsyncMock()

        mock_select = mocker.patch('tg_app.database_tools.user_requests.AsyncSessionLocal')
    
        mock_select.return_value.__aenter__.return_value = fake_db

        mock_result = MagicMock()
        fake_db.execute.return_value = mock_result
        mock_result.scalar_one_or_none.return_value = None
        
        fake_user = AsyncMock(spec = types.User)
        fake_user.configure_mock(username = "Test", id = 45)
        
        fake_message = AsyncMock()
        fake_message.configure_mock(from_user = fake_user, text = None, answer = AsyncMock())
        
        middleware = RegistrationCheckMiddleware()
        fake_handler = AsyncMock()
        fake_data = {}

        await middleware(fake_handler, fake_message, fake_data)

        fake_message.answer.assert_awaited_with("Пожалуйста, введите команду /start, чтобы пройти регистрацию.")
        fake_handler.assert_not_awaited()







