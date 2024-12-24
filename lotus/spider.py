
from typing import overload, Union
from lotus.request import Request
from lotus.response import Response


class Spider():

    def __init__(self, method: str, url: str) -> None:
        self._url = url
        self._method = method
        self._params = {}
        self._headers = {}
        self._proxies = {}
        self._data = {}
        self._json = {}
        self.config = {
            "retry_times": 3,
            "timeout": 10,
            "verify": False
        }

    def headers(self) -> dict | None:
        return None

    def params(self) -> dict | None:
        return None

    def proxies(self) -> dict | None:
        return None

    def data(self) -> dict | None:
        return None

    def json(self) -> dict | None:
        return None

    def make_request(self) -> Request:
        params = self.params()
        headers = self.headers()
        proxies = self.proxies()
        json = self.json()
        data = self.data()
        return Request(self._url, self._method, params, headers, json, data, proxies, self.config['timeout'], self.config['retry_times'], self.config['verify'])

    def download(self) -> dict:
        result = {}
        response = self.make_request().download()
        result['has_next'] = self.has_next(response)
        result['ignore'] = self.ignore(response)
        result['retry'] = self.retry(response)
        result['data'] = self.parse(response)
        return result

    def parse(self, response: Response) -> any:
        pass

    def has_next(self, response: Response) -> bool:
        return False

    def retry(self, response: Response) -> bool:
        return False

    def ignore(self, response: Response) -> bool:
        return False
