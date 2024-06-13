from aiogram import types, F
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile

from models.grenade import StatusOK
from tg_bot.fsm_states import FSMCreateGrenade
from tg_bot.middlewares import CheckIsAdminMiddleware
from config import ADMINS
from api import grenades_api as api
from tg_bot.keyboards import admin as kb

router = Router()

router.message.middleware.register(CheckIsAdminMiddleware(ADMINS))


# GRENADE ADD
@router.message(Command("add_grenade"))
async def add_grenade_handler_start(message: types.Message, state: FSMContext) -> None:
    """Начало добавления гранаты, запрос введения карты"""
    await state.set_state(FSMCreateGrenade.map)
    await message.answer("Выберите карту", reply_markup=kb.maps_keyboard_with_cancel().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "map", FSMCreateGrenade.map)
async def add_map_grenade_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Запись карты в fsm data, запрос на выбор side"""
    map = callback.data.split("_")[1]
    await state.update_data(map=map)

    await state.set_state(FSMCreateGrenade.side)
    await callback.message.edit_text("Выберите сторону", reply_markup=kb.sides_keyboard_with_cancel().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "side", FSMCreateGrenade.side)
async def add_title_grenade_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Запись side в fsm data, запрос на выбор type"""
    side = callback.data.split("_")[1]
    await state.update_data(side=side)

    await state.set_state(FSMCreateGrenade.type)
    await callback.message.edit_text("Выберите тип гранаты", reply_markup=kb.types_keyboard_with_cancel().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "type", FSMCreateGrenade.type)
async def add_type_grenade_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Запись type в fsm data, запрос на введение title"""
    type = callback.data.split("_")[1]
    await state.update_data(type=type)
    await state.update_data(message=callback.message)

    await state.set_state(FSMCreateGrenade.title)
    await callback.message.edit_text("Введите название гранаты (например \"Смок на кт\")",
                                     reply_markup=kb.cancel_keyboard().as_markup())


@router.message(FSMCreateGrenade.title)
async def add_title_grenade_handler(message: types.Message, state: FSMContext) -> None:
    """Запись title в fsm data, запрос на введение description"""
    title = message.text
    await state.update_data(title=title)

    data = await state.get_data()

    previous_message = data["message"]
    await previous_message.delete()

    await state.set_state(FSMCreateGrenade.description)
    msg = await message.answer("Введите полное описание как бросать гранату", reply_markup=kb.cancel_keyboard().as_markup())
    await state.update_data(message=msg)


@router.message(FSMCreateGrenade.description)
async def add_description_grenade_handler(message: types.Message, state: FSMContext) -> None:
    """Запись description в fsm data, запрос на отправку картинок"""
    description = message.text
    await state.update_data(description=description)

    data = await state.get_data()
    previous_message = data["message"]
    await previous_message.delete()

    await state.set_state(FSMCreateGrenade.images)
    msg = await message.answer("Отправьте скриншот с ориентирами броска гранаты",
                               reply_markup=kb.cancel_keyboard().as_markup())
    await state.update_data(message=msg)


@router.message(F.photo, FSMCreateGrenade.images)
async def add_images_handler(message: types.Message, state: FSMContext) -> None:
    """Добавление изображений"""
    file_id = message.photo[-1].file_id
    image = await message.bot.download(file=file_id, destination="test.jpg")
    print(type(image))

    data = await state.get_data()
    previous_message = data["message"]
    try:
        await previous_message.delete()
    except TelegramBadRequest:
        pass

    await message.answer("Граната создана")


# GRENADE DELETE
@router.message(Command("delete_grenade"))
@router.callback_query(lambda callback: callback.data == "back-to-map-list")
async def maps_for_delete_handler(message: types.Message | types.CallbackQuery) -> None:
    """Вывод списка карт для удаления гранаты"""
    if type(message) == types.Message:
        await message.answer(f"Удаление гранат", reply_markup=kb.maps_keyboard().as_markup())
    else:
        await message.message.edit_text(f"Удаление гранат", reply_markup=kb.maps_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "delete-map")
async def grenades_for_delete_handler(callback: types.CallbackQuery) -> None:
    """Вывод списка гранат для удаления по карте"""
    map = callback.data.split("_")[1]
    response = api.get_grenades(params={"map": map})
    if response.grenades:
        await callback.message.edit_text("Выберите гранату", reply_markup=kb.grenades_keyboard(response).as_markup())
    else:
        await callback.message.delete()
        await callback.message.answer(f"На карте {map} гранат нет")
        await callback.message.answer(f"Удаление гранат", reply_markup=kb.maps_keyboard().as_markup())


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


@router.callback_query(lambda callback: callback.data == 'cancel', StateFilter("*"))
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    """Отмена всех FSM и удаление последнего сообщения"""
    await state.clear()
    await callback.message.answer("Действие отменено")
    await callback.message.delete()