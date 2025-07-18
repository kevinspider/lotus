from curl_cffi.requests import Session, AsyncSession

SESSION_ATTR = ["tread", "curl_options", "debug"]
REQUEST_ATTR = [
    "method",
    "url",
    "params",
    "data",
    "json",
    "headers",
    "cookies",
    "files",
    "auth",
    "timeout",
    "allow_redirects",
    "max_redirects",
    "proxies",
    "proxy",
    "proxy_auth",
    "verify",
    "referer",
    "accept_encoding",
    "content_callback",
    "impersonate",
    "ja3",
    "akamai",
    "extra_fp",
    "default_headers",
    "default_encoding",
    "quote",
    "http_version",
    "interface",
    "cert",
    "stream",
    "max_recv_speed",
    "multipart",
]


class Request:
    def __init__(self, **kwargs) -> None:
        self._session_config = {}
        self._request_config = {}
        # 在这里过滤, 只有 curl_cffi 的合法参数才会传递, spider 的参数并不会传递给 Request
        for key, value in kwargs.items():
            if key in SESSION_ATTR:
                self._session_config[key] = value
            if key in REQUEST_ATTR:
                self._request_config[key] = value

    def download(self):
        try:
            with Session(**self._session_config) as s:
                return s.request(**self._request_config)
        except Exception as e:
            raise e

    async def async_download(self):
        try:
            async with AsyncSession(**self._session_config) as s:
                return await s.request(**self._request_config)
        except Exception as e:
            raise e
        return None
