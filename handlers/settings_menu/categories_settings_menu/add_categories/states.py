"""Module defines the state used in the "Add Categories" functionality.

Variables:
    waiting_categories (State): Represents the state where the bot is waiting
    for the user to input new categories to be added.
"""
from aiogram.fsm.state import State

waiting_categories = State("waiting_categories")
