"""Module defines the basic states for the Telegram bot using aiogram's finite state machine (FSM).

Attributes:
    start_menu (State): Represents the state for the start menu.
"""
from aiogram.fsm.state import State

start_menu = State("start_menu")
