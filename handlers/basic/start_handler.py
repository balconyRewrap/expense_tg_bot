"""Module defines the start handler for the Telegram bot using the aiogram framework."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext, LazyProxy

from handlers.basic.registration_handler import start_registration
from handlers.basic.states import start_menu
from handlers.error_utils import handle_error_situation
from handlers.keyboard import get_menu_keyboard
from services.user_configs_service import user_config_exist_by_tg_id

start_router: Router = Router()


@start_router.message(F.text.casefold() == LazyProxy("MAIN_MENU_BUTTON", case="lower"))
@start_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle the /start command.

    This function is an asynchronous handler for the /start command in a Telegram bot.
    It clears the current state, sends a start message to the user with a menu keyboard,
    and sets the state to 'start_menu'.

    Args:
        message (types.Message): The incoming message object from the user.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for managing translations.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_USER_INFO"))
        return
    if not await user_config_exist_by_tg_id(message.from_user.id):
        await message.answer(
            i18n.get("REGISTRATION_REQUIRED"),
            reply_markup=types.reply_keyboard_remove.ReplyKeyboardRemove(),
        )
        await start_registration(message, state, i18n)
        return
    await message.answer(
        i18n.get("START_MESSAGE"),
        reply_markup=get_menu_keyboard(i18n),
    )
    await state.set_state(start_menu)
