"""This module defines the start handler for the Telegram bot using the aiogram framework."""
from aiogram import F, Router, types  # noqa: WPS347
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from handlers.basic.keyboard import get_menu_keyboard
from handlers.basic.states import start_menu
from handlers.texts import MAIN_MENU_BUTTON, START_MESSAGE

start_router: Router = Router()


@start_router.message(F.text.casefold() == MAIN_MENU_BUTTON.lower())
@start_router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """Handle the /start command for the bot.

    This function clears the current state, sends a start message with a menu keyboard,
    and sets the state to the start menu.

    Args:
        message (types.Message): The message object containing the /start command.
        state (FSMContext): The finite state machine context for managing user states.

    Returns:
        None
    """
    await state.clear()
    await message.answer(
        START_MESSAGE,
        reply_markup=get_menu_keyboard(),  # type: ignore
    )
    await state.set_state(start_menu)
