"""Script serves as the entry point for running the Telegram bot.

Functions:
    _reset_redis_db: Asynchronously resets the Redis database by deleting all keys.

    main: Asynchronous main entry point for the bot, which resets the Redis database
          and starts polling for updates.

Command-line Arguments:
    --init-db: If provided, initializes the database instead of running the bot.
"""
import argparse
import asyncio
from html import parser

from bot import bot
from config import redis_client
from database.init_db import init_db
from dispatcher import dp


async def _reset_redis_db() -> None:
    """Asynchronously resets the Redis database by deleting all keys.

    This function retrieves all keys from the Redis database and deletes them.
    It uses the `redis_client` to perform these operations.
    """
    keys = await redis_client.keys("*")
    if keys:
        await redis_client.delete(*keys)


async def main() -> None:
    """Is main entry point for the bot.

    This asynchronous function performs the following tasks:
    1. Resets the Redis database.
    2. Starts polling the bot for updates.
    """
    await _reset_redis_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the bot.")
    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize the database.",
    )
    args = parser.parse_args()
    if args.init_db:
        asyncio.run(init_db())
    else:
        asyncio.run(main())
