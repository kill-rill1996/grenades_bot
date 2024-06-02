import base64
import json

from aiogram import types
from aiogram import Router
from aiogram.types import InputFile, FSInputFile, BufferedInputFile
from pydantic import ValidationError

from models.grenade import Grenade, Grenades

from app import api

router = Router()


@router.message(lambda message: message.text == "1")
async def get_grenades_handle(message: types.Message) -> None:
    response = api.send_request("grenades/1", "GET")

    if response.get("error") is not None:
        await message.answer(response["error"])

    try:
        grenades = Grenades.model_validate(response)
        msg = ""
        for grenade in grenades.grenades:
            msg += f"ID: {grenade.id}, title: {grenade.title}, type: {grenade.type}, side: {grenade.side}, {grenade.images}\n\n"
        await message.answer(msg)

    except ValidationError:
        await message.answer("Не получилось получить гранаты")


@router.message(lambda message: message.text == "2")
async def req_get(message: types.Message) -> None:
    body = {
            "map": "Mirage",
            "title": "Conn molotov",
            "description": "left mouse key",
            "type": "molotov",
            "side": "T"
        }
    created_grenade = api.send_request("grenades/", "POST", body=body)
    msg = f"{created_grenade}"
    await message.answer(msg)


@router.message(lambda message: message.text == "3")
async def req_get(message: types.Message) -> None:
    grenades = api.send_request("grenades/5", "DELETE")
    msg = f"{grenades}"
    await message.answer(msg)


@router.message(lambda message: message.text == "4")
async def req_get(message: types.Message) -> None:
    body = {
        "map": "Ancient",
        "title": "Mid grenade",
        "description": "jumpthrow",
        "type": "smoke",
        "side": "CT"
    }
    grenades = api.send_request("grenades/4", "PATCH", body=body)
    msg = f"{grenades}"
    await message.answer(msg)


@router.message(lambda message: message.text == "5")
async def req_get(message: types.Message) -> None:
    response = api.send_request("http://localhost:4000/v1/image/1717344283796283.jpg", "GET_IMAGE")
    image = BufferedInputFile(response.content, filename="image")

    await message.answer_photo(image)


@router.message()
async def echo(message: types.Message) -> None:
    await message.answer(f'{message.text}!')
