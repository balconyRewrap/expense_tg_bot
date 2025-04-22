"""States for registration process."""
from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """RegistrationStates is a state group used to manage the registration process.

    Attributes:
        waiting_for_language (State): Represents the state where the bot is waiting
            for the user to select their preferred language.
        waiting_for_currency (State): Represents the state where the bot is waiting
            for the user to select their preferred currency.
        waiting_for_categories (State): Represents the state where the bot is waiting
            for the user to define their expense categories.
    """

    waiting_for_language = State()
    waiting_for_currency = State()
    waiting_for_categories = State()
