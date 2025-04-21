"""Utility functions for handling custom statistics generation in the statistics menu."""
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from aiogram_i18n.types import InlineKeyboardMarkup

from database.models import Expense
from handlers.basic.states import start_menu
from handlers.error_utils import handle_error_situation
from handlers.handlers_utils import (
    NavigationCallbackData,
    SelectedCategory,
    get_categories_inline_keyboard_and_total_pages,
    get_navigation_inline_keyboard,
)
from services.expenses_service import (
    ALL_CATEGORIES_ID,
    ExpensePeriod,
    StatisticsNotGeneratedError,
    get_expenses_by_category_ids_by_period,
)


@dataclass
class StatisticsConfig:
    """StatisticsConfig class of parameters for generating statistics.

    Attributes:
        period (str | None): The predefined period for the statistics (e.g., "daily", "weekly", "monthly").
            Can be None if no predefined period is selected.
        custom_period_start_date (date | None): The start date for a custom period. Can be None if no custom
            period is defined.
        custom_period_end_date (date | None): The end date for a custom period. Can be None if no custom
            period is defined.
        categories (dict[int, str]): A dictionary mapping category IDs (int) to their corresponding names (str).
            Used to filter or group statistics by categories.
    """

    period: str | None
    custom_period_start_date: date | None
    custom_period_end_date: date | None
    categories: dict[int, str]


async def ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.update_data(
        period=None,
        custom_period_start_date=None,
        custom_period_end_date=None,
        categories={},
        current_page_choose_category=0,
        last_page_category_expenses=0,
    )
    await state.set_state(start_menu)


async def send_statistics(
    user_id: int,
    message: types.Message,
    state: FSMContext,
    i18n: I18nContext,
    statistics_navigation_callback_data: NavigationCallbackData,
) -> None:
    """Send statistical data to the user in a paginated format.

    This function retrieves statistical pages for the user and sends the first page
    along with navigation buttons. If no statistics are available, it handles the
    error situation by sending an appropriate error message.

    Args:
        user_id (int): The ID of the user requesting the statistics.
        message (types.Message): The message object representing the user's request.
        state (FSMContext): The finite state machine context for managing user state.
        i18n (I18nContext): The internationalization context for localized messages.
        statistics_navigation_callback_data (NavigationCallbackData): Callback data
            used for navigation between statistical pages.
    """
    statististics_pages = await get_statistics_pages(user_id, message, state, i18n)
    if not statististics_pages:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_NO_STATISTICS"),
            ensure_safe_exit=ensure_safe_exit,
        )
        return
    await state.update_data(last_page_category_expenses=len(statististics_pages) - 1)
    await message.answer(
        text=statististics_pages[0],
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                get_navigation_inline_keyboard(
                    page=0,
                    total_pages=len(statististics_pages),
                    navigation_callback_data=statistics_navigation_callback_data,
                ),
            ],
        ),
    )


def get_period_inline_keyboard_markup(
    i18n: I18nContext,
    default_periods: dict[str, str],
    custom_periods: dict[str, str],
) -> InlineKeyboardMarkup:
    """Generate an inline keyboard markup for selecting periods.

    Args:
        i18n (I18nContext): The internationalization context used for translating button text.
        default_periods (dict[str, str]): A dictionary where keys are button text identifiers
            for default periods and values are their corresponding callback data.
        custom_periods (dict[str, str]): A dictionary where keys are button text identifiers
            for custom periods and values are their corresponding callback data.

    Returns:
        InlineKeyboardMarkup: An inline keyboard markup containing buttons for both default
        and custom periods.
    """
    period_buttons: list[list[types.InlineKeyboardButton]] = [
        [
            types.InlineKeyboardButton(text=i18n.get(button_text), callback_data=callback_data)
            for button_text, callback_data in default_periods.items()
        ],
        [
            types.InlineKeyboardButton(text=i18n.get(button_text), callback_data=callback_data)
            for button_text, callback_data in custom_periods.items()
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=period_buttons)


async def get_categories_inline_keyboard_markup(
    tg_id: int,
    page: int,
    i18n: I18nContext,
    categories_choose_pages_navigation: NavigationCallbackData,
    all_categories_name: str,
    end_categories_select_callback_data: str,
    all_categories_id: int = ALL_CATEGORIES_ID,
) -> InlineKeyboardMarkup | None:
    """Generate an inline keyboard markup for selecting categories.

    Args:
        tg_id (int): Telegram user ID.
        page (int): Current page number for category navigation.
        i18n (I18nContext): Internationalization context for retrieving localized strings.
        categories_choose_pages_navigation (NavigationCallbackData): Callback data for handling
            category navigation between pages.
        all_categories_name (str): Display name for the "All Categories" button.
        end_categories_select_callback_data (str): Callback data for the "End Selection" button.
        all_categories_id (int, optional): ID representing all categories. Defaults to ALL_CATEGORIES_ID.

    Returns:
        (InlineKeyboardMarkup | None): The generated inline keyboard markup, or None if no categories
        or pages are available.
    """
    inline_keyboard_markup, total_pages = await get_categories_inline_keyboard_and_total_pages(
        tg_id,
        page,
        categories_choose_pages_navigation,
    )
    if not inline_keyboard_markup or not total_pages:
        return None
    inline_keyboard = inline_keyboard_markup.inline_keyboard
    inline_keyboard_custom = [
        [
            types.InlineKeyboardButton(
                text=i18n.get("ALL_CATEGORIES_BUTTON"),
                callback_data=SelectedCategory(
                    category_id=all_categories_id,
                    category_name=all_categories_name,
                ).pack(),
            ),
        ],
    ]
    inline_keyboard_custom.extend(inline_keyboard)
    inline_keyboard_custom.append(
        [
            types.InlineKeyboardButton(
                text=i18n.get("END_CATEGORIES_SELECT_BUTTON"),
                callback_data=end_categories_select_callback_data,
            ),
        ],
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard_custom)


async def handle_categories_list(
    user_id: int,
    message: types.Message,
    state: FSMContext,
    i18n: I18nContext,
    categories_choose_pages_navigation: NavigationCallbackData,
    all_categories_name: str,
    end_categories_select_callback_data: str,
) -> None:
    """Handle the display and navigation of a paginated list of categories in a Telegram bot.

    Args:
        user_id (int): The Telegram user ID of the user interacting with the bot.
        message (types.Message): The Telegram message object representing the user's interaction.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for handling translations.
        categories_choose_pages_navigation (NavigationCallbackData):
            Callback data for navigating between pages of categories.

        all_categories_name (str): The name representing the "all categories" option.
        end_categories_select_callback_data (str):
            Callback data to be used when the category selection process ends.
    """
    if not message.from_user:
        return
    state_data = await state.get_data()
    current_page = state_data.get("current_page_choose_category") or 0
    inline_keyboard_markup = await get_categories_inline_keyboard_markup(
        tg_id=user_id,
        page=current_page,
        i18n=i18n,
        categories_choose_pages_navigation=categories_choose_pages_navigation,
        all_categories_name=all_categories_name,
        end_categories_select_callback_data=end_categories_select_callback_data,
    )
    if not inline_keyboard_markup:
        return
    await message.edit_reply_markup(
        reply_markup=inline_keyboard_markup,
    )


async def get_statistics_pages(
    user_id: int,
    message: types.Message,
    state: FSMContext,
    i18n: I18nContext,
) -> list[str] | None:
    """Generate statistics pages based on user input and state data.

    Args:
        user_id (int): The ID of the user requesting the statistics.
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context containing user session data.
        i18n (I18nContext): The internationalization context for localized messages.

    Returns:
        list[str] | None: A list of strings representing the statistics pages, or None if an error occurs.

    Raises:
        StatisticsNotGeneratedError: If the statistics could not be generated.
    """
    state_data = await state.get_data()
    period = state_data.get("period")
    custom_period_start_date = state_data.get("custom_period_start_date", None)
    custom_period_end_date = state_data.get("custom_period_end_date", None)
    categories = state_data.get("categories", {})

    if not categories:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_NO_CATEGORIES_SELECTED"),
            ensure_safe_exit=ensure_safe_exit,
        )
        return None

    start_date = (
        datetime.strptime(custom_period_start_date, "%d.%m.%Y").date()  # noqa: DTZ007
        if custom_period_start_date
        else None
    )
    end_date = (
        datetime.strptime(custom_period_end_date, "%d.%m.%Y").date()  # noqa: DTZ007
        if custom_period_end_date
        else None
    )
    categories = {int(category_id): category_name for category_id, category_name in categories.items()}
    try:
        return await _generate_statistics_text(
            user_id=user_id,
            i18n=i18n,
            statistics_config=StatisticsConfig(
                period=period,
                custom_period_start_date=start_date,
                custom_period_end_date=end_date,
                categories=categories,
            ),
        )
    except StatisticsNotGeneratedError:
        return None


async def _generate_statistics_text(
    user_id: int,
    i18n: I18nContext,
    statistics_config: StatisticsConfig,
) -> list[str]:
    """Generate statistics text based on the provided information in StatisticsConfig.

    Args:
        user_id (int): The ID of the user for whom the statistics are being generated.
        i18n (I18nContext): The localization context for translating messages.
        statistics_config (StatisticsConfig): The configuration specifying the
            categories, period, and custom date range for generating statistics.

    Returns:
        list[str]: A list of strings representing the generated statistics message pages.

    Raises:
        StatisticsNotGeneratedError: If the statistics configuration is invalid
            or no expenses are found for the specified period.
    """
    if not _is_statistics_config_valid(statistics_config):
        raise StatisticsNotGeneratedError("Statistics not generated because of invalid configuration.")
    if statistics_config.period:
        expense_period = _get_expense_period_from_callback_data(statistics_config.period)
    else:
        expense_period = None

    if statistics_config.custom_period_start_date and statistics_config.custom_period_end_date:
        custom_period = (statistics_config.custom_period_start_date, statistics_config.custom_period_end_date)
    else:
        custom_period = None

    expenses = await get_expenses_by_category_ids_by_period(
        user_id,
        list(statistics_config.categories.keys()),
        period=expense_period,
        custom_period=custom_period,
    )
    if not expenses:
        raise StatisticsNotGeneratedError("No expenses found for the specified period.")
    return _generate_statistics_message_pages(expenses, statistics_config, i18n)


def _generate_statistics_message_pages(
    expenses: dict[int, list[Expense]],
    statistics_config: StatisticsConfig,
    i18n: I18nContext,
) -> list[str]:
    """Generate a list of statistics pages for the user.

    Args:
        expenses (dict[int, list[Expense]]): A dictionary mapping category IDs to lists of expenses.
        statistics_config (StatisticsConfig): The statistics configuration to generate the statistics for.
        i18n (I18nContext): The internationalization context for localizing text.

    Returns:
        list[str]: A list of strings containing the statistics message pages.
    """
    statistics_pages = []
    for category_id, category_expenses in expenses.items():
        category_name = statistics_config.categories.get(category_id)
        if not category_name:
            continue
        statistics_page = _generate_statistics_page(category_expenses, category_name, i18n)
        statistics_pages.append(statistics_page)
    return statistics_pages


def _generate_statistics_page(expenses: list[Expense], category_name: str, i18n: I18nContext) -> str:
    """Generate a statistics page for a single category.

    Args:
        expenses (list[Expense]): A list of Expense objects to generate statistics for.
        category_name (str): The name of the category to generate statistics for.
        i18n (I18nContext): The internationalization context for localizing text.

    Returns:
        str: A string containing the statistics message for the category.
    """
    if not expenses:
        return i18n.get("ERROR_NO_EXPENSES_PAGE_MESSAGE", category_name=category_name)
    sums = defaultdict(float)
    for expense in expenses:
        # pyright doesnt understand the SQL Alchemy models types
        sums[expense.currency] += expense.amount  # pyright: ignore[reportArgumentType]
    expenses_message = "\n".join(
        i18n.get(
            "CUSTOM_STATISTICS_CURRENCY_SUM",
            amount=total,
            currency=currency,
        )
        for currency, total in sums.items()
    )
    return i18n.get(
        "CUSTOM_STATISTICS_PAGE",
        category_name=category_name,
        total_expenses=expenses_message,
    )


def _is_statistics_config_valid(statistics_config: StatisticsConfig) -> bool:
    """Check if the statistics configuration is valid.

    Args:
        statistics_config (StatisticsConfig): The statistics configuration to validate.

    Returns:
        bool: True if the statistics configuration is valid, False otherwise.
    """
    custom_period_valid = _is_custom_period_valid(
        statistics_config.custom_period_start_date,
        statistics_config.custom_period_end_date,
    )
    if bool(statistics_config.period) == custom_period_valid:
        return False
    return bool(statistics_config.categories)


def _is_custom_period_valid(start_date: date | None, end_date: date | None) -> bool:
    """Validate whether a custom period defined by a start date and an end date is valid.

    Args:
        start_date (date | None): The start date of the period. Can be None.
        end_date (date | None): The end date of the period. Can be None.

    Returns:
        bool: True if both dates are provided and the start date is less than or equal to the end date,
              otherwise False.
    """
    if not (start_date and end_date):
        return False
    return start_date <= end_date


def _get_expense_period_from_callback_data(period: str) -> ExpensePeriod | None:
    """Convert a string representation of an expense period into an ExpensePeriod enum instance.

    Args:
        period (str): The string representation of the expense period.

    Returns:
        (ExpensePeriod | None): An instance of ExpensePeriod if the conversion is successful,
        otherwise None if the input string is invalid.
    """
    try:
        return ExpensePeriod(period)
    except ValueError:
        return None
