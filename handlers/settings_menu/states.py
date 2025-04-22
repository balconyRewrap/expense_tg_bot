"""Module defines the state for the settings menu in the Telegram bot.

Attributes:
    settings_menu (State): A state representing the settings menu in the bot's FSM.
"""
from aiogram.fsm.state import State

settings_menu = State("settings_menu")
