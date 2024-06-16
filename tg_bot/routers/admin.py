from aiogram import types, F
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from models.grenade import StatusOK
from tg_bot.fsm_states import FSMCreateGrenade, FSMUpdateGrenade
from tg_bot.middlewares import CheckIsAdminMiddleware
from config import ADMINS
from api import grenades_api as api
from tg_bot.keyboards import admin as kb
from tg_bot.messages.admin import update_grenade_message, change_field_grenade_message, successful_grenade_changes_message

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
    # удаление записанных сообщений
    data = await state.get_data()
    if data.get("old_messages"):
        for message in data["old_messages"]:
            try:
                await message.delete()
            except TelegramBadRequest:
                continue

    await state.clear()
    await callback.message.answer("Действие отменено")
    try:
        await callback.message.delete()

    except TelegramBadRequest:
        pass

# UPDATE GRENADE
@router.message(Command("update_grenade"))
async def update_grenade_handler(message: types.Message, state: FSMContext) -> None:
    """Изменение гранат, первоначальная клавиатура с выбором гранаты"""
    await state.set_state(FSMUpdateGrenade.grenade)

    all_grenades = api.get_grenades(params={"sort": "map"})
    await message.answer("Изменение гранат", reply_markup=kb.update_grenade_keyboard(all_grenades).as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "update-grenade", FSMUpdateGrenade.grenade)
async def choose_update_field_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор поля для изменения у гранаты"""
    grenade = api.get_grenade(callback.data.split("_")[1])

    # записываем данные о гранате в state
    await state.update_data(grenade=grenade)
    await state.set_state(FSMUpdateGrenade.field)

    msg = update_grenade_message(grenade)
    await callback.message.edit_text(msg, reply_markup=kb.fields_to_change_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "update-field", FSMUpdateGrenade.field)
async def get_changes_in_filed_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Внесение изменений в выбранное поле"""
    field_to_changed = callback.data.split("_")[1]
    await state.update_data(field=field_to_changed)

    data = await state.get_data()

    await state.set_state(FSMUpdateGrenade.updating)

    old_messages = []

    # в случае изменения фотографий
    if field_to_changed == "images":
        # 1 image
        if len(data["grenade"].images) == 1:
            await callback.message.delete()

            image_response = api.get_image(data["grenade"].images[0].image_url)
            image = BufferedInputFile(image_response, filename="image")
            old_message_photo = await callback.message.answer_photo(image, reply_markup=kb.delete_image_keyboard(data["grenade"].images[0].id).as_markup())
            old_messages.append(old_message_photo)

        # > 1 images
        else:
            await callback.message.delete()
            for image in data["grenade"].images:
                image_id = image.id
                image_response = api.get_image(image.image_url)
                image = BufferedInputFile(image_response, filename="image")
                message = await callback.message.answer_photo(image, reply_markup=kb.delete_image_keyboard(image_id).as_markup())
                old_messages.append(message)

        old_message_cancel = await callback.message.answer("Выберите фотографию для удаления", reply_markup=kb.cancel_keyboard().as_markup())
        old_messages.append(old_message_cancel)
        # добавляем в state
        await state.update_data(old_messages=old_messages)

    # в случае изменения всех остальных полей
    else:
        # формируем сообщение со старым значением поля
        msg = change_field_grenade_message(data=data)

        # для приема информации из сообщения
        if data["field"] in ["title", "description"]:
            keyboard = kb.fields_to_change_title_description()
            old_message_desc_title = await callback.message.edit_text(msg, reply_markup=keyboard.as_markup())
            old_messages.append(old_message_desc_title)
            # добавляем в state
            await state.update_data(old_messages=old_messages)

        # для выбора с кнопок
        elif data["field"] in ["type", "side", "map"]:
            keyboard = kb.fields_to_change_side_type_map(data)
            await callback.message.edit_text(msg, reply_markup=keyboard.as_markup())


@router.message(FSMUpdateGrenade.updating)
@router.callback_query(FSMUpdateGrenade.updating)
async def change_grenade_handler(event: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    """Получение переданных (в сообщении или с кнопок) изменений и внесение их в БД"""

    # получение измененных данных
    if type(event) == types.Message:
        changed_data = event.text
    else:
        changed_data = event.data
        # убираем приписку из callback кнопок (map_, type_, side_, ...)
        changed_data = changed_data.split("_")[1]

    await state.update_data(changed_data=changed_data)
    data = await state.get_data()

    # удаление фотографии
    if data["field"] == "images":
        response = api.delete_image(changed_data)

    # изменение любых других полей
    else:
        # формируем данные для отправки
        data_to_send = {
            "map": data["grenade"].map,
            "title": data["grenade"].title,
            "description": data["grenade"].description,
            "type": data["grenade"].type,
            "side": data["grenade"].side,
            }

        # изменяем необходимое поле
        data_to_send[data["field"]] = data["changed_data"]

        # отправляем запрос на сервер с новыми данными
        response = api.update_grenade(data["grenade"].id, data_to_send)

    # удаляем старые сообщения
    if data.get("old_messages"):
        for message in data["old_messages"]:
            try:
                await message.delete()
            except TelegramBadRequest:
                continue

    # проверяем вернул ли запрос ошибку
    if type(response) == StatusOK:
        # msg = successful_grenade_changes_message(data_to_send)
        msg = "<b>Граната успешно изменена</b>"
    else:
        msg = "<b>Ошибка при изменении гранаты</b>"

    await state.clear()

    # удаляем предыдущее если CallbackQuery
    # if type(event) == types.CallbackQuery:
    #     await event.message.delete()

    # отправляем ответ
    if type(event) == types.Message:
        await event.answer(msg)
    else:
        await event.message.answer(msg)


