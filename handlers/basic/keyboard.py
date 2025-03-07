"""This module provides functions to generate various types of Telegram bot keyboards using the aiogram library."""
from aiogram import types

from handlers.texts import ADD_EXPENSE_BUTTON, EDIT_SETTINGS_BUTTON, MAIN_MENU_BUTTON, SHOW_EXPENSES_BUTTON

main_menu_button = types.KeyboardButton(text=MAIN_MENU_BUTTON)


def get_menu_keyboard_error_tg_id() -> types.ReplyKeyboardMarkup:
    """Generate TG keyboard for situation without TG ID (fully error situations).

    This function creates a reply keyboard markup using the basic buttons obtained
    from the `_get_basic_buttons` function. The keyboard is resized to fit the screen.

    Returns:
        types.ReplyKeyboardMarkup: The generated reply keyboard markup with basic buttons.
    """
    basic_keyboard = _get_basic_buttons()
    basic_reply_keyboard_markup = types.ReplyKeyboardMarkup(keyboard=basic_keyboard, resize_keyboard=True)
    return basic_reply_keyboard_markup


def get_menu_keyboard() -> types.ReplyKeyboardMarkup:
    """Generate a ReplyKeyboardMarkup for a Telegram bot.

    This function creates a basic keyboard layout using the _get_basic_buttons function
    and returns a ReplyKeyboardMarkup object with the generated keyboard.

    Returns:
        types.ReplyKeyboardMarkup: A keyboard markup object for the Telegram bot.
    """
    basic_keyboard = _get_basic_buttons()
    basic_reply_keyboard_markup = types.ReplyKeyboardMarkup(keyboard=basic_keyboard, resize_keyboard=True)
    return basic_reply_keyboard_markup


def get_post_menu_keyboard() -> types.ReplyKeyboardMarkup:
    """Create and returns a ReplyKeyboardMarkup object with a main menu button.

    Returns:
        types.ReplyKeyboardMarkup: A keyboard markup object containing a single button labeled "Главное меню".
    """
    basic_keyboard: list[list[types.KeyboardButton]] = []
    basic_keyboard.append([main_menu_button])
    basic_reply_keyboard_markup = types.ReplyKeyboardMarkup(keyboard=basic_keyboard, resize_keyboard=True)
    return basic_reply_keyboard_markup


def _get_basic_buttons() -> list[list[types.KeyboardButton]]:
    """Generate a list of basic keyboard buttons.

    This function retrieves common buttons and returns them as a list of lists
    containing `types.KeyboardButton` objects.

    Returns:
        list[list[types.KeyboardButton]]: A list of lists of keyboard buttons.
    """
    buttons = _get_common_buttons()
    return buttons


def _get_common_buttons() -> list[list[types.KeyboardButton]]:
    """Generate a list of common keyboard buttons for a Telegram bot.

    Returns:
        list[list[types.KeyboardButton]]: A nested list containing keyboard buttons with predefined text.
    """
    return [
        [types.KeyboardButton(text=ADD_EXPENSE_BUTTON)],
        [types.KeyboardButton(text=SHOW_EXPENSES_BUTTON)],
        [types.KeyboardButton(text=EDIT_SETTINGS_BUTTON)],
    ]
