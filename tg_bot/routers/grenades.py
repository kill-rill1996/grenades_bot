from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

import models.grenade
from api import grenades_api as api
from tg_bot.keyboards import grenades as kb
from tg_bot.messages import grenades as ms
from tg_bot.fsm_states import FSMGrenades

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    """Стартовое сообщение и сообщение с выбором карт"""
    sticker = FSInputFile("tg_bot/static/stickers/hello.webm")
    await message.answer_sticker(sticker)
    await message.answer(ms.hello_message())

    await message.answer("Выберите карту", reply_markup=kb.maps_keyboard().as_markup())


@router.message(Command("grenades"))
@router.callback_query(lambda callback: callback.data == "back-to-maps")
async def all_maps_handler(message: types.Message | types.CallbackQuery, state: FSMContext) -> None:
    """Сообщение с выводом карт"""
    if type(message) == types.CallbackQuery:
        await state.clear()
        await message.message.edit_text("Выберите карту", reply_markup=kb.maps_keyboard().as_markup())
    else:
        await message.answer("Выберите карту", reply_markup=kb.maps_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "map"
                       or (callback.data == "back-to-sides" and FSMGrenades.type))
async def sides_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор стороны после выбора карты"""
    await state.set_state(FSMGrenades.side)

    # map из fsm data по кнопке Назад
    data = await state.get_data()
    map = data.get("map")

    # для планового выбора гранат
    if not map:
        map = callback.data.split("_")[1]
        await state.update_data(map=map)

    await callback.message.edit_text(f"<b>{map.upper()}</b>", reply_markup=kb.side_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "side", FSMGrenades.side)
@router.callback_query(lambda callback: callback.data.split("_")[0] == "back-to-type")
async def grenade_type_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор типа гранаты"""
    # для кнопки Назад
    await state.set_state(FSMGrenades.type)

    if callback.data.split("_")[0] == "back-to-type":
        data = callback.data.split("_")[1:]
        await state.update_data(map=data[1])
        await state.update_data(side=data[2])

        await callback.message.edit_text(f"<b>{data[1].upper()}</b> | <b>{data[2]}</b>",
                                         reply_markup=kb.grenade_type_keyboard().as_markup())

    # для планового выбора
    else:
        side = callback.data.split("_")[1]
        data = await state.get_data()
        await state.update_data(side=side)

        await callback.message.edit_text(f"<b>{data['map'].upper()}</b> | <b>{side}</b>", reply_markup=kb.grenade_type_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "type", FSMGrenades.type)
async def grenades_title_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Вывод отсортированных гранат"""
    grenade_type = callback.data.split("_")[1]
    await state.update_data(type=grenade_type)

    fsm_data = await state.get_data()
    params = {
        "type": fsm_data["type"],
        "map": fsm_data["map"],
        "side": fsm_data["side"],
    }

    await state.clear()

    response = api.get_grenades(params)

    if type(response) == models.grenade.StatusError:
        await callback.message.edit_text(response.error)

    elif not response.grenades:
        await callback.message.edit_text("По запросу гранат не найдено")
        await callback.message.answer("Выберите карту:", reply_markup=kb.maps_keyboard().as_markup())

    else:
        await callback.message.edit_text(f"<b>{params['map'].upper()}</b> | <b>{params['side'].upper()}</b> | <b>{params['type'].upper()}</b>",
                                         reply_markup=kb.grenade_titles_keyboard(response.grenades, params).as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "grenadeId")
async def grenade_handler(callback: types.CallbackQuery) -> None:
    grenade_id = callback.data.split("_")[1]
    response = api.get_grenade(grenade_id)

    if type(response) == models.grenade.StatusError:
        await callback.message.edit_text(response.error)

    else:
        msg = f"<b>{response.title}</b>\n\n{response.description}"

        if len(response.images) == 1:
            await callback.message.delete()

            image_response = api.get_image(response.images[0].image_url)
            image = BufferedInputFile(image_response, filename="image")
            await callback.message.answer_photo(image, msg)

        else:
            album_builder = MediaGroupBuilder(caption=msg)

            for image in response.images:
                image_response = api.get_image(image.image_url)
                image = BufferedInputFile(image_response, filename="image")
                album_builder.add(type="photo", media=image)

            await callback.message.answer_media_group(
                media=album_builder.build()
            )



