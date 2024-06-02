import requests


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

    def _get_image_request(self, url: str):
        response = requests.get(url)
        return response

    def send_request(self, url: str, method: str, params: dict = None, body: dict = None) -> dict:
        if method == "GET":
            response = self._get_request(url, params)
        elif method == "POST":
            response = self._post_request(url, body)
        elif method == "DELETE":
            response = self._delete_request(url)
        elif method == "GET_IMAGE":
            response = self._get_image_request(url)
        else:
            response = self._patch_request(url, body)
        return response

    def get_grenade(self) -> dict:
        pass

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


