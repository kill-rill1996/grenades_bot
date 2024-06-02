import requests
from aiogram import types
from aiogram import Router

from app import api

router = Router()


@router.message(lambda message: message.text == "1")
async def req_get(message: types.Message) -> None:
    grenades = api.send_request("grenades/", "GET")
    msg = f"{grenades}"
    await message.answer(msg)


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


@router.message()
async def echo(message: types.Message) -> None:
    await message.answer(f'{message.text}!')
