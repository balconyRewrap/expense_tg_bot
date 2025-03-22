"""States for changing the currency in the settings menu."""
from aiogram.fsm.state import State, StatesGroup


class ChangeCurrencyStatesGroup(StatesGroup):
    """A class representing the states for changing the currency in the settings menu."""

    waiting_for_currency = State()
    confirming_currency_change = State()
