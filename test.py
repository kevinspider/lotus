import time
import hashlib
from lotus.spider import Spider


class Api(Spider):
    def __init__(self, method: str, url: str) -> None:
        super().__init__(method, url)
        self.ts = int(time.time() * 1000)

    def params(self):
        return {
            "ts": self.ts
        }

    def data(self):
        ts = self.params()['ts']
        print(ts)
        time.sleep(1)
        print(self.params())
    
    def prepare_request(self) -> dict | None:
        print("hello world")
        return None
    

if __name__ == '__main__':
    api = Api("get", "https://www.baidu.com")
    params = api.params()
    data = api.download()
    print(params)
