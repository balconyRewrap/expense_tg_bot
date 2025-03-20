"""States group for removing category from user's categories list handler."""
from aiogram.fsm.state import State, StatesGroup


class RemoveCategoryStatesGroup(StatesGroup):
    """States Group for remove category handler.

    RemoveCategoryStatesGroup is a state group used to manage the states involved
    in the process of removing a category in the settings menu of the expense
    Telegram bot.

    Attributes:
        selecting_category (State): Represents the state where the user is selecting
            a category to remove.
        confirming_removal (State): Represents the state where the user is confirming
            the removal of the selected category.
    """

    selecting_category = State()
    confirming_removal = State()
