"""Module initializes and configures the Dispatcher for the Telegram bot using the aiogram library.

It sets up middleware, includes various routers for handling bot commands and interactions,
and organizes the bot's functionality into modular components.

Usage:
    This module is intended to be imported and executed as part of the bot's initialization process.
    It ensures that all necessary routers and middleware are properly
    configured and included in the dispatcher.
"""
from aiogram import Dispatcher

from bot import bot
from config import i18n_middleware, storage
from handlers.add_expense.handler import add_expense_router
from handlers.basic.default_handler import default_router
from handlers.basic.start_handler import start_router
from handlers.registration.handler import registration_router
from handlers.settings_menu.categories_settings_menu.add_categories.handler import add_category_router
from handlers.settings_menu.categories_settings_menu.handler import category_settings_menu_router
from handlers.settings_menu.categories_settings_menu.remove_category.handler import remove_category_router
from handlers.settings_menu.change_currency.handler import change_currency_router
from handlers.settings_menu.change_language.handler import change_language_router
from handlers.settings_menu.handler import settings_menu_router
from handlers.statistics_menu.custom_statistics.handler import custom_statistics_router
from handlers.statistics_menu.handler import statistics_menu_router
from handlers.statistics_menu.month_statistics.handler import month_statistics_router

dp = Dispatcher(bot=bot, storage=storage)
i18n_middleware.setup(dp)

# start routers
dp.include_router(start_router)
dp.include_router(registration_router)

# basic menu routers
dp.include_router(add_expense_router)
dp.include_router(statistics_menu_router)
dp.include_router(settings_menu_router)

# settings menu routers
dp.include_router(category_settings_menu_router)
dp.include_router(change_currency_router)
dp.include_router(change_language_router)

# categories menu routers
dp.include_router(add_category_router)
dp.include_router(remove_category_router)

# statistics menu routers
dp.include_router(custom_statistics_router)
dp.include_router(month_statistics_router)

# default router
dp.include_router(default_router)
