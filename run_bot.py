"""
This module serves as the entry point for running the Telegram bot.

It performs the following tasks:
    - Imports necessary modules and components.
    - Defines an asynchronous function to reset the Redis database.
    - Defines the main asynchronous function to reset the Redis database and start polling the bot for updates.
    - Runs the main function using asyncio when the module is executed as the main program.
"""
import asyncio

from bot import bot
from config import redis_client
from dispatcher import dp


async def _reset_redis_db() -> None:
    """
    Asynchronously resets the Redis database by deleting all keys.

    This function retrieves all keys from the Redis database and deletes them.
    It uses the `redis_client` to perform these operations.

    Returns:
        None
    """
    keys = await redis_client.keys("*")
    if keys:
        await redis_client.delete(*keys)


async def main() -> None:
    """
    Is main entry point for the bot.

    This asynchronous function performs the following tasks:
    1. Resets the Redis database.
    2. Starts polling the bot for updates.

    Returns:
        None
    """
    await _reset_redis_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
