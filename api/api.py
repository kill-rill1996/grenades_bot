import io
import json
from typing import BinaryIO

import requests
from aiogram.types import BufferedInputFile

import config
from models.grenade import Grenades, StatusError, Grenade, StatusOK, Image, CreateGrenadeModel


class API:
    def __init__(self, domen: str):
        self.domen = domen
        self.headers = {
            "Content-Type": "application/json"
        }

    def _get_request(self, url: str, params) -> str | dict:
        response = requests.get(self.domen + url, headers=self.headers, params=params)
        if response.status_code != 200:
            return self._handle_error(response)
        return response.json()

    def _post_request(self, url: str, body: dict) -> dict:
        response = requests.post(self.domen + url, json=body, headers=self.headers)
        if response.status_code != 201:
            return self._handle_error(response)
        return response.json()

    def _delete_request(self, url: str) -> dict:
        response = requests.delete(self.domen + url, headers=self.headers)
        if response.status_code != 200:
            return self._handle_error(response)
        return response.json()

    def _patch_request(self, url: str, body: dict) -> dict:
        response = requests.patch(self.domen + url, json=body, headers=self.headers)
        if response.status_code != 200:
            return self._handle_error(response)
        return response.json()

    def _post_image_request(self, url: str, body: BinaryIO) -> dict:
        files = {'grenadeImage': body.getvalue()}

        response = requests.post(self.domen + url, files=files)

        if response.status_code != 200:
            return self._handle_error(response)
        return response.json()

    def _get_image_request(self, url: str) -> bytes:
        response = requests.get(url)
        return response.content

    def send_request(self, url: str, method: str, params: dict = None, body: dict | BinaryIO = None) -> dict | bytes:
        if method == "GET":
            response = self._get_request(url, params)
        elif method == "POST":
            response = self._post_request(url, body)
        elif method == "POST_IMAGE":
            response = self._post_image_request(url, body=body)
        elif method == "DELETE":
            response = self._delete_request(url)
        elif method == "GET_IMAGE":
            response = self._get_image_request(url)
        else:
            response = self._patch_request(url, body)
        return response

    def get_grenades(self, params: dict) -> StatusError | Grenades:
        """Получение всех гранат по заданным параметрам"""
        response = self.send_request("grenades/", "GET", params)

        if response.get("error") is not None:
            return StatusError.model_validate(response)

        return Grenades.model_validate(response)

    def get_grenade(self, grenade_id: str) -> Grenade | StatusError:
        """Получение гранаты по id"""
        response = self.send_request(f"grenades/{grenade_id}", "GET")

        if response.get("error") is not None:
            return StatusError.model_validate(response)

        return Grenade.model_validate(response["grenade"])

    def get_image(self, url: str) -> bytes:
        """Получение картинки по url"""
        url = url.replace("http://localhost:4000/v1/", config.DOMEN)

        response = self.send_request(url, "GET_IMAGE")
        return response

    def delete_image(self, image_id: str) -> StatusOK | StatusError:
        """Удаление фотографии у гранаты"""
        response = self.send_request(f"images/{image_id}", "DELETE")

        if response.get("error") is not None:
            return StatusError.model_validate(response)

        return StatusOK.model_validate(response)

    def delete_grenade(self, grenade_id: str) -> StatusOK | StatusError:
        """Удаление гранаты по id"""
        response = self.send_request(f"grenades/{grenade_id}", "DELETE")

        if response.get("error") is not None:
            return StatusError.model_validate(response)

        return StatusOK.model_validate(response)

    def update_grenade(self, grenade_id: int, updated_data: dict) -> StatusOK | StatusError:
        """Обновление гранаты"""
        response = self.send_request(url=f"grenades/{grenade_id}", method="PATCH", body=updated_data)

        if response.get("error") is not None:
            return StatusError.model_validate(response)

        return StatusOK.model_validate({"message": "grenade successfully modified"})

    def create_grenade(self, grenade: CreateGrenadeModel) -> Grenade | StatusError:
        """Создание гранаты"""
        body = {
            "map": grenade.map,
            "side": grenade.side,
            "type": grenade.type,
            "title": grenade.title,
            "description": grenade.description
        }
        response = self.send_request(url=f"grenades/", method="POST", body=body)

        if response.get("error") is not None:
            return StatusError.model_validate(response)

        return Grenade.model_validate(response["grenade"])

    def create_image(self, grenade_id: int, image: BinaryIO) -> Image | StatusError:
        """Добавление изображения к гранате"""
        response = self.send_request(url=f"grenades/{grenade_id}/images", method="POST_IMAGE", body=image)

        if response.get("error") is not None:
            return StatusError.model_validate(response)

        return Image.model_validate(response["image"])

    def _handle_error(self, response: requests.Response) -> dict:
        code = response.status_code
        if code == 500:
            message = {"error": "Ошибка на сервере. Повторите попытку позже."}
        elif code == 404:
            message = {"error": "Данные не найдены."}
        elif code == 400:
            message = {"error": "Переданы неверные данные."}
        elif code == 402:
            message = {"error": "Неверный формат переданных данных."}
        elif code == 409:
            message = {"error": "Ошибка. Попробуйте еще раз."}
        elif code == 405:
            message = {"error": "Метод запроса по данному URL запрещен."}
        elif code == 429:
            message = {"error": "Лимит запросов превышен."}
        else:
            message = {"error": "Непредвиденная ошибка на сервере."}
        return message


