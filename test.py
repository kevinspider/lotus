import hashlib
import json
import time

from lotus.response import Response
from lotus.spider import Spider, Config
from lotus.private import ABUYUN_PROXIES
from lotus.utils import dict_to_json


class Api(Spider):
    def __init__(self, keyword, location, page, tk, enc):
        self.keyword = keyword
        self.location = location
        self.page = page
        self.tk = tk
        self.enc = enc
        config = Config(http_version=1, proxy="http://127.0.0.1:8889")
        super().__init__(
            "POST",
            "https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/",
            config,
        )

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
            "ALIPAYJSESSIONID": "RZ55zX7ZXtG1DsRTcN5LjwFevAXNci58mobilegwRZ55",
            "_cc_": "WqG3DMC9EA%3D%3D",
            "_l_g_": "Ug%3D%3D",
            "_m_h5_tk": self.tk,
            "_m_h5_tk_enc": self.enc,
            "_nk_": "tb577169955",
            "_tb_token_": "3eee7e0856468",
            "atpsida": "e74266a4dc7a45c814a69a9b_1731652884_2",
            "aui": "2215822705328",
            "cbc": "T2gAbKt8EMyz1l_59qHjbJ-7aeObo_jOZ35fNzhzv84zTU8HcjlD_F6sQixymwXIazM",
            "cna": "Ddu9H62drS8CAZhFz9sxjD8M",
            "cnaui": "2215822705328",
            "cookie1": "BvbZgp%2BNewdZ6MDo11APw6U%2BnijNmkObc%2B704b9EB5o%3D",
            "cookie17": "UUpgQyFZeJDQPtU9Rw%3D%3D",
            "cookie2": "2ef8dc73db1801401a62bba6cbe7027e",
            "csg": "ee10fd01",
            "dnk": "tb577169955",
            "isg": "BHV1KAhzfgKORJq-ikZpp_NXj_iD4igLMprdzfeaMOw7zpTAv0MA1qRPHfTdy0G8",
            "lgc": "tb577169955",
            "munb": "2215822705328",
            "sca": "052d5356",
            "sg": "58a",
            "sgcookie": "W100Nplds3TOZNfoUlGACnMXS2xrm75d7MoHBDso7Yb%2B1daaz5%2BpDTxBy2AzCNfAmecHnj7YIALgQ49D5a%2FkU3mxy3XaxJlWMyX5l%2FH0LN%2Fjry4ql%2F58fWYcMOMypn%2BnDc2q",
            "skt": "fdb0f55249915c59",
            "spanner": "WwIq5djd9O7l86fRh8yX8J8rnNGMzcAi5cCxWi3u7WA",
            "t": "e0b77a1db5749225075a45cc8cdf21b8",
            "tbcp": "f",
            "tbsa": "e76358ce4570da4944a6ccd6_1731652884_1",
            "tfstk": "fnqxDN2guRR6Cq9JyF_oszI--42Orle4USyBjfcD57F8Q5F0oj2XWce_dVg0CfmT65FtiV1qmlF8d7RmGZygwfesaoVGumc6BSc-oK2bj5ETtbKDmVmjVLi4qrxiisoTCWmT66jhx-yqYc1htofyfrmsCGc6CBijsco1t_YkfqSKbW8srnB9PYGrHht_1jsWFbkvhcGj5QTSdbis15tXF3MnQITshh68FbksffOX3ZhO5b-TS5WE4nInhht_2M3x9-TMfhZ-HqnLhbU0ouHxkX0rubHYYJe_m0Up1ieqXbktHoBM8fznBRMKApxLeSN7v2Zlahc14uZ3YbwilYo-tTBJ7FujELg0wKTjOkBKeXXrUF8Zkyk-tTBJ7FujUYhhUM8w7qUF.",
            "tracknick": "tb577169955",
            "uc1": "cookie21",
            "uc3": "id2",
            "uc4": "id4",
            "umdata_": "T2gAIHDEBnAqKEZe8gMl5FqKwZXkBQV8z1RCDepvNerWoqH4uzVmPd2D7xXdYe3_Ugs",
            "unb": "2215822705328",
            "zone": "GZ00F"
        }

    def headers(self):
        return {
            'accept': 'application/json',
            'accept-language': 'zh',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.goofish.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.goofish.com/',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }

    def data(self):
        jsonData = dict_to_json({
            'pageNumber': self.page,
            'keyword': f'{self.location} {self.keyword}',
            'fromFilter': False,
            'rowsPerPage': 30,
            'sortValue': '',
            'sortField': '',
            'customDistance': '',
            'gps': '',
            'propValueStr': {},
            'customGps': '',
        })

        return {
            'data': jsonData,
        }

    def params(self):
        json_data = self.get_data()['data']
        t = str(int(time.time() * 1000))
        sign = self.get_sign(self.get_cookies()['_m_h5_tk'], t, json_data)

        return {
            'jsv': '2.7.2',
            'appKey': '12574478',
            't': t,
            'sign': sign,
            'v': '1.0',
            'type': 'originaljson',
            'accountSite': 'xianyu',
            'dataType': 'json',
            'timeout': '20000',
            'api': 'mtop.taobao.idlemtopsearch.pc.search',
            'sessionOption': 'AutoLoginOnly',
            'spm_cnt': 'a21ybx.search.0.0',
            'spm_pre': 'a21ybx.search.searchInput.0',
        }

    def parse(self, response):
        print(response.text)
        return response.text

    def is_update(self, response: Response) -> dict | str:
        if '["FAIL_SYS_TOKEN_EXOIRED::令牌过期"]' in response.text:
            return response.get_set_cookies("_m_h5_tk", "_m_h5_tk_enc")


class Test(Spider):
    def __init__(self, config=None):
        config = Config(http_version=1, proxy="http://127.0.0.1:8889")
        super().__init__("POST", "http://10.0.0.15:8000/test_json", config)

    def headers(self):
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def json(self):
        return {
            'name': 'string',
        }
        
    def parse(self, response):
        print(response.text)


if __name__ == '__main__':

    result = Test().download()
    print(result)

    # _m_h5_tk = "d903c89c3ad363d9cdf68fc07d4c4565_1733980172025"
    # _m_h5_tk_enc = "974ad2908d599c5dc1673ef1570a71b5"
    # while True:
    #     api = Api(keyword="按需", location="江阴", page=1,
    #               tk=_m_h5_tk, enc=_m_h5_tk_enc)
    #     result = api.download()
    #     if result['is_update'] is not None:
    #         _m_h5_tk = result['is_update']['_m_h5_tk']
    #         _m_h5_tk_enc = result['is_update']['_m_h5_tk_enc']
    #         continue
    #     else:
    #         print(result)
    #         break

