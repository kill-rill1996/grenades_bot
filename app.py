import asyncio
import aiogram as io
from aiogram.enums import ParseMode
from loguru import logger

import config as c
from tg_bot.routers import admin


async def start_bot() -> None:
    """Starting telegram bot"""
    bot = io.Bot(c.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dispatcher = io.Dispatcher()

    dispatcher.include_routers(admin.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logger.info("Starting bot...")
    asyncio.run(start_bot())
