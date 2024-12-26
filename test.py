from lotus.thread_manager import ThreadManager
from lotus.utils import merge_to_dict
import time
import hashlib
from lotus.spider import Spider


class CustomSpider(Spider):
    def __init__(self):
        super().__init__("get", "http://10.0.0.15:8000/test")
        self.update_config(http_version=1)
        # self.update_config(proxy="http://127.0.0.1:8889")
        # self.update_config(debug=False)
        # self.update_config(timeout=0.01)

    def params(self) -> dict:
        # 返回一个动态生成的字典
        return {"query": "python", "page": 1, "ts": str(int(time.time() * 1000))}

    def data(self) -> dict:
        # 使用 params() 来确保数据同步
        params = self.get_params()
        # return {"search_term": params["query"], "page_number": params["page"]}
        return None

    def headers(self) -> dict:
        return {"User-Agent": "CustomSpider/1.0", "Authorization": "Bearer 1231234124124"}

    def pre_request(self):
        params = self.get_params()
        sign = hashlib.md5(params['ts'].encode("utf-8")).hexdigest()
        self.update_params({"sign": sign})
        # self.update_data({"sign": sign})
        data = self.get_data()
        params = self.get_params()

        print("data", data)
        print("params", params)

    def parse(self, response):
        print(response.request.url)
        print(response.request.headers)

        return response.text


def main():
    # 创建 ThreadManager 实例
    manager = ThreadManager(max_workers=3)

    # 添加多个爬虫实例
    results = manager.map("download", [CustomSpider() for i in range(5)])
    print(results)
    merge_to_dict(results, results)
    print(results)




if __name__ == "__main__":
    main()

    
