"""Module that defines the different states in the process of adding an expense in the Telegram bot."""
from aiogram.fsm.state import State, StatesGroup


class AddExpenseStatesGroup(StatesGroup):
    """Class that defines the different states in the process of adding an expense in the Telegram bot.

    Attributes:
        entering_amount (State): State where the user is prompted to enter the amount of the expense.
        entering_name (State): State where the user is prompted to enter the name or description of the expense.
        selecting_category (State): State where the user is prompted to select a category for the expense.
        confirming_expense (State):
            State where the user is prompted to confirm the details of the expense before saving.
    """

    entering_amount = State()
    entering_name = State()
    selecting_category = State()
    confirming_expense = State()
