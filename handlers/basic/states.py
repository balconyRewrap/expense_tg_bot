"""Module defines the basic states for the Telegram bot using aiogram's finite state machine (FSM).

Attributes:
    start_menu (State): Represents the state for the start menu.
    is_admin (str): A string indicating whether the user is an admin.
"""
from aiogram.fsm.state import State, StatesGroup

start_menu = State("start_menu")


class RegistrationStates(StatesGroup):
    """States for registration process."""

    waiting_for_language = State()
    waiting_for_currency = State()
    waiting_for_categories = State()
