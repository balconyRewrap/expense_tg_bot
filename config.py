"""Module configures the necessary components for the expense Telegram bot.

Variables:
    redis_client (Redis): Redis client configured with host, port, and database from environment variables.
    storage (RedisStorage): Redis-based storage for FSM.
    i18n_middleware (I18nMiddleware): Middleware for handling internationalization with default locale set to Russian.
"""
import logging
from typing import Final

from aiogram.fsm.storage.redis import RedisStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from decouple import config
from redis.asyncio.client import Redis

from middleware import LocaleManager

logging.basicConfig(level=logging.ERROR)

LANGUAGES: Final = {"ru": "Русский", "en": "English"}  # noqa: WPS407

# Pyright is unable to infer the type of the API_TOKEN variable from the decouple config function.
redis_client = Redis(
    host=config("REDIS_HOST"),  # pyright: ignore[reportArgumentType]
    port=config("REDIS_PORT"),  # pyright: ignore[reportArgumentType]
    db=int(config("REDIS_DB")),  # pyright: ignore[reportArgumentType]
    decode_responses=True,
)


storage = RedisStorage(redis=redis_client)

i18n_middleware = I18nMiddleware(
    core=FluentRuntimeCore(
        path="locales/{locale}/LC_MESSAGES",
    ),
    manager=LocaleManager(),
    default_locale="ru",
)
