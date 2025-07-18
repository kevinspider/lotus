from typing import (
    Callable,
    Dict,
    Literal,
    Optional,
    Tuple,
    TypedDict,
    Union,
    List,
    Unpack,
)
from curl_cffi import CurlHttpVersion
from curl_cffi.requests.impersonate import (
    BrowserTypeLiteral,
    ExtraFingerprints,
    ExtraFpDict,
)
from curl_cffi.requests.session import (
    HttpMethod,
    BytesIO, # type: ignore
    HeaderTypes, # type: ignore
    CookieTypes, # type: ignore
    ProxySpec,
    ThreadType,
    CurlMime, # type: ignore
)


class Config(TypedDict, total=False):
    method: HttpMethod
    url: str
    params: Optional[Union[Dict, List, Tuple]]
    data: Optional[Union[Dict[str, str], List[Tuple], str, BytesIO, bytes]]
    json: Optional[dict]
    headers: Optional[HeaderTypes]
    cookies: Optional[CookieTypes]
    files: Optional[Dict]
    auth: Optional[Tuple[str, str]]
    timeout: Union[float, Tuple[float, float]]
    allow_redirects: bool
    max_redirects: int
    proxies: Optional[ProxySpec]
    proxy_error_ignore: bool
    proxy: Optional[str]
    proxy_auth: Optional[Tuple[str, str]]
    verify: Optional[bool]
    referer: Optional[str]
    accept_encoding: Optional[str]
    content_callback: Optional[Callable]
    impersonate: Optional[BrowserTypeLiteral]
    ja3: Optional[str]
    akamai: Optional[str]
    extra_fp: Optional[Union[ExtraFingerprints, ExtraFpDict]]
    thread: Optional[ThreadType]
    default_headers: Optional[bool]
    default_encoding: Union[str, Callable[[bytes], str]]
    quote: Union[str, Literal[False]]
    curl_options: Optional[dict]
    http_version: Optional[CurlHttpVersion]
    debug: bool
    interface: Optional[str]
    cert: Optional[Union[str, Tuple[str, str]]]
    stream: bool
    max_recv_speed: int
    multipart: Optional[CurlMime]
    # add by kevin
    retry_times: int
    log_level: Literal["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
    log_file: Optional[str]


class AttrMixin:

    def __init__(self, config: Optional[Config] = None):
        self._params = None
        self._data = None
        self._headers = None
        self._json = None
        self._cookies = None
        self._config = Config()

        # 初始化懒加载的属性
        self._params: Optional[dict] = self.params()
        self._data: dict | str | bytes | None = self.data()
        self._headers: Optional[dict] = self.headers()
        self._json: Optional[dict] = self.json()
        self._cookies: Optional[dict] = self.cookies()
        self._config: Config = self.config()
        if config is not None:
            self.update_config(**config)

    # config 属性

    def get_config(self, key: Optional[Config.keys] = None): # type: ignore
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
        if self._params is None:
            self._params = self.params()
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
    def get_data(self) -> dict | str | bytes | None:
        if self._data is None:
            self._data = self.data()
        return self._data

    def set_data(self, value: dict) -> dict | None:
        self._data = value
        return self._data

    def update_data(self, value: dict) -> dict | None:
        if self._data is None:
            self._data = value
        else:
            if isinstance(self._data, dict):
                self._data.update(value)
            else:
                raise TypeError("data is not dict")
        return self._data

    # headers 属性
    def get_headers(self) -> dict | None:
        if self._headers is None:
            self._headers = self.headers()
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
        if self._json is None:
            self._json = self.json()
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
        if self._cookies is None:
            self._cookies = self.cookies()
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

    def data(self) -> dict | str | bytes | None:
        return None

    def headers(self) -> dict | None:
        return None

    def json(self) -> dict | None:
        return None

    def cookies(self) -> dict | None:
        return None

    def config(self) -> Config:
        return {}
