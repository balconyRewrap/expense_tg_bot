"""Module initializes the bot and provides a function to send messages to users.

Attributes:
    API_TOKEN (str): The API token for the bot, retrieved from environment variables.
    bot (Bot): An instance of the Bot class, initialized with the API token and default properties.
"""
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from decouple import config

from config import logging

# Pyright is unable to infer the type of the API_TOKEN variable from the decouple config function.
API_TOKEN: str = config("API_TOKEN")  # pyright: ignore[reportAssignmentType]
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def send_message_to_user(user_id: int, text: str) -> None:
    """Send a message to a user via the bot.

    Args:
        user_id (int): The ID of the user to send the message to.
        text (str): The text of the message to be sent.

    Logs:
        Info: Logs a message indicating that the message was sent successfully.
        Error: Logs an error message if there was an issue sending the message.
    """
    try:
        await bot.send_message(chat_id=user_id, text=text)
        logging.info(f"Сообщение отправлено пользователю {user_id}")
    except Exception as exception:  # noqa: BLE001
        logging.error(f"Ошибка при отправке сообщения пользователю {user_id}: {exception}")
