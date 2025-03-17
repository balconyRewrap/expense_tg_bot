"""Utility functions for handling user input in some handlers process."""
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from handlers.error_utils import SafeExitProtocol, handle_error_situation
from handlers.keyboards import get_add_categories_keyboard


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
    state_data = await state.get_data()
    categories = state_data.get("categories", [])
    categories.append(new_category)
    await state.update_data(categories=categories)
    await message.answer(
        i18n.get("INPUT_NEXT_CATEGORY_MESSAGE"),
        reply_markup=get_add_categories_keyboard(i18n),
    )
