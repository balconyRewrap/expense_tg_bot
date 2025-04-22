"""Module defines the state for the categories settings menu in the Telegram bot.

Attriutes:
    categories_settings_menu (State):
        A state representing the categories settings menu
        in the bot's FSM. This state is used to manage user interactions within the
        categories settings menu.
"""
from aiogram.fsm.state import State

categories_settings_menu = State("categories_settings_menu")
