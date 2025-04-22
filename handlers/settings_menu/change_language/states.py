"""Module defines the state used in the settings menu for changing the language in the Telegram bot.

Attributes:
    waiting_for_language (State): A state indicating that the bot is waiting for the user to select a language.
"""
from aiogram.fsm.state import State

waiting_for_language = State("waiting_for_language")
