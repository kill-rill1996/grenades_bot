import requests


class API:
    def __init__(self, domen: str):
        self.domen = domen

    def _get_request(self, url: str) -> dict:
        response = requests.get(self.domen + url)
        if response.status_code != 200:
            pass
        return response.json()

    def send_request(self, url: str, method: str, headers: dict = None, params: dict = None) -> None:
        if method == "GET":
            response = self._get_request(url)
            print(type(response))
            print(response)

    def get_grenade(self) -> dict:
        pass


