import sys
import traceback
from loguru import logger
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

logger = logger

# 定义一个函数来配置 logger
def configure_logger(log_file: str = None, log_level: str = "DEBUG"):
    # 添加新的处理器
    if log_file:
        # 移除所有现有的处理器
        logger.remove()
        logger.add(sink=sys.stdout, level=log_level, enqueue=True)
        logger.add(sink=log_file, level=log_level, enqueue=True)
        
    else:
        # 移除所有现有的处理器
        logger.remove()
        logger.add(sink=sys.stdout, level=log_level, enqueue=True)


class Spider(AttrMixin):
    _log_configed = False
    
    def __init__(self, method: HttpMethod, url: str, config: Optional[Config] = None) -> None:
        # 初始化 config, 获取默认值
        self._config = self.config()
        # 添加 url 和 method
        self._config['url'] = url
        self._config['method'] = method
        
        # 加载用户自定义的 config
        if config is not None:
            self.update_config(**config)
        
        # 配置 logger
        if Spider._log_configed is False:
            configure_logger(self._config.get("log_file"), self._config.get("log_level"))
            Spider._log_configed = True

        super().__init__(self._config)
    
    # config 默认值定义在 Spider 中; Config 类型定义在 AttrMixin 中
    def config(self) -> Config:
        config: Config = {
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
            # 自定义属性, 非 curl_cffi 的属性, 会在 Request() 实例化的时候, 被 Request 过滤掉, 不会传递给 Request 和 Session
            "retry_times": 5,
            "log_file": None,
            "log_level": "DEBUG"
        }
        return config

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

    def download(self) -> dict | None:
        retry_times = self._config.get("retry_times")
        while retry_times:
            try:
                parent_response = self.make_request().download()
                response = Response.from_parent(parent_response)
                final_result = self.parse(response)
                return final_result
            except Exception as e:
                retry_times -= 1
                logger.debug(f"Download error {e}, caused from")
                if self._config.get("log_level") == "DEBUG":
                    traceback.print_exc()
                    logger.debug("this error will retry ...")
        logger.critical(f"Ignore request, retry_time is {self._config.get('retry_times')}, url={self._config.get('url')}")


    # async def async_download(self) -> dict:
    #     retry_times = self._config.get("retry_times", 3)
    #     while retry_times:
    #         try:
    #             result = {}
    #             response = await self.make_request().async_download()
    #             result['is_next'] = self.is_next(response)
    #             result['is_ignore'] = self.is_ignore(response)
    #             result['is_retry'] = self.is_retry(response)
    #             result['is_update'] = self.is_update(response)
    #             result['data'] = self.parse(response)     
    #             return result
    #         except Exception as e:
    #             retry_times -= 1

    # 子类重写 解析页面数据
    def parse(self, response: Response) -> dict | str | None:
        return None
