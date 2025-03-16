"""Module provides functions to generate various types of Telegram bot keyboards using the aiogram library."""
from aiogram_i18n import I18nContext
from aiogram_i18n.types import KeyboardButton, ReplyKeyboardMarkup


def get_menu_keyboard_error_tg_id(i18n: I18nContext) -> ReplyKeyboardMarkup:
    """Generate a ReplyKeyboardMarkup object with basic buttons for the menu keyboard.

    Args:
        i18n (I18nContext): The internationalization context for translating button labels.

    Returns:
        ReplyKeyboardMarkup: A keyboard markup object with the basic buttons.
    """
    basic_keyboard = _get_basic_buttons(i18n)
    return ReplyKeyboardMarkup(keyboard=basic_keyboard, resize_keyboard=True)


def get_menu_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    """Generate a reply keyboard markup for the menu.

    Args:
        i18n (I18nContext): The internationalization context for translating button labels.

    Returns:
        ReplyKeyboardMarkup: A keyboard markup object with the basic buttons.
    """
    basic_keyboard = _get_basic_buttons(i18n)
    return ReplyKeyboardMarkup(keyboard=basic_keyboard, resize_keyboard=True)


def get_post_menu_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    """Generate a ReplyKeyboardMarkup object for the post menu.

    Args:
        i18n (I18nContext): The internationalization context to fetch localized text.

    Returns:
        ReplyKeyboardMarkup: A keyboard markup with a single button for the main menu.
    """
    basic_keyboard: list[list[KeyboardButton]] = []
    main_menu_button = KeyboardButton(text=i18n.get("MAIN_MENU_BUTTON"))

    basic_keyboard.append([main_menu_button])
    return ReplyKeyboardMarkup(keyboard=basic_keyboard, resize_keyboard=True)


def get_registration_category_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    """Generate a ReplyKeyboardMarkup object for the registration category selection.

    Args:
        i18n (I18nContext): The internationalization context for translating button labels.

    Returns:
        ReplyKeyboardMarkup: A keyboard markup object with the registration category buttons.
    """
    categories = [[KeyboardButton(text=i18n.get("REGISTRATION_CATEGORY_END_BUTTON"))]]
    return ReplyKeyboardMarkup(keyboard=categories, resize_keyboard=True)


def _get_basic_buttons(i18n: I18nContext) -> list[list[KeyboardButton]]:
    """Generate a list of basic keyboard buttons.

    Args:
        i18n (I18nContext): The internationalization context for localizing button labels.

    Returns:
        list[list[KeyboardButton]]: A list of lists containing KeyboardButton objects.
    """
    return _get_common_buttons(i18n)


def _get_common_buttons(i18n: I18nContext) -> list[list[KeyboardButton]]:
    """Generate a list of common keyboard buttons for the expense tracking bot.

    Args:
        i18n (I18nContext): The internationalization context to fetch localized button texts.

    Returns:
        list[list[KeyboardButton]]: A list of lists containing KeyboardButton objects with localized text.
    """
    return [
        [KeyboardButton(text=i18n.get("ADD_EXPENSE_BUTTON"))],
        [KeyboardButton(text=i18n.get("SHOW_EXPENSES_BUTTON"))],
        [KeyboardButton(text=i18n.get("EDIT_SETTINGS_BUTTON"))],
    ]
