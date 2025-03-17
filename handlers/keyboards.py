"""Module provides functions to generate various types of Telegram bot keyboards using the aiogram library."""
from aiogram_i18n import I18nContext
from aiogram_i18n.types import KeyboardButton, ReplyKeyboardMarkup


def get_settings_menu_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    """Generate a settings menu keyboard for a Telegram bot.

    Args:
        i18n (I18nContext):
            The internationalization context to fetch localized button texts.

    Returns:
        ReplyKeyboardMarkup:
            A Telegram ReplyKeyboardMarkup object with the settings menu buttons.
    """
    settings_buttons = [
        [KeyboardButton(text=i18n.get("CATEGORIES_SETTINGS_MENU_BUTTON"))],
        [KeyboardButton(text=i18n.get("CHANGE_CURRENCY_MENU_BUTTON"))],
        [KeyboardButton(text=i18n.get("CHANGE_LANGUAGE_MENU_BUTTON"))],
        [_get_main_menu_button(i18n)],
    ]
    return ReplyKeyboardMarkup(keyboard=settings_buttons, resize_keyboard=True)


def get_category_settings_menu_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    """Generate a category settings menu keyboard for a Telegram bot.

    Args:
        i18n (I18nContext):
            The internationalization context to fetch localized button texts.

    Returns:
        ReplyKeyboardMarkup:
            A Telegram ReplyKeyboardMarkup object with the category settings menu buttons.
    """
    category_settings_buttons = [
        [KeyboardButton(text=i18n.get("ADD_CATEGORY_BUTTON"))],
        [KeyboardButton(text=i18n.get("REMOVE_CATEGORY_BUTTON"))],
        [_get_main_menu_button(i18n)],
    ]
    return ReplyKeyboardMarkup(keyboard=category_settings_buttons, resize_keyboard=True)


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
    basic_keyboard.append([_get_main_menu_button(i18n)])
    return ReplyKeyboardMarkup(keyboard=basic_keyboard, resize_keyboard=True)


def get_add_categories_keyboard(i18n: I18nContext) -> ReplyKeyboardMarkup:
    """Generate a ReplyKeyboardMarkup object for the entering category/ies selection.

    Args:
        i18n (I18nContext): The internationalization context for translating button labels.

    Returns:
        ReplyKeyboardMarkup: A keyboard markup object with the registration category buttons.
    """
    categories = [[KeyboardButton(text=i18n.get("CATEGORY_END_BUTTON"))]]
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
        [KeyboardButton(text=i18n.get("SETTINGS_MENU_BUTTON"))],
    ]


def _get_main_menu_button(i18n: I18nContext) -> KeyboardButton:
    """Generate the main menu button for the keyboard.

    Args:
        i18n (I18nContext): The internationalization context to fetch the localized text.

    Returns:
        KeyboardButton: A keyboard button with the text for the main menu.
    """
    return KeyboardButton(text=i18n.get("MAIN_MENU_BUTTON"))
