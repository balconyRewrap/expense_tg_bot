"""States for month statistics handler."""
from aiogram.fsm.state import State, StatesGroup


class MonthStatisticsStatesGroup(StatesGroup):
    """MonthStatisticsStatesGroup defines states for the month statistics handler.

    Attributes:
        selecting_categories (State):
            Represents the state where the user is prompted to select categories for filtering the statistics.
    """

    selecting_categories = State()
