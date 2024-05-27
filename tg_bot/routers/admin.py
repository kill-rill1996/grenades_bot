import aiogram.types
from aiogram import Router

router = Router()


@router.message()
async def echo(message: aiogram.types.Message) -> None:
    await message.answer(f'{message.text}!')
