from typing import Callable, Dict, Literal, Optional, Tuple, TypedDict, Union
from curl_cffi import CurlHttpVersion
from curl_cffi.requests.impersonate import *
from curl_cffi.requests.session import *


class Config(TypedDict, total=False):
    method: HttpMethod
    url: str
    params: Optional[Union[Dict, List, Tuple]] = None
    data: Optional[Union[Dict[str, str],
                         List[Tuple], str, BytesIO, bytes]] = None
    json: Optional[dict] = None
    headers: Optional[HeaderTypes] = None
    cookies: Optional[CookieTypes] = None
    files: Optional[Dict] = None
    auth: Optional[Tuple[str, str]] = None
    timeout: Union[float, Tuple[float, float]] = 30
    allow_redirects: bool = True
    max_redirects: int = 30
    proxies: Optional[ProxySpec] = None
    proxy: Optional[str] = None
    proxy_auth: Optional[Tuple[str, str]] = None
    verify: Optional[bool] = False
    referer: Optional[str] = None
    accept_encoding: Optional[str] = "gzip, deflate, br, zstd"
    content_callback: Optional[Callable] = None
    impersonate: Optional[BrowserTypeLiteral] = None
    ja3: Optional[str] = None
    akamai: Optional[str] = None
    extra_fp: Optional[Union[ExtraFingerprints, ExtraFpDict]] = None
    thread: Optional[ThreadType] = None
    default_headers: Optional[bool] = None
    default_encoding: Union[str, Callable[[bytes], str]] = "utf-8"
    quote: Union[str, Literal[False]] = ""
    curl_options: Optional[dict] = None
    http_version: Optional[CurlHttpVersion] = None
    debug: bool = False
    interface: Optional[str] = None
    cert: Optional[Union[str, Tuple[str, str]]] = None
    stream: bool = False
    max_recv_speed: int = 0
    multipart: Optional[CurlMime] = None


class AttrMixin:
    def __init__(self):
        # 初始化懒加载的属性
        self._params: Optional[dict] = self.params()
        self._data: Optional[dict] = self.data()
        self._headers: Optional[dict] = self.headers()
        self._json: Optional[dict] = self.json()
        self._cookies: Optional[dict] = self.cookies()
        self._config: Config = self.config()

    # config 属性

    def get_config(self, key: Optional[Config.keys] = None):
        if key is None:
            return self._config
        else:
            return self._config[key]

    def update_config(self, **ksargs: Unpack[Config]):
        if self._config is None:
            self._config = ksargs
        else:
            self._config.update(ksargs)
        return self._config

    # params 属性
    def get_params(self) -> dict | None:
        return self._params

    def set_params(self, value: dict) -> dict | None:
        self._params = value
        return self._params

    def update_params(self, value: dict) -> dict | None:
        if self._params is None:
            self._params = value
        else:
            self._params.update(value)
        return self._params

    # data 属性
    def get_data(self) -> dict | None:
        return self._data

    def set_data(self, value: dict) -> dict | None:
        self._data = value
        return self._data

    def update_data(self, value: dict) -> dict | None:
        if self._data is None:
            self._data = value
        else:
            self._data.update(value)
        return self._data

    # headers 属性
    def get_headers(self) -> dict | None:
        return self._headers

    def set_headers(self, value: dict) -> dict | None:
        self._headers = value
        return self._headers

    def update_headers(self, value: dict) -> dict | None:
        if self._headers is None:
            self._headers = value
        else:
            self._headers.update(value)
        return self._headers

    # json 属性
    def get_json(self) -> dict | None:
        return self._json

    def set_json(self, value: dict) -> dict | None:
        self._json = value
        return self._json

    def update_json(self, value: dict) -> dict | None:
        if self._json is None:
            self._json = value
        else:
            self._json.update(value)
        return self._json

    # cookies 属性
    def get_cookies(self) -> dict | None:
        return self._cookies

    def set_cookies(self, value: dict) -> dict | None:
        self._cookies = value
        return self._cookies

    def update_cookies(self, value: dict) -> dict | None:
        if self._cookies is None:
            self._cookies = value
        else:
            self._cookies.update(value)
        return self._cookies

    # 默认实现的方法，子类可以重写以自定义行为
    def params(self) -> dict | None:
        return None

    def data(self) -> dict | None:
        return None

    def headers(self) -> dict | None:
        return None

    def json(self) -> dict | None:
        return None

    def cookies(self) -> dict | None:
        return None

    def config(self) -> dict:
        return {}
