import asyncio
import aiogram as io
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

import config as conf

from tg_bot.routers import admin, grenades


async def start_bot() -> None:
    """Starting telegram bot"""
    bot = io.Bot(conf.BOT_TOKEN, parse_mode=ParseMode.HTML)

    storage = MemoryStorage()
    dispatcher = io.Dispatcher(storage=storage)

    dispatcher.include_routers(admin.router, grenades.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logger.info("Starting bot...")
    asyncio.run(start_bot())
