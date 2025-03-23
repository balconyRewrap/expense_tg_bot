"""Handle the statistics menu interaction for the Telegram bot."""
from aiogram import F, Router  # noqa: WPS347  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext, LazyProxy

from handlers.basic.states import start_menu
from handlers.error_utils import handle_error_situation
from handlers.keyboards import get_statistics_menu_keyboard
from handlers.statistics_menu.states import statistics_menu

statistics_menu_router: Router = Router()


@statistics_menu_router.message(start_menu, F.text == LazyProxy("SHOW_EXPENSES_BUTTON"))
async def settings_menu_handler(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the settings menu interaction for the Telegram bot.

    This asynchronous function processes the user's message when they access the settings menu.
    It checks if the user information is available and handles any error situations accordingly.
    If the user information is valid, it sends a message with the settings menu options and updates the state.

    Args:
        message (Message): The incoming message from the user.
        state (FSMContext): The finite state machine context for managing conversation states.
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
    await state.set_state(statistics_menu)

    await message.answer(
        text=i18n.get("CHOOSE_STATISTICS_METHOD"),
        reply_markup=get_statistics_menu_keyboard(i18n),
    )


async def _ensure_safe_exit(state: FSMContext) -> None:
    """Ensure a safe exit by resetting the state and clearing sensitive data.

    Args:
        state (FSMContext): The finite state machine context to be reset.
    """
    await state.set_state(statistics_menu)
