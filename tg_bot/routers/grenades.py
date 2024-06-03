from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, BufferedInputFile

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

    await message.answer("Выберите карту:", reply_markup=kb.maps_keyboard().as_markup())


@router.message(Command("maps"))
async def all_maps_handler(message: types.Message) -> None:
    """Сообщение с выводом карт"""
    await message.edit_text("Выберите карту:", reply_markup=kb.maps_keyboard().as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "map")
async def sides_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор стороны после выбора карты"""
    await state.set_state(FSMGrenades.side)

    map = callback.data.split("_")[1]
    await state.update_data(map=map)

    await callback.message.edit_text("Выберите сторону:", reply_markup=kb.side_keyboard().as_markup())


@router.callback_query(FSMGrenades.side)
async def grenade_type_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Выбор типа гранаты"""
    await state.set_state(FSMGrenades.type)
    side = callback.data.split("_")[1]
    await state.update_data(side=side)

    await callback.message.edit_text("Выберите тип гранаты", reply_markup=kb.grenade_type_keyboard().as_markup())


@router.callback_query(FSMGrenades.type)
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

    if type(response) == models.grenade.Error:
        await callback.message.edit_text(response.error)

    elif not response.grenades:
        await callback.message.edit_text("По запросу гранат не найдено")
        await callback.message.answer("Выберите карту:", reply_markup=kb.maps_keyboard().as_markup())

    else:
        await callback.message.edit_text("Выберите гранату",
                                         reply_markup=kb.grenade_titles_keyboard(response.grenades).as_markup())


@router.callback_query(lambda callback: callback.data.split("_")[0] == "grenadeId")
async def grenade_handler(callback: types.CallbackQuery) -> None:
    grenade_id = callback.data.split("_")[1]
    print(grenade_id)
    response = api.get_grenade(grenade_id)
    print(response)

    if type(response) == models.grenade.Error:
        await callback.message.edit_text(response.error)

    else:
        msg = f"{response.title} {response.description} {response.type}"

        if len(response.images) == 1:
            await callback.message.delete()

            image_response = api.get_image(response.images[0].image_url)
            image = BufferedInputFile(image_response, filename="image")
            await callback.message.answer_photo(image, msg)
            await callback.message.answer(msg)
        # else:
        #     for image in response.images:
        #         await




