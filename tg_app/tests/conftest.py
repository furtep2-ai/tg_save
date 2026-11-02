import pytest
from unittest.mock import AsyncMock
from aiogram.fsm.context import FSMContext


@pytest.fixture
def fake_state(scope = "function"):
    state = AsyncMock(spec=FSMContext)
    return state