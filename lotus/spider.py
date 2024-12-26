import json
from curl_cffi import CurlHttpVersion
from curl_cffi.requests.impersonate import *
from curl_cffi.requests.session import *
from lotus.request import Request
from lotus.attr import AttrMixin, Config
from lotus.response import Response
from typing import Optional

from lotus.utils import dict_to_json


"""
requests 参数
    method: HttpMethod,
    url: str,
    params: Optional[Union[Dict, List, Tuple]] = None,
    data: Optional[Union[Dict[str, str], List[Tuple], str, BytesIO, bytes]] = None,
    json: Optional[dict] = None,
    headers: Optional[HeaderTypes] = None,
    cookies: Optional[CookieTypes] = None,
    files: Optional[Dict] = None,
    auth: Optional[Tuple[str, str]] = None,
    timeout: Union[float, Tuple[float, float]] = 30,
    allow_redirects: bool = True,
    max_redirects: int = 30,
    proxies: Optional[ProxySpec] = None,
    proxy: Optional[str] = None,
    proxy_auth: Optional[Tuple[str, str]] = None,
    verify: Optional[bool] = None,
    referer: Optional[str] = None,
    accept_encoding: Optional[str] = "gzip, deflate, br, zstd",
    content_callback: Optional[Callable] = None,
    impersonate: Optional[BrowserTypeLiteral] = None,
    ja3: Optional[str] = None,
    akamai: Optional[str] = None,
    extra_fp: Optional[Union[ExtraFingerprints, ExtraFpDict]] = None,
    thread: Optional[ThreadType] = None,
    default_headers: Optional[bool] = None,
    default_encoding: Union[str, Callable[[bytes], str]] = "utf-8",
    quote: Union[str, Literal[False]] = "",
    curl_options: Optional[dict] = None,
    http_version: Optional[CurlHttpVersion] = None,
    debug: bool = False,
    interface: Optional[str] = None,
    cert: Optional[Union[str, Tuple[str, str]]] = None,
    stream: bool = False,
    max_recv_speed: int = 0,
    multipart: Optional[CurlMime] = None,
"""


class Spider(AttrMixin):

    def __init__(self, method: HttpMethod, url: str, config: Optional[Config] = None) -> None:
        self._config = self.config()
        self._config['url'] = url
        self._config['method'] = method
        if config is not None:
            self.update_config(**config)
        super().__init__(self._config)

    # config 默认值

    def config(self) -> dict:
        return {
            "timeout": 30,
            "allow_redirects": True,
            "max_redirects": 30,
            "proxies": None,
            "verify": False,
            "referer":  None,
            "accept_encoding": "gzip, deflate, br, zstd",
            "impersonate": DEFAULT_CHROME,
            "default_encoding": "utf-8",
            "quote":  "",
            "http_version": CurlHttpVersion.V1_1,
            "debug":  False,
            "stream": False,
            "max_recv_speed": 0,
            # 自定义属性, 非 curl_cffi 的属性
            "retry_time": 5
        }

    # 特定参数的默认实现，可以在子类中重写
    def headers(self) -> dict | None:
        return None

    def params(self) -> dict | None:
        return None

    def data(self) -> dict | str | bytes | None:
        return None

    def json(self) -> dict | None:
        return None

    def cookies(self) -> dict | None:
        return None

    def make_request(self) -> Request:
        """子类介入时机, 通过 set 或者 update 的方式改变 self.xxx 的值"""
        self.pre_request()

        """构建请求体"""
        self._config['params'] = self.get_params()
        self._config['headers'] = self.get_headers()
        # 如果此处传递 json, 直接截断
        json_data = self.get_json()
        # 包含了 json 就肯定不能包含 data, 互斥
        if json_data is not None:
            self._config['data'] = dict_to_json(json_data).encode("utf-8")
            assert self.get_data() is None
        else:
            self._config['data'] = self.get_data()
        self._config['cookies'] = self.get_cookies()
        return Request(**self._config)

    # 子类按需要重写, 提供了 request 的 hook
    def pre_request(self) -> None:
        return None

    def download(self) -> dict:
        retry_times = self._config.get("retry_times", 3)
        while retry_times:
            try:
                result = {}
                parent_response = self.make_request().download()
                response = Response.from_parent(parent_response)
                result['is_next'] = self.is_next(response)
                result['is_ignore'] = self.is_ignore(response)
                result['is_retry'] = self.is_retry(response)
                result['data'] = self.parse(response)
                result['is_update'] = self.is_update(response)
                # self.save_data(result)
                return result
            except Exception as e:
                retry_times -= 1
                print(f"download error {e}")

    async def async_download(self) -> dict:
        retry_times = self._config.get("retry_times", 3)
        while retry_times:
            try:
                result = {}
                response = await self.make_request().async_download()
                result['has_next'] = self.has_next(response)
                result['ignore'] = self.ignore(response)
                result['retry'] = self.retry(response)
                result['data'] = self.parse(response)
                result['is_update'] = self.is_update(response)
                # self.save_data(result)
                return result
            except Exception as e:
                retry_times -= 1

    # 子类重写 解析页面数据
    def parse(self, response: Response) -> dict | str | None:
        return None

    # 子类重写, 是否需要翻页
    def is_next(self, response: Response) -> bool | None:
        return None

    # 子类重写, 是否需要再次请求
    def is_retry(self, response: Response) -> bool | None:
        return None

    # 子类重写, 是否需要忽略该请求
    def is_ignore(self, response: Response) -> bool | None:
        return None

    # 子类重写, 是否需要根据本次响应来更新下一次的参数
    def is_update(self, response: Response) -> dict | str | None:
        return None
