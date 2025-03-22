"""Handler for the category settings menu interaction."""
from aiogram import F, Router  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy

from handlers.error_utils import handle_error_situation
from handlers.keyboards import get_category_settings_menu_keyboard
from handlers.settings_menu.categories_settings_menu.states import categories_settings_menu
from handlers.settings_menu.states import settings_menu

category_settings_menu_router: Router = Router()


@category_settings_menu_router.message(settings_menu, F.text == LazyProxy("CATEGORIES_SETTINGS_MENU_BUTTON"))
async def category_settings_menu_handler(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the category settings menu interaction.

    This function processes the user's message when they interact with the category
    settings menu. It sends a response message with the settings menu options and updates the state
    to `categories_settings_menu`.

    Args:
        message (Message): The incoming message from the user.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for handling translations.
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

    await message.answer(
        text=i18n.get("CHOOSE_CATEGORY_SETTINGS_MENU_ITEM"),
        reply_markup=get_category_settings_menu_keyboard(i18n),
    )
    await state.set_state(categories_settings_menu)


async def _ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.set_state(settings_menu)
