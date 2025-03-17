"""Module defines a defaul message handler for an aiogram-based bot.

Attributes:
    basic_router (Router): An instance of aiogram's Router used to register message handlers.
"""
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_i18n import I18nContext

from handlers.basic.states import start_menu
from handlers.error_utils import handle_error_situation
from handlers.keyboards import get_menu_keyboard

default_router: Router = Router()


@default_router.message()
async def handle_all_other_messages(message: Message, state: FSMContext, i18n: I18nContext) -> None:
    """Handle all other messages that do not match any specific command.

    This function is called when a message is received that does not match any predefined command.
    It clears the current state, sends a message to the user indicating that the command is not recognized,
    and sets the state to the start menu.

    Args:
        message (Message): The incoming message object.
        state (FSMContext): The finite state machine context for managing user states.
        i18n (I18nContext): The internationalization context for retrieving localized messages.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, i18n, i18n.get("ERROR_USER_INFO"))
        return
    await state.clear()
    await message.answer(i18n.get("COMMAND_NOT_RECOGNIZED"), reply_markup=get_menu_keyboard(i18n))
    await state.set_state(start_menu)
