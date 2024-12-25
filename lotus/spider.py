
from typing import Literal, Union
from typing_extensions import Unpack
from lotus.request import Request
from lotus.response import Response
from curl_cffi.const import CurlHttpVersion
from curl_cffi.requests.session import BaseSessionParams


class Spider():

    def __init__(self, method: Literal["post", "get"], url: str) -> None:
        self._url = url
        self._method = method
        self._config = {}

    def set_config(self, **ksargs: Unpack[BaseSessionParams]):
        for key, value in ksargs.items():
            self._config.update({key: value})        

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
    
    def prepare_request(self) -> dict | None:
        return None

    def make_request(self) -> Request:
        params = self.params()
        headers = self.headers()
        json = self.json()
        data = self.data()
        proxies = self.proxies()
        return Request(self._url, self._method, params, headers, json, data, proxies)

    def download(self) -> dict:
        result = {}
        response = self.make_request().download()
        result['has_next'] = self.has_next(response)
        result['ignore'] = self.ignore(response)
        result['retry'] = self.retry(response)
        result['data'] = self.parse(response)
        return result

    def parse(self, response: Response) -> dict:
        pass

    def has_next(self, response: Response) -> bool:
        return False

    def retry(self, response: Response) -> bool:
        return False

    def ignore(self, response: Response) -> bool:
        return False
