"""Module provides handlers for managing the removal of user-defined expense categories."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy
from aiogram_i18n.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.error_utils import handle_error_situation
from handlers.handlers_utils import (
    NavigationCallbackData,
    SelectedCategory,
    get_categories_inline_keyboard_and_total_pages,
)
from handlers.keyboards import get_menu_keyboard
from handlers.settings_menu.categories_settings_menu.remove_category.states import RemoveCategoryStatesGroup
from handlers.settings_menu.categories_settings_menu.states import categories_settings_menu
from handlers.settings_menu.states import settings_menu
from services.user_configs_service import UserConfigNotChangedError, remove_user_expenses_category

REMOVE_CATEGORY_CALLBACK_DATA = NavigationCallbackData(
    next_page="next_page_remove_category",
    prev_page="prev_page_remove_category",
)
remove_category_router: Router = Router()


@remove_category_router.message(categories_settings_menu, F.text == LazyProxy("REMOVE_CATEGORY_BUTTON"))
async def remove_category_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the removal of a category by guiding the user through the process.

    This asynchronous handler function is triggered when a user initiates the process
    of removing a category. It validates the user's information, updates the state
    with the provided category name, and displays an inline keyboard for category
    selection. If no categories are available, it handles the error situation
    gracefully.

    Args:
        message (types.Message): The incoming message object from the user.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    if message.from_user is None:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return

    await state.update_data(name=message.text)
    await state.set_state(RemoveCategoryStatesGroup.selecting_category)
    inline_keyboard_markup, total_pages = await get_categories_inline_keyboard_and_total_pages(
        message.from_user.id,
        page=0,
        navigation_callback_data=REMOVE_CATEGORY_CALLBACK_DATA,
    )
    if not inline_keyboard_markup or not total_pages:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_NO_CATEGORIES"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    # its already checked upper. Not 1 or Not None = True
    await state.update_data(current_page_remove_category=0, last_page_remove_category=total_pages - 1)  # pyright: ignore[reportOptionalOperand]
    await message.answer(
        i18n.get("CHOOSE_CATEGORY_TO_REMOVE"),
        reply_markup=inline_keyboard_markup,
    )


@remove_category_router.callback_query(
    F.data == "next_page_remove_category",
    RemoveCategoryStatesGroup.selecting_category,
)
async def next_page_remove_category_button_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Handle the "next page" button press in the remove category settings menu.

    This function is triggered when the user interacts with the "next page" button
    while navigating through the list of categories in the remove category settings menu.
    It updates the current page in the state and calls a helper function to handle
    the updated categories list.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing
            information about the user's interaction with the button.
        state (FSMContext): The finite state machine context for storing and retrieving
            user-specific data.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    # it takes user_id from callback query, not message, because user_id from message is nonsense
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    current_page = state_data.get("current_page_remove_category", 0)
    last_page = state_data.get("last_page_remove_category", 0)
    if current_page == last_page:
        await state.update_data(current_page_remove_category=0)
    else:
        await state.update_data(current_page_remove_category=current_page + 1)

    await _handle_categories_list(user_id, callback_query.message, state)


@remove_category_router.callback_query(
    F.data == "prev_page_remove_category",
    RemoveCategoryStatesGroup.selecting_category,
)
async def prev_page_remove_category_button_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Handle the "previous page" button press in the remove category menu.

    This function updates the current page in the state to the previous page
    or loops back to the last page if the current page is the first one. It
    then updates the categories list display for the user.

    Args:
        callback_query (types.CallbackQuery): The callback query triggered by the user interaction.
        state (FSMContext): The finite state machine context for storing user-specific data.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    # it takes user_id from callback query, not message, because user_id from message is nonsense
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    current_page = state_data.get("current_page_remove_category", 0)
    last_page = state_data.get("last_page_remove_category", 0)

    if current_page == 0:
        await state.update_data(current_page_remove_category=last_page)
    else:
        await state.update_data(current_page_remove_category=current_page - 1)

    await _handle_categories_list(user_id, callback_query.message, state)


@remove_category_router.callback_query(RemoveCategoryStatesGroup.selecting_category, F.data.not_contains("page"))
async def handle_category(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the callback query for removing a category in the settings menu.

    This function processes a callback query triggered when a user selects a category
    to remove. It validates the callback query, extracts the category information,
    and transitions the state to confirm the removal of the selected category.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing
            data about the user's interaction.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized
            strings.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    if not (callback_query.data and callback_query.from_user and callback_query.message):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    callback_data = SelectedCategory.unpack(callback_query.data)
    category_id = callback_data.category_id
    category_name = callback_data.category_name
    if not (category_name and category_id):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_UNKNOWN"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await state.update_data(category_id=category_id)
    await state.set_state(RemoveCategoryStatesGroup.confirming_removal)
    await callback_query.message.answer(
        i18n.get("CONFIRM_REMOVE_CATEGORY", category_name=category_name),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i18n.get("CONFIRM_REMOVE_CATEGORY_BUTTON"),
                        callback_data="confirm",
                    ),
                    InlineKeyboardButton(
                        text=i18n.get("CANCEL_REMOVE_CATEGORY_BUTTON"),
                        callback_data="cancel",
                    ),
                ],
            ],
        ),
    )


@remove_category_router.callback_query(RemoveCategoryStatesGroup.confirming_removal, F.data == "confirm")
@remove_category_router.callback_query(RemoveCategoryStatesGroup.confirming_removal, F.data == "cancel")
async def handle_confirmation(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the confirmation callback query in the settings menu for removing a category.

    This function processes the user's confirmation or cancellation of a category removal
    action. It ensures that the callback query contains valid data and user information.
    If the user cancels the action, it invokes the appropriate handler. If the user confirms
    the action, it proceeds with the confirmation handler. In case of invalid data or user
    information, it handles the error situation gracefully.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing the user's
            interaction with the bot.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if not isinstance(callback_query.message, types.Message):
        return
    if not (callback_query.data and callback_query.from_user):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    if callback_query.data == "cancel":
        await _handle_cancel(callback_query, state, i18n)
        return
    await _handle_confirm(callback_query, state, i18n)


async def _handle_categories_list(user_id: int, message: types.Message, state: FSMContext) -> None:
    """Handle the display of a paginated list of categories for a user to remove.

    Args:
        user_id (int): The ID of the user requesting the category list.
        message (types.Message): The message object containing the user's interaction.
        state (FSMContext): The finite state machine context for managing user state.
    """
    if not message.from_user:
        return
    state_data = await state.get_data()
    current_page = state_data.get("current_page_remove_category") or 0
    inline_keyboard_markup, _ = await get_categories_inline_keyboard_and_total_pages(  # noqa: VNE003
        user_id,
        page=current_page,
        navigation_callback_data=REMOVE_CATEGORY_CALLBACK_DATA,
    )
    if not inline_keyboard_markup:
        return
    await message.edit_reply_markup(
        reply_markup=inline_keyboard_markup,
    )


async def _handle_cancel(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the cancellation of the "remove category" operation in the settings menu.

    This function ensures a safe exit from the current state and sends a cancellation
    message to the user along with the main menu keyboard.

    Args:
        callback_query (types.CallbackQuery): The callback query object triggered by the user.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    await _ensure_safe_exit(state)
    if not callback_query.message:
        return
    await callback_query.message.answer(i18n.get("CANCELLED_REMOVE_CATEGORY"), reply_markup=get_menu_keyboard(i18n))


async def _handle_confirm(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the confirmation of removing a user-defined expense category.

    Args:
        callback_query (types.CallbackQuery):
            The callback query object containing information about the user's interaction.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    if not callback_query.message or not isinstance(callback_query.message, types.Message):
        return
    state_data = await state.get_data()
    user_tg_id = callback_query.from_user.id
    category_id = state_data.get("category_id")
    if not all([user_tg_id, category_id]):
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_UNKNOWN"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await _ensure_safe_exit(state)
    try:
        # pyright do not understand not all() operation
        await remove_user_expenses_category(user_tg_id, category_id)  # pyright: ignore[reportArgumentType]
    except UserConfigNotChangedError:
        await handle_error_situation(
            message=callback_query.message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_UNKNOWN"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await callback_query.message.answer(i18n.get("CATEGORY_REMOVED"), reply_markup=get_menu_keyboard(i18n))


async def _ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.update_data(
        name=None,
        category_id=None,
        current_page_remove_category=0,
        last_page_remove_category=0,
    )
    await state.set_state(settings_menu)
