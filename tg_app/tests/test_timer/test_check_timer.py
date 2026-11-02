from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
import pytest
from tg_app.midllewares.check_user import RegistrationCheckMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tg_app.midllewares.timer import TimeoutMenuMiddleware
from datetime import datetime, timedelta
from tg_app.midllewares.timer import get_timer
from aiogram.fsm.context import FSMContext
from tg_app.states.user_states import BotSession
from pytz import timezone

@pytest.mark.asyncio
async def test_timer_admin(mocker):
    scheduler = MagicMock()
    scheduler.get_job.return_value = None

    mocker.patch(
        "tg_app.midllewares.timer.get_timezone",
        new_callable=AsyncMock,
        return_value="Asia/Almaty"
    )

    fake_admin = MagicMock()
    fake_admin.is_admin = True
    fake_admin.user_id = 232141

    fake_state = AsyncMock(spec=FSMContext)

    fake_data = {
        "current_user": fake_admin,
        "state": fake_state
    }

    fake_chat = MagicMock()
    fake_chat.id = 232141

    fake_message = AsyncMock()
    fake_message.configure_mock(
        chat=fake_chat,
        bot=AsyncMock()
    )

    fake_handler = AsyncMock()

    middleware = TimeoutMenuMiddleware(scheduler)

    frozen_time = datetime(2026, 6, 25, 12, 0, 0)

    mock_datetime = mocker.patch(
        "tg_app.midllewares.timer.datetime"
    )

    mock_datetime.now.return_value = frozen_time

    run_time = frozen_time + timedelta(minutes=20)

    await middleware(
        fake_handler,
        fake_message,
        fake_data
    )

    scheduler.add_job.assert_called_once_with(
        get_timer,
        trigger="date",
        run_date=run_time,
        args=[
            fake_message.bot,
            232141,
            fake_state
        ],
        id="timeout_232141",
        replace_existing=True,
        misfire_grace_time=30
    )

    fake_handler.assert_awaited_once()

@pytest.mark.asyncio
async def test_timer_not_admin(mocker):
    scheduler = MagicMock()
    scheduler.get_job.return_value = None

    mocker.patch(
        "tg_app.midllewares.timer.get_timezone",
        new_callable=AsyncMock,
        return_value="Asia/Almaty"
    )

    fake_user = MagicMock()
    fake_user.is_admin = False
    fake_user.user_id = 3435

    fake_state = AsyncMock(spec=FSMContext)

    fake_data = {
        "current_user": fake_user,
        "state": fake_state
    }

    fake_chat = MagicMock()
    fake_chat.id = 3435

    fake_message = AsyncMock(spec=types.Message)
    fake_message.configure_mock(
        chat=fake_chat,
        bot=AsyncMock()
    )

    fake_handler = AsyncMock()

    middleware = TimeoutMenuMiddleware(scheduler)

    frozen_time = datetime(2026, 6, 25, 12, 0, 0)

    mock_datetime = mocker.patch(
        "tg_app.midllewares.timer.datetime"
    )

    mock_datetime.now.return_value = frozen_time

    run_time = frozen_time + timedelta(minutes=10)

    await middleware(
        fake_handler,
        fake_message,
        fake_data
    )

    scheduler.add_job.assert_called_once_with(
        get_timer,
        trigger="date",
        run_date=run_time,
        args=[
            fake_message.bot,
            3435,
            fake_state
        ],
        id="timeout_3435",
        replace_existing=True,
        misfire_grace_time=30
    )

    fake_handler.assert_awaited_once()


@pytest.mark.asyncio
async def test_timer_not_data():
    fake_chat = MagicMock()
    fake_chat.configure_mock(id = 3435)
    fake_message = AsyncMock(spec=types.Message)

    fake_message.configure_mock(chat = fake_chat, bot = AsyncMock())

    scheduler = AsyncMock(spec=AsyncIOScheduler)

    fake_handler = AsyncMock()
    fake_date = {}

    midlleware = TimeoutMenuMiddleware(scheduler)

    await midlleware(fake_handler, fake_message, fake_date)

    fake_handler.assert_awaited_with(fake_message, fake_date)

    scheduler.get_job.assert_not_called()
    scheduler.add_job.assert_not_called()

    assert scheduler.add_job.call_args == None

@pytest.mark.asyncio
async def test_timer_user(mocker):
    fake_scheduler = MagicMock()
    fake_scheduler.get_job.return_value = "existing_job"

    mocker.patch(
        "tg_app.midllewares.timer.get_timezone",
        new_callable=AsyncMock,
        return_value="Asia/Almaty"
    )

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.get_state.return_value = BotSession.active.state
    fake_state.set_state = AsyncMock()

    fake_current_user = MagicMock()
    fake_current_user.is_admin = False
    fake_current_user.user_id = 777

    fake_chat = MagicMock(spec=types.Chat)
    fake_chat.id = 777

    fake_message = AsyncMock()
    fake_message.configure_mock(
        chat=fake_chat,
        bot=AsyncMock()
    )

    fake_handler = AsyncMock()

    fake_data = {
        "current_user": fake_current_user,
        "state": fake_state
    }

    middleware = TimeoutMenuMiddleware(fake_scheduler)

    frozen_time = datetime(2026, 6, 25, 12, 0, 0)

    mock_datetime = mocker.patch(
        "tg_app.midllewares.timer.datetime"
    )

    mock_datetime.now.return_value = frozen_time

    expected_time = frozen_time + timedelta(minutes=10)

    await middleware(
        fake_handler,
        fake_message,
        fake_data
    )

    fake_scheduler.get_job.assert_called_once_with(
        "timeout_777"
    )

    fake_scheduler.remove_job.assert_called_once_with(
        "timeout_777"
    )

    fake_scheduler.add_job.assert_called_once_with(
        get_timer,
        trigger="date",
        run_date=expected_time,
        args=[
            fake_message.bot,
            777,
            fake_state
        ],
        id="timeout_777",
        replace_existing=True,
        misfire_grace_time=30
    )

    fake_handler.assert_awaited_once()









    







    





    




