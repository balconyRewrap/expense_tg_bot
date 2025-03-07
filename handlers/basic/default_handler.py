"""This module defines a defaul message handler for an aiogram-based bot.

Attributes:
    basic_router (Router): An instance of aiogram's Router used to register message handlers.
"""
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.basic.keyboard import get_menu_keyboard
from handlers.basic.states import start_menu
from handlers.error_utils import handle_error_situation
from handlers.texts import COMMAND_NOT_RECOGNIZED, ERROR_USER_INFO

default_router: Router = Router()


@default_router.message()
async def handle_all_other_messages(message: Message, state: FSMContext) -> None:
    """Handle all messages that do not match any specific command.

    Args:
        message (Message): The message object containing the details of the received message.

    Returns:
        None: This function sends a response message to the user indicating that the command is not recognized.
    """
    if message.from_user is None:
        await handle_error_situation(message, state, ERROR_USER_INFO)
        return
    await state.clear()
    await message.answer(COMMAND_NOT_RECOGNIZED, reply_markup=get_menu_keyboard())
    await state.set_state(start_menu)
