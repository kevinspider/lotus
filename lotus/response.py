from http.cookies import BaseCookie
from curl_cffi.requests.session import Response as ParentResponse
from curl_cffi.requests.cookies import CurlMorsel

class Response(ParentResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 你可以在这里添加自定义的初始化逻辑

    @classmethod
    def from_parent(cls, parent_response):
        # 创建一个新的自定义 Response 实例
        response = cls()
        
        # 将父类 Response 的属性复制到自定义 Response 实例中
        response.__dict__.update(parent_response.__dict__)
        
        return response

    def get_set_cookies(self, *args):
        # curl_cffi 中, response 已经包含了最新 set 的 cookie
        bc = BaseCookie()
        # bc.load(" ".join(self.headers.get_list('Set-Cookie')))
        for each in self.headers.get_list("Set-Cookie"):
            bc.load(each)
        result = {}
        for key in args:
            result[key] = bc.get(key).value
        return result

        