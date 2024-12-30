from loguru import logger
from lotus.spider import Spider, Config, Response
from lotus.thread_manager import ThreadContext, ThreadManager
from lotus.utils import dict_to_json

class API(Spider):
    context: ThreadContext = None
    manager: ThreadManager = None

    def __init__(self):
        config = Config()
        super().__init__(url='https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/', method='POST', config=config)

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
            '_m_h5_tk': 'c3c475600cab4ecf678255f32cc957a3_1735538767038',
            '_m_h5_tk_enc': '45f8b87923d42402abac618d09c52565',
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
        return {
            'jsv': '2.7.2',
            'appKey': '34839810',
            't': '1735528705466',
            'sign': '907295ee733fa91a2abaa0fb9f798d8f',
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
        data = dict_to_json({"pageNumber":2,"keyword":"爬虫","fromFilter":False,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":"","searchReqFromPage":"pcSearch","extraFilterValue":"{}","userPositionJson":"{}"})
        return {
            'data': data,
        }

    def parse(self, res: Response):
        logger.info(res.text)
        return None


if __name__ == "__main__":
    api = API()
    api.download()
