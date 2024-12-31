import hashlib
import time
from loguru import logger
import requests.cookies
from lotus.spider import Spider, Config, Response
from lotus.thread_manager import ThreadContext, ThreadManager
from lotus.utils import dict_to_json


class API(Spider):
    context: ThreadContext = None
    manager: ThreadManager = None

    def __init__(self):
        config = Config()
        super().__init__(url='https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/',
                         method='POST', config=config)

    # 加密逻辑

    def get_sign(self, _m5_h5_tk, ts, data):
        inputStr = (
            _m5_h5_tk.split("_")[0] + "&" + str(ts) +
            "&" + str(12574478) + "&" + data
        )

        m5 = hashlib.md5()
        m5.update(inputStr.encode())
        sign = m5.hexdigest()
        return sign

    def cookies(self):
        return {
            't': 'dfb63bb953f4ccabfbe08139a1009e43',
            'cna': 'DqN6H425YFcCAXr0PdOC8gwl',
            'tracknick': '%E8%8A%B1%E5%BC%80%E5%BC%A5%E6%BC%AB%E6%82%B2%E5%87%89',
            'havana_lgc2_77': 'eyJoaWQiOjc5MTY2MjU5MSwic2ciOiJjYjYzNzc4ZTIzMjdiZDRiNGM2ZGNhMTNjNGUyOGM1MSIsInNpdGUiOjc3LCJ0b2tlbiI6IjFRdmFqSWFQUVRuTDJ6dkhGaEt6WkxBIn0',
            '_hvn_lgc_': '77',
            'havana_lgc_exp': '1736400935091',
            'isg': 'BDEx5q3x8pdsZV-RZ92x0EcnQLvLHqWQ_OQTBhNG6_gXOleMUW_LYe4ZXMZc8j3I',
            'mtop_partitioned_detect': '1',
            '_m_h5_tk': API.context.get("_m_h5_tk"),
            '_m_h5_tk_enc': API.context.get("_m_h5_tk_enc"),
            'cookie2': '119eea12f6b427a57926e5d16b0d93d9',
            'xlly_s': '1',
            '_samesite_flag_': 'true',
            'sgcookie': 'E100h05sUw6pVukb0dcnZGi5Ej4swEf%2BsIGxPKnrBwXgscS2nNi1BsR1zxDKgHXvunqvGPb8P6QV32JyXe4mnweeZme%2FX%2F41071m1z91k%2FvCv00%3D',
            'csg': 'fa40cbaa',
            '_tb_token_': 'fe638763b357e',
            'unb': '791662591',
            'sdkSilent': '1735615088863',
            'tfstk': 'gEuSQK6Wwv3VRdpnmYA4C7ZEi6zIdI8NO6NKsXQP9zURp9hT3YyzzBYQpY2qz8lzyJQILXurL2GhRWhKKQ2eZnloZy4pQdJw7bclNC1ya4N8kZh0NwQp0uBwAz-vQd8wu3CYRL9ZUkr7rIN3H7FLJWdbk5VQJ7eLpIwYO5jdevHKMIN_OwId2yFYHW2YpyUKp-eYnWaLwAWhhW-79bO5fV4fywGjw-_dJ4LuVRi1Yw7Ep72o60wXgIubNuwa0YeXpVGtwVVI-CIQd0i-USDB5KatjxgQXyTCozlsDYZjVp_bmmhiJoiDCGci9fmLc26JaAhKEqau5hISBYGsAzDyTMVjAX3gryt1ZSuSMVqIrL_YFxcxbz09nwMtgfuum291HJmzsrFI-CIQdkIr7Ny6rksCGlbQGRRXGMjHE4MMW6Aic0E8i7LwGI6fxuF0GSAXGMj32SV-dIOfbMf..',
        }

    def headers(self):
        return {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 't=dfb63bb953f4ccabfbe08139a1009e43; cna=DqN6H425YFcCAXr0PdOC8gwl; tracknick=%E8%8A%B1%E5%BC%80%E5%BC%A5%E6%BC%AB%E6%82%B2%E5%87%89; havana_lgc2_77=eyJoaWQiOjc5MTY2MjU5MSwic2ciOiJjYjYzNzc4ZTIzMjdiZDRiNGM2ZGNhMTNjNGUyOGM1MSIsInNpdGUiOjc3LCJ0b2tlbiI6IjFRdmFqSWFQUVRuTDJ6dkhGaEt6WkxBIn0; _hvn_lgc_=77; havana_lgc_exp=1736400935091; isg=BDEx5q3x8pdsZV-RZ92x0EcnQLvLHqWQ_OQTBhNG6_gXOleMUW_LYe4ZXMZc8j3I; mtop_partitioned_detect=1; _m_h5_tk=c3c475600cab4ecf678255f32cc957a3_1735538767038; _m_h5_tk_enc=45f8b87923d42402abac618d09c52565; cookie2=119eea12f6b427a57926e5d16b0d93d9; xlly_s=1; _samesite_flag_=true; sgcookie=E100h05sUw6pVukb0dcnZGi5Ej4swEf%2BsIGxPKnrBwXgscS2nNi1BsR1zxDKgHXvunqvGPb8P6QV32JyXe4mnweeZme%2FX%2F41071m1z91k%2FvCv00%3D; csg=fa40cbaa; _tb_token_=fe638763b357e; unb=791662591; sdkSilent=1735615088863; tfstk=gEuSQK6Wwv3VRdpnmYA4C7ZEi6zIdI8NO6NKsXQP9zURp9hT3YyzzBYQpY2qz8lzyJQILXurL2GhRWhKKQ2eZnloZy4pQdJw7bclNC1ya4N8kZh0NwQp0uBwAz-vQd8wu3CYRL9ZUkr7rIN3H7FLJWdbk5VQJ7eLpIwYO5jdevHKMIN_OwId2yFYHW2YpyUKp-eYnWaLwAWhhW-79bO5fV4fywGjw-_dJ4LuVRi1Yw7Ep72o60wXgIubNuwa0YeXpVGtwVVI-CIQd0i-USDB5KatjxgQXyTCozlsDYZjVp_bmmhiJoiDCGci9fmLc26JaAhKEqau5hISBYGsAzDyTMVjAX3gryt1ZSuSMVqIrL_YFxcxbz09nwMtgfuum291HJmzsrFI-CIQdkIr7Ny6rksCGlbQGRRXGMjHE4MMW6Aic0E8i7LwGI6fxuF0GSAXGMj32SV-dIOfbMf..',
            'origin': 'https://www.goofish.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.goofish.com/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

    def params(self):
        ts = str(int(time.time() * 1000))
        sign = self.get_sign(
            self.get_cookies()['_m_h5_tk'],
            ts,
            self.get_data()['data']
        )
        return {
            'jsv': '2.7.2',
            'appKey': '12574478',
            't': ts,
            'sign': sign,
            'v': '1.0',
            'type': 'originaljson',
            'accountSite': 'xianyu',
            'dataType': 'json',
            'timeout': '20000',
            'api': 'mtop.taobao.idlemtopsearch.pc.search',
            'sessionOption': 'AutoLoginOnly',
            'spm_cnt': 'a21ybx.search.0.0',
            'spm_pre': 'a21ybx.home.searchInput.0',
        }

    def data(self):
        data = dict_to_json({"pageNumber": 2, "keyword": "爬虫", "fromFilter": False, "rowsPerPage": 30, "sortValue": "", "sortField": "", "customDistance": "",
                            "gps": "", "propValueStr": {}, "customGps": "", "searchReqFromPage": "pcSearch", "extraFilterValue": "{}", "userPositionJson": "{}"})
        return {
            'data': data,
        }

    def parse(self, res: Response):
        logger.info(res.json())
        if self.is_update(res):
            return None

        return None

    def is_update(self, res: Response):
        if "令牌过期" in res.text:
            new_cookies = res.get_set_cookies("_m_h5_tk", "_m_h5_tk_enc")
            print(new_cookies)
            API.context['_m_h5_tk'] = new_cookies['_m_h5_tk']
            API.context['_m_h5_tk_enc'] = new_cookies['_m_h5_tk_enc']
            API().download()
            return True
        return False


if __name__ == "__main__":
    context = {
        '_m_h5_tk': 'df91b6a8386e589a81a59b41bc4ce2ce_1735560774914',
        '_m_h5_tk_enc': '92632f39e21ae6b4d73339479028fcf8',
    }
    API.context = context
    api = API()
    api.download()


# ['mtop_partitioned_detect=1;Path=/;Domain=.goofish.com;Max-Age=5400;SameSite=None;Secure;Partitioned', '_m_h5_tk=df91b6a8386e589a81a59b41bc4ce2ce_1735560774914;Path=/;Domain=.goofish.com;Max-Age=5400;SameSite=None;Secure;Partitioned', '_m_h5_tk_enc=92632f39e21ae6b4d73339479028fcf8;Path=/;Domain=.goofish.com;Max-Age=5400;SameSite=None;Secure;Partitioned']
# ['unb=;Path=/;Domain=.goofish.com;Max-Age=0;HttpOnly', '_nk_=;Path=/;Domain=.goofish.com;Max-Age=0', 'cookie1=;Path=/;Domain=.goofish.com;Max-Age=0;HttpOnly', '_l_g_=;Path=/;Domain=.goofish.com;Max-Age=0', 'uss=;Path=/;Domain=.goofish.com;Max-Age=0;HttpOnly', 'sg=;Path=/;Domain=.goofish.com;Max-Age=0', 'cookie17=;Path=/;Domain=.goofish.com;Max-Age=0;HttpOnly', 'mtop_partitioned_detect=1;Path=/;Domain=.goofish.com;Max-Age=5400;SameSite=None;Secure;Partitioned', '_m_h5_tk=dc0ce66bb696ad917273ca62f3df7796_1735562226708;Path=/;Domain=.goofish.com;Max-Age=5400;SameSite=None;Secure', '_m_h5_tk_enc=f98d9caa14401ac368483d16ace18d3b;Path=/;Domain=.goofish.com;Max-Age=5400;SameSite=None;Secure']
    import requests