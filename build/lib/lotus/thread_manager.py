import concurrent.futures
from threading import Lock
import copy
from typing import Callable


class ThreadContext:
    def __init__(self, **kwargs) -> None:
        self._context = kwargs
        self._lock = Lock()

    def update(self, **kwargs) -> None:
        with self._lock:
            self._context.update(kwargs)

    def get(self, key) -> None:
        with self._lock:
            return self._context.get(key)
    
    def get_dict(self):
        with self._lock:
            return dict(self._context)


class ThreadManager:
    def __init__(self, max_workers=4):
        # 初始化线程池，默认最大线程数为4
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        # 初始化数据存储列表和锁
        self.data_store = []
        self.lock = Lock()
        self.futures = []

    def add_task(self, func_name: str, spider):
        # 提交任务实例并提交任务
        func = getattr(spider, func_name)
        future = self.executor.submit(self.execute_task, func)
        self.futures.append(future)

    def execute_task(self, func: Callable):
        # 执行任务并存储结果
        result = func()
        self.save_result(result)

    def join(self):
        # 等待所有任务完成
        for future in self.futures:
            future.result()
    
    def join_for_results(self):
        self.join()
        return self.get_results()

    def get_results(self):
        # 获取所有存储的数据并清空数据存储
        with self.lock:
            data_copy = copy.deepcopy(self.data_store)  # 使用深拷贝
            self.data_store.clear()  # 清空数据存储
        return data_copy

    def save_result(self, value):
        # 存储数据，使用锁以确保线程安全
        if value is not None:  # 仅在结果不为 None 时存储
            with self.lock:
                self.data_store.append(value)

    def map(self, func_name: str, spiders):
        # 使用线程池的 map 方法
        return list(self.executor.map(lambda spider: getattr(spider, func_name)(), spiders))

    def __del__(self):
        # 确保在析构函数中关闭线程池
        self.executor.shutdown(wait=True)
