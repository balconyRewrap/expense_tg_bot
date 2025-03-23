"""States for custom statistics handler."""
from aiogram.fsm.state import State, StatesGroup


class CustomStatisticsStatesGroup(StatesGroup):
    """CustomStatisticsStatesGroup defines states for the custom statistics handler.

    Attributes:
        waiting_for_period (State): Represents the state where the user is prompted to select a predefined
            time period for statistics.
        waiting_for_custom_period_start (State): Represents the state where the user is prompted to input
            the start date for a custom time period.
        waiting_for_custom_period_end (State): Represents the state where the user is prompted to input
            the end date for a custom time period.
        selecting_categories (State): Represents the state where the user is prompted to select categories
            for filtering the statistics.
    """

    waiting_for_period = State()
    waiting_for_custom_period_start = State()
    waiting_for_custom_period_end = State()
    selecting_categories = State()
