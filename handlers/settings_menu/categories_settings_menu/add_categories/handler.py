"""Handler for adding new categories to the user's expenses categories list."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from handlers.error_utils import handle_error_situation
from handlers.handlers_utils import add_category_handler
from handlers.keyboards import get_add_categories_keyboard, get_menu_keyboard
from handlers.settings_menu.categories_settings_menu.add_categories.states import waiting_categories
from handlers.settings_menu.categories_settings_menu.states import categories_settings_menu
from handlers.settings_menu.states import settings_menu
from services.user_configs_service import UserConfigNotChangedError, add_user_expenses_categories

add_category_router: Router = Router()


@add_category_router.message(categories_settings_menu, F.text == LazyProxy("ADD_CATEGORY_BUTTON"))
async def add_categories_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the addition of new categories by the user.

    Args:
        message (types.Message): The message object containing the user's message.
        state (FSMContext): The finite state machine context to manage the state of the conversation.
        i18n (I18nContext): The internationalization context for handling localized messages.
    """
    if message.from_user is None:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )

    await state.set_state(waiting_categories)
    await message.answer(
        i18n.get("INPUT_CATEGORIES_MESSAGE"),
        reply_markup=get_add_categories_keyboard(i18n),
    )


@add_category_router.message(
    waiting_categories,
    F.text != LazyProxy("CATEGORY_END_BUTTON"),
)
async def add_new_category_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the addition of a new category.

    This asynchronous function processes a message to add a new category.
    It first checks if the message's sender information is available.
    If not, it handles the error situation.
    If the sender information is available, it proceeds to add the category.

    Args:
        message (types.Message): The message object containing the category information.
        state (FSMContext): The finite state machine context for the current user.
        i18n (I18nContext): The internationalization context for handling translations.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_USER_INFO"), _ensure_safe_exit)
        return
    await add_category_handler(message, state, i18n, _ensure_safe_exit)


@add_category_router.message(waiting_categories, F.text == LazyProxy("CATEGORY_END_BUTTON"))
async def end_categories_input_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the end of the categories input process.

    Args:
        message (types.Message): The message object containing the user's input.
        state (FSMContext): The finite state machine context for the current user.
        i18n (I18nContext): The internationalization context for retrieving localized strings.
    """
    state_data = await state.get_data()
    categories = state_data.get("categories", [])
    if not message.from_user:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_USER_INFO"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    if not categories:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_CATEGORIES"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    try:
        await add_user_expenses_categories(message.from_user.id, categories)
    except UserConfigNotChangedError:
        await handle_error_situation(
            message=message,
            state=state,
            i18n=i18n,
            answer_text=i18n.get("ERROR_CATEGORY_NOT_ADDED"),
            ensure_safe_exit=_ensure_safe_exit,
        )
        return
    await state.set_state(categories_settings_menu)
    await message.answer(
        i18n.get("CATEGORIES_ADDED_MESSAGE"),
        reply_markup=get_menu_keyboard(i18n),
    )


async def _ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.update_data(
        categories=[],
    )
    await state.set_state(settings_menu)
