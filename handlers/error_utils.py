"""This module provides utility functions for handling errors in an aiogram-based Telegram bot.

It includes functions to safely retrieve state data or message text, and handle error situations
by sending appropriate messages to the user and ensuring a safe exit from the current state.
"""
from typing import Protocol

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.basic.keyboard import get_menu_keyboard, get_menu_keyboard_error_tg_id
from handlers.texts import ERROR_USER_INFO


class SafeExitProtocol(Protocol):
    """A protocol that defines a safe exit procedure for a state machine context."""

    async def __call__(self, state: FSMContext) -> None:
        """Asynchronously handle the call with the given FSMContext state.

        Args:
            state (FSMContext): The current state of the finite state machine context.

        Returns:
            None
        """


async def get_state_field_or_send_error(
    message: Message,
    state: FSMContext,
    field: str,
    error_text: str,
    ensure_safe_exit: SafeExitProtocol,
) -> str | None:
    """Retrieve a specific field from the FSMContext state data or send an error message if the field is not found.

    Args:
        message (Message): The message object to send the error message to.
        state (FSMContext): The finite state machine context to retrieve the state data from.
        field (str): The field name to retrieve from the state data.
        error_text (str): The error message text to send if the field is not found.
        ensure_safe_exit (SafeExitProtocol): The protocol to ensure a safe exit in case of an error.

    Returns:
        str | None: The value of the specified field if found, otherwise None.
    """
    state_data = await state.get_data()
    state_data_value = state_data.get(field)
    if not state_data_value:
        await handle_error_situation(message, state, error_text, ensure_safe_exit)
        return None
    return state_data_value


async def get_text_or_send_error(
    message: Message,
    state: FSMContext,
    error_text: str,
    ensure_safe_exit: SafeExitProtocol,
) -> str | None:
    """Asynchronously retrieves the text from a message or sends an error if the text is not present.

    Args:
        message (Message): The message object containing the text.
        state (FSMContext): The finite state machine context.
        error_text (str): The error message to send if the text is not present.
        ensure_safe_exit (SafeExitProtocol): Protocol to ensure a safe exit in case of an error.

    Returns:
        str | None: The text from the message if present, otherwise None.
    """
    if not message.text:
        await handle_error_situation(message, state, error_text, ensure_safe_exit)
        return None
    return message.text


async def handle_error_situation(
    message: Message,
    state: FSMContext,
    answer_text: str,
    ensure_safe_exit: SafeExitProtocol | None = None,
) -> None:
    """Handle error situations by sending an appropriate message to the user and optionally ensuring a safe exit.

    Args:
        message (Message): The message object containing information about the user and the message.
        state (FSMContext): The finite state machine context for the current user.
        answer_text (str): The text to be sent as a response to the user.
        ensure_safe_exit (SafeExitProtocol | None, optional):
        An optional callable to ensure a safe exit from the current state. Defaults to None.

    Returns:
        None
    """
    if not message.from_user:
        if ensure_safe_exit:
            await ensure_safe_exit(state)
        await message.answer(
            ERROR_USER_INFO,
            reply_markup=get_menu_keyboard_error_tg_id(),
        )
        return
    if ensure_safe_exit:
        await ensure_safe_exit(state)
    await message.answer(answer_text, reply_markup=get_menu_keyboard())
