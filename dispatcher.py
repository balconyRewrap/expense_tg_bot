
from aiogram import Dispatcher

from bot import bot
from config import storage
from handlers.basic.start_handler import start_router

dp = Dispatcher(bot=bot, storage=storage)

dp.include_router(start_router)
