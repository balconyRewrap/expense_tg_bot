# TODO(balconyRewrap): add documentation when all routers will be in DP
from aiogram import Dispatcher

from bot import bot
from config import i18n_middleware, storage
from handlers.add_expense.handler import add_expense_router
from handlers.basic.default_handler import default_router
from handlers.basic.registration_handler import registration_router
from handlers.basic.start_handler import start_router

dp = Dispatcher(bot=bot, storage=storage)
i18n_middleware.setup(dp)

dp.include_router(start_router)
dp.include_router(registration_router)

dp.include_router(add_expense_router)

dp.include_router(default_router)
