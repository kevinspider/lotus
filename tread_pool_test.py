import sys
import time
import hashlib
import jsonpath
import pandas as pd
from lotus.spider import Spider, Config, Response
from lotus.private import ABUYUN_PROXIES
from lotus.thread_manager import ThreadContext, ThreadManager
from lotus.utils import dict_to_json, json_parse, merge_data
from loguru import logger


class Api(Spider):
    # 对于需要相对静态的变量使用类属性
    context: ThreadContext = None
    manager: ThreadManager = None

    def __init__(self, keyword, location, page):
        self.keyword = keyword
        self.location = location
        self.page = page
        config = Config(http_version=1, proxies=ABUYUN_PROXIES, timeout=1, retry_times=10, log_file="lotus.log", log_level="INFO")
        super().__init__(
            "POST",
            "https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.wx.search/1.0/",
            config,
        )
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

    # 初始化请求参数
    def cookies(self):
        return {
            'xlly_s': '1',
            'cookie2': '1b8a76e5a29ce3c048cead605801bc76',
            '_samesite_flag_': 'true',
            't': '1ae519fa26b2d708c132e9fbec16f441',
            '_tb_token_': '737347373e869',
            'isg': 'BH19CeL8xuduXmIL6u155KCfjN93GrFsghnBUD_CoFQDdp2oB2nxPFCtIKowQskk',
            'mtop_partitioned_detect': '1',
            "_m_h5_tk": Api.context.get("_m_h5_tk"),
            "_m_h5_tk_enc": Api.context.get("_m_h5_tk_enc"),
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
            'api': 'mtop.taobao.idlemtopsearch.wx.search',
            'sessionOption': 'AutoLoginOnly',
            'c': f'{self.get_cookies()["_m_h5_tk"]};{self.get_cookies()["_m_h5_tk_enc"]}'
        }

    # 页面解析
    def parse(self, response: Response):
        logger.info(f"Parsing response for {self.keyword}, {self.location}, page {self.page} {response.text}")
        if self.is_ignore(response):
            return None
        if self.page == 1:
            self.add_pages(response)
        result = json_parse(response.json(), ["area", "price", "title", "itemId"], "$.data.resultList")
        return result
    
    # 爬虫子类自实现工具和调度
    def add_pages(self, response: Response):
        sku_nums = jsonpath.jsonpath(response.json(), "$..docNumWhenFirstPage")[0]
        total_page = (sku_nums // 30) + 1
        for page in range(2, total_page + 1):
            # print("增加任务", page)
            Api.manager.add_task("download", Api(self.keyword, self.location, page))

    # 更新 set-cookies
    def is_ignore(self, response: Response):
        if '["FAIL_SYS_TOKEN_EXOIRED::令牌过期"]' in response.text:
            cookies = response.get_set_cookies("_m_h5_tk", "_m_h5_tk_enc")
            Api.context.update(**cookies)
            Api.manager.add_task("download", Api(self.keyword, self.location, self.page))
            logger.info("Token expired, updated cookies and re-added task")
            return True
        return False
    

if __name__ == '__main__':
    # 并发
    manager = ThreadManager(max_workers=4)
    
    # 数据存储
    df = pd.DataFrame()
    
    # 上下文
    context = ThreadContext(
        _m_h5_tk="d903c89c3ad363d9cdf68fc07d4c4565_1733980172025",
        _m_h5_tk_enc="974ad2908d599c5dc1673ef1570a71b5",
    )
    
    Api.context = context
    Api.manager = manager

    cities = ["宁波"]
    keywords = ["口罩"]
    tasks = [Api(keyword=keyword, location=city, page=1) for city in cities for keyword in keywords]
    
    for task in tasks:
        manager.add_task("download", task)

    results = manager.join_for_results()
    for each in results:
        df = merge_data(each, df)
    
    df.to_excel("result.xlsx")
    
