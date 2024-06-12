from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from tg_bot.middlewares import CheckIsAdminMiddleware
from config import ADMINS

router = Router()

router.message.middleware.register(CheckIsAdminMiddleware(ADMINS))


@router.message(Command("add_grenade"))
async def add_grenade_handler(message: types.Message) -> None:
    await message.answer("Added grenade")