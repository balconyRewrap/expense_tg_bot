"""
This module configures the Redis storage for the Telegram bot using aiogram and decouple.

Attributes:
    redis_client (Redis):
        An instance of the Redis client configured with host, port, and database from environment variables.

    storage (RedisStorage): An instance of RedisStorage using the configured Redis client.
    REDIS_HOST: The hostname of the Redis server.
    REDIS_PORT: The port number of the Redis server.
    REDIS_DB: The database number to use in the Redis server.
"""
import logging

from aiogram.fsm.storage.redis import RedisStorage
from decouple import config
from redis.asyncio.client import Redis

logging.basicConfig(level=logging.ERROR)

redis_client = Redis(
    host=config("REDIS_HOST"),  # type: ignore
    port=config("REDIS_PORT"),  # type: ignore
    db=int(config("REDIS_DB")),  # type: ignore
    decode_responses=True,
)


storage = RedisStorage(redis=redis_client)
