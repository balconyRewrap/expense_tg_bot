"""States for registration process."""
from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """States for registration process."""

    waiting_for_language = State()
    waiting_for_currency = State()
    waiting_for_categories = State()
