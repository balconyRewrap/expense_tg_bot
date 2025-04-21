"""States for changing the currency in the settings menu."""
from aiogram.fsm.state import State, StatesGroup


class ChangeCurrencyStatesGroup(StatesGroup):
    """A class representing the states for changing the currency in the settings menu.

    Attributes:
        waiting_for_currency (State): Represents the state where the bot is waiting for
            the user to input the desired currency.
        confirming_currency_change (State): Represents the state where the bot is waiting
            for the user to confirm the currency change.
    """

    waiting_for_currency = State()
    confirming_currency_change = State()
