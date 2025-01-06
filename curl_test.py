import time
import jsonpath
from loguru import logger
import pandas as pd
from lotus.spider import Spider, Config, Response
from lotus.thread_manager import ThreadContext, ThreadManager
from lotus.utils import dict_to_json, json_parse, merge_data
from lotus.private import ABUYUN_PROXIES, get_sign


class API(Spider):
    context = None

    def __init__(self, keyword, location, page):
        config = Config(proxies=ABUYUN_PROXIES, log_level="DEBUG")
        self.keyword = keyword
        self.location = location
        self.page = page
        super().__init__(url='https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.wx.search/1.0/',
                         method='POST', config=config)
        

    def cookies(self):
        return {
            'xlly_s': '1',
            'cookie2': '1b8a76e5a29ce3c048cead605801bc76',
            '_samesite_flag_': 'true',
            't': '1ae519fa26b2d708c132e9fbec16f441',
            '_tb_token_': '737347373e869',
            'isg': 'BH19CeL8xuduXmIL6u155KCfjN93GrFsghnBUD_CoFQDdp2oB2nxPFCtIKowQskk',
            'mtop_partitioned_detect': '1',
            '_m_h5_tk': self.context['_m_h5_tk'],
            '_m_h5_tk_enc': self.context['_m_h5_tk_enc'],
        }

    def headers(self):
        return {
            'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            # 'cookie': 'xlly_s=1; cookie2=1b8a76e5a29ce3c048cead605801bc76; _samesite_flag_=true; t=1ae519fa26b2d708c132e9fbec16f441; _tb_token_=737347373e869; isg=BH19CeL8xuduXmIL6u155KCfjN93GrFsghnBUD_CoFQDdp2oB2nxPFCtIKowQskk; mtop_partitioned_detect=1; _m_h5_tk=3a3ff242ed745b28d684c25691c7f900_1736139638101; _m_h5_tk_enc=678ff668b06f964780b1c3a0ff0f869f',
            'origin': 'https://2.taobao.com',
            'priority': 'u=1, i',
            'referer': 'https://2.taobao.com/',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        }

    def params(self):
        ts = str(int(time.time() * 1000))
        _m_h5_tk = self.get_cookies()['_m_h5_tk']
        _m_h5_tk_enc = self.get_cookies()['_m_h5_tk_enc']
        data = self.get_data()['data']
        sign = get_sign(_m_h5_tk, ts, data)
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
            'api': 'mtop.taobao.idlemtopsearch.wx.search',
            'sessionOption': 'AutoLoginOnly',
            'c': f'{_m_h5_tk};{_m_h5_tk_enc}',
        }

    def data(self):
        data = dict_to_json({"keyword": f"{self.location} {self.keyword}", "pageNumber": self.page, "rowsPerPage": 30, "plateform": "pc", "searchReqFromPage": "xyHome",
                            "bizFrom": "home", "searchTabType": "SEARCH_TAB_MAIN", "sortField": "", "sortValue": "", "propValueStr": ""})
        return {
            'data': data,
        }

    def parse(self, res: Response):
        if self.is_update(res):
            return API(self.keyword, self.location, self.page).download()
        
        for each in res.json()['data']['resultList']:
            result = json_parse(each, ['exContent'])['exContent']
            API.context['df'] = merge_data(result, API.context['df'])
        
        logger.info(f"page is {self.page} items:{len(res.json()['data']['resultList'])} totol:{len(API.context['df'])}")

        if self.has_next(res):
            return API(self.keyword, self.location, self.page + 1).download()
        
        
    
    def is_update(self, res: Response):
        if '["FAIL_SYS_TOKEN_EXOIRED::令牌过期"]' in res.text:
            cookies = res.get_set_cookies("_m_h5_tk", "_m_h5_tk_enc")
            API.context.update(cookies)
            return True
        return False
    
    def has_next(self, res: Response):
        next_page = jsonpath.jsonpath(res.json(), "$..hasNextPage")
        if next_page:
            next_page = next_page[0]
            return next_page
        return False


if __name__ == "__main__":
    context = {
        '_m_h5_tk': 'd903c89c3ad363d9cdf68fc07d4c4565_1733980172025',
        '_m_h5_tk_enc': '974ad2908d599c5dc1673ef1570a71b5',
        'df': pd.DataFrame()
    }

    API.context = context
    
    keyword = "口罩"
    location = "宁波"
    page = 1

    api = API(keyword, location, page)
    api.download()

    API.context['df'].to_excel("result.xlsx")