from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from models.grenade import StatusOK
from tg_bot.middlewares import CheckIsAdminMiddleware
from config import ADMINS
from api import grenades_api as api
from tg_bot.keyboards import admin as kb
from tg_bot.keyboards.grenades import maps_keyboard

router = Router()

router.message.middleware.register(CheckIsAdminMiddleware(ADMINS))


@router.message(Command("add_grenade"))
async def add_grenade_handler(message: types.Message) -> None:
    await message.answer("Added grenade")


# Grenade deletion
@router.message(Command("delete_grenade"))
@router.callback_query(lambda callback: callback.data == "back-to-maps")
async def maps_for_delete_handler(message: types.Message | types.CallbackQuery) -> None:
    """Карты для удаления гранаты"""
    if type(message) == types.Message:
        await message.answer(f"Выберите карту", reply_markup=maps_keyboard().as_markup())
    else:
        await message.message.edit_text(f"Выберите карту", reply_markup=maps_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "map")
async def grenades_for_delete_handler(callback: types.CallbackQuery) -> None:
    """Вывод списка гранат для удаления по карте"""
    map = callback.data.split("_")[1]
    response = api.get_grenades(params={"map": map})
    if response.grenades:
        await callback.message.edit_text("Выберите гранату", reply_markup=kb.grenades_keyboard(response).as_markup())
    else:
        await callback.message.delete()
        await callback.message.answer(f"На карте {map} гранат нет")
        await callback.message.answer(f"Выберите карту", reply_markup=maps_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "delete")
async def confirmation_grenade_delete_handler(callback: types.CallbackQuery) -> None:
    """Вывод клавиатуры подтверждения удаления гранаты"""
    grenade_id = callback.data.split("_")[1]
    await callback.message.edit_text("Вы действительно хотите удалить гранату?", reply_markup=kb.yes_no_keyboard(grenade_id).as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "delete-confirmation-yes")
async def delete_grenade_handler(callback: types.CallbackQuery) -> None:
    """Подтверждение удаления гранаты при нажатии Да"""
    grenade_id = callback.data.split("_")[1]
    response = api.delete_grenade(grenade_id)
    if type(response) == StatusOK:
        await callback.message.edit_text("Граната удалена")
    else:
        await callback.message.edit_text("Произошла ошибка при удалении гранаты")


@router.callback_query(lambda callback: callback.data.split("_")[0] == "delete-confirmation-no")
async def delete_grenade_handler(callback: types.CallbackQuery) -> None:
    """Отмена удаления гранаты при нажатии Нет"""
    await callback.message.delete()