import asyncio
import aiogram as io
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

import config as conf

from tg_bot.routers import admin, grenades


async def set_commands(bot: io.Bot):
    """Устанавливает перечень команд для бота"""
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="grenades", description="Гранаты"),
        BotCommand(command="add_grenade", description="Добавить гранату"),
        BotCommand(command="delete_grenade", description="Удалить гранату"),
        BotCommand(command="update_grenade", description="Изменение гранат"),
        BotCommand(command="add_images", description="Добавить изображение"),
        BotCommand(command="help", description="Справочная информация"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot() -> None:
    """Starting telegram bot"""
    bot = io.Bot(conf.BOT_TOKEN, parse_mode=ParseMode.HTML)

    storage = MemoryStorage()
    dispatcher = io.Dispatcher(storage=storage)
    await set_commands(bot)

    dispatcher.include_routers(admin.router, grenades.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logger.info("Starting bot...")
    asyncio.run(start_bot())
