import requests
from aiogram import types
from aiogram import Router

from app import api

router = Router()


@router.message(lambda message: message.text == "1")
async def req_get(message: types.Message) -> None:
    api.send_request("grenades/", "GET")
    # print(requests.get("http://host.docker.internal:4000/v1/healthcheck"))
    await message.answer("запрос отправлен")


@router.message()
async def echo(message: types.Message) -> None:
    await message.answer(f'{message.text}!')
