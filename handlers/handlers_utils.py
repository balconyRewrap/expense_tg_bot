"""Utility functions for handling user input in some handlers process."""
from dataclasses import dataclass

from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from handlers.error_utils import SafeExitProtocol, handle_error_situation
from handlers.keyboards import get_add_categories_keyboard
from services.user_configs_service import CategoryData, get_user_expenses_categories

MAXIMUM_CATEGORIES_PER_ROW = 2
MAXIMUM_CATEGORIES_PER_PAGE = 6


@dataclass
class NavigationCallbackData:
    """NavigationCallbackData is a data class that represents the callback data for navigation buttons."""

    next_page: str
    prev_page: str


class SelectedCategory(CallbackData, prefix="category"):
    """ChoosenCategory is a data class that represents a chosen category in the expense tracking bot.

    Attributes:
        category_id (int): The unique identifier for the category.
        category_name (str): The name of the category.
    """

    category_id: int
    category_name: str


async def add_category_handler(
    message: types.Message,
    state: FSMContext,
    i18n: I18nContext,
    ensure_safe_exit: SafeExitProtocol,
) -> None:
    """Handle the addition of a new category from the user's message.

    This function retrieves the new category from the user's message, checks if it is valid,
    and then updates the state with the new category. If the new category is not valid, it
    handles the error situation appropriately.

    Args:
        message (types.Message): The message object containing the user's input.
        state (FSMContext): The finite state machine context for managing user state.
        i18n (I18nContext): The internationalization context for handling translations.
        ensure_safe_exit (SafeExitProtocol): Protocol to ensure safe exit in case of errors.

    State Data ("categories" list):
        - Retrieves the current list of categories from the state.
        - Updates the state with the new list of categories.
    """
    new_category = message.text
    if not new_category:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_CATEGORIES"), ensure_safe_exit)
        return
    state_data = await state.get_data()
    categories = state_data.get("categories", [])
    categories.append(new_category)
    await state.update_data(categories=categories)
    await message.answer(
        i18n.get("INPUT_NEXT_CATEGORY_MESSAGE"),
        reply_markup=get_add_categories_keyboard(i18n),
    )


# I haven't found a way to avoid two DB queries without making the handler fetch all categories itself.
# So func gets so bad return
async def get_categories_inline_keyboard_and_total_pages(  # noqa: WPS118, FNE007
    tg_id: int,
    page: int,
    navigation_callback_data: NavigationCallbackData,
) -> tuple[types.InlineKeyboardMarkup, int] | tuple[None, None]:
    """Asynchronously retrieve the inline keyboard markup for user categories and the total number of pages.

    This function fetches the user's expense categories, calculates the total number of pages required to display them,
    paginates the categories for the current page, and generates the inline keyboard markup for navigation.

    Args:
        tg_id (int): The Telegram user ID.
        page (int): The current page number.
        navigation_callback_data (NavigationCallbackData): The callback data for navigation buttons.

    Returns:
        tuple[types.InlineKeyboardMarkup, int] | tuple[None, None]:
            A tuple containing the inline keyboard markup and the total number of pages.
            If the user has no categories, returns (None, None).
    """
    user_categories: list[CategoryData] | None = await get_user_expenses_categories(tg_id)
    if not user_categories:
        return None, None
    total_pages = _get_total_category_pages(user_categories)
    user_categories = _paginate_categories(user_categories, page)
    return _get_categories_inline_keyboard_markup(
        user_categories,
        page,
        total_pages,
        navigation_callback_data,
    ), total_pages


def get_confirmation_inline_keyboard_markup(
    confirm_i18n_text: str,
    cancel_i18n_text: str,
    i18n: I18nContext,
) -> types.InlineKeyboardMarkup:
    """Create an inline keyboard markup with two buttons: one for confirmation and one for cancellation.

    Args:
        confirm_i18n_text (str): The key for the confirmation button text in the i18n context.
        cancel_i18n_text (str): The key for the cancellation button text in the i18n context.
        i18n (I18nContext): The internationalization context used to retrieve localized text.

    Returns:
        types.InlineKeyboardMarkup: An inline keyboard markup containing the confirmation and cancellation buttons.
    """
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=i18n.get(confirm_i18n_text),
                    callback_data="confirm",
                ),
                types.InlineKeyboardButton(
                    text=i18n.get(cancel_i18n_text),
                    callback_data="cancel",
                ),
            ],
        ],
    )


def _get_total_category_pages(categories: list[CategoryData]) -> int:
    """Calculate the total number of pages required to display all categories.

    Args:
        categories (list[CategoryData]): A list of category data objects.

    Returns:
        int: The total number of pages needed to display the categories.
    """
    return (len(categories) + MAXIMUM_CATEGORIES_PER_PAGE - 1) // MAXIMUM_CATEGORIES_PER_PAGE


def _paginate_categories(categories: list[CategoryData], page: int) -> list[CategoryData]:
    """Paginate a list of categories.

    Args:
        categories (list[CategoryData]): The list of categories to paginate.
        page (int): The page number to retrieve.

    Returns:
        list[CategoryData]: A sublist of categories for the specified page.
    """
    start_index = page * MAXIMUM_CATEGORIES_PER_PAGE
    end_index = start_index + MAXIMUM_CATEGORIES_PER_PAGE
    return categories[start_index:end_index]


def _get_categories_inline_keyboard_markup(
    paginated_categories: list[CategoryData],
    page: int,
    total_pages: int,
    navigation_callback_data: NavigationCallbackData,
) -> types.InlineKeyboardMarkup:
    """Generate an inline keyboard markup for categories with pagination.

    Args:
        paginated_categories (list[CategoryData]): A list of category data for the current page.
        page (int): The current page number.
        total_pages (int): The total number of pages.
        navigation_callback_data (NavigationCallbackData): Callback data for navigation buttons.

    Returns:
        types.InlineKeyboardMarkup: The inline keyboard markup with category buttons and navigation buttons.
    """
    inline_keyboard = _get_categories_inline_keyboard(paginated_categories)
    inline_keyboard.append(_get_navigation_inline_keyboard(page, total_pages, navigation_callback_data))
    return types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def _get_categories_inline_keyboard(paginated_categories: list[CategoryData]) -> list[list[types.InlineKeyboardButton]]:
    """Generate an inline keyboard for Telegram bot with categories as buttons.

    Args:
        paginated_categories (list[CategoryData]): A list of tuples where each tuple contains
            a category name and category ID.

    Returns:
        list[list[types.InlineKeyboardButton]]: A list of lists, where each inner list represents
            a row of inline keyboard buttons for the categories.
    """
    inline_keyboard = []
    categories_in_row = 0
    buttons_row = []
    for category_name, category_id in paginated_categories:
        if categories_in_row == MAXIMUM_CATEGORIES_PER_ROW:
            inline_keyboard.append(buttons_row)
            buttons_row = []
            categories_in_row = 0
        button = types.InlineKeyboardButton(
            text=category_name,
            callback_data=SelectedCategory(category_id=category_id, category_name=category_name).pack(),
        )
        buttons_row.append(button)
        categories_in_row += 1
    if buttons_row:
        inline_keyboard.append(buttons_row)
    return inline_keyboard


def _get_navigation_inline_keyboard(
    page: int,
    total_pages: int,
    navigation_callback_data: NavigationCallbackData,
) -> list[types.InlineKeyboardButton]:
    """Generate an inline keyboard for navigation with previous, current, and next page buttons.

    Args:
        page (int): The current page number.
        total_pages (int): The total number of pages.
        navigation_callback_data (NavigationCallbackData): An object containing callback data for navigation buttons.

    Returns:
        list[list[types.InlineKeyboardButton]]: A list of lists containing InlineKeyboardButton objects for navigation.
    """
    previous_page_button = types.InlineKeyboardButton(
        text="<<",
        callback_data=navigation_callback_data.prev_page,
    )
    # it isn't complex F-string at all
    current_page_button = types.InlineKeyboardButton(
        text=f"{page + 1}/{total_pages}",  # noqa: WPS237
        callback_data="current_page",
    )
    next_page_button = types.InlineKeyboardButton(
        text=">>",
        callback_data=navigation_callback_data.next_page,
    )
    return [previous_page_button, current_page_button, next_page_button]
