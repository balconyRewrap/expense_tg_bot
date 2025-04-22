"""Module defines the state for the statistics menu in the Telegram bot.

Attributes:
    statistics_menu (State): A state representing the statistics menu in the bot's FSM.
"""
from aiogram.fsm.state import State

statistics_menu = State("statistics_menu")
