# TODO (balconyRewrap): add documentation when all routers will be in DP
from aiogram import Dispatcher

from bot import bot
from config import i18n_middleware, storage
from handlers.add_expense.handler import add_expense_router
from handlers.basic.default_handler import default_router
from handlers.basic.start_handler import start_router
from handlers.registration.handler import registration_router
from handlers.settings_menu.categories_settings_menu.add_categories.handler import add_category_router
from handlers.settings_menu.categories_settings_menu.handler import category_settings_menu_router
from handlers.settings_menu.change_currency.handler import change_currency_router
from handlers.settings_menu.handler import settings_menu_router

dp = Dispatcher(bot=bot, storage=storage)
i18n_middleware.setup(dp)

# start routers
dp.include_router(start_router)
dp.include_router(registration_router)

# basic menu routers
dp.include_router(add_expense_router)
dp.include_router(settings_menu_router)

# settings menu routers
dp.include_router(category_settings_menu_router)
dp.include_router(change_currency_router)

# categories menu routers
dp.include_router(add_category_router)

# default router
dp.include_router(default_router)
