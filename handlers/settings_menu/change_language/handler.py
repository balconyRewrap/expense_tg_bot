"""Module contains handler for changing the language settings for users."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from config import LANGUAGES
from handlers.error_utils import handle_error_situation
from handlers.keyboards import get_language_inline_keyboard, get_settings_menu_keyboard
from handlers.settings_menu.change_language.states import waiting_for_language
from handlers.settings_menu.states import settings_menu

change_language_router: Router = Router()


@change_language_router.message(settings_menu, F.text == LazyProxy("CHANGE_LANGUAGE_MENU_BUTTON"))
async def change_language_handler(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle change of the language settings of the user.

    Args:
        message (types.Message): The message object containing information about the user and the message.
        state (FSMContext): The finite state machine context to manage the state of the user.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_USER_INFO"), _ensure_safe_exit)
        return

    await state.set_state(waiting_for_language)

    await message.answer(
        i18n.get("CHOOSE_LANGAUGE_MESSAGE"),
        reply_markup=get_language_inline_keyboard(),
    )


@change_language_router.callback_query(F.data.in_(LANGUAGES), waiting_for_language)
async def set_language_handler(callback_query: types.CallbackQuery, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the language selection callback for the user.

    Args:
        callback_query (types.CallbackQuery): The callback query object containing the user's selection.
        state (FSMContext): The finite state machine context to manage the state of the user.
        i18n (I18nContext): The internationalization context to handle multilingual support.
    """
    if not callback_query.message or not callback_query.from_user:
        return

    language = callback_query.data
    if not language:
        return

    await i18n.set_locale(language)
    await _ensure_safe_exit(state)
    await callback_query.message.answer(
        i18n.get("LANGUAGE_CHANGED"),
        reply_markup=get_settings_menu_keyboard(i18n),
    )


async def _ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.update_data(language=None)
    await state.set_state(settings_menu)
