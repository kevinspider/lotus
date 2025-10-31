import copy
import concurrent.futures
from threading import Lock
from typing import Callable
from lotus.spider import logger
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
    TextColumn,
)


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
        self.force_stop = False
        self.data_length = 0

        # 进度条
        self.progress = Progress(
            SpinnerColumn(),
            "[bold blue]进度:",
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            MofNCompleteColumn(),
            TextColumn(
                "[bold green] data len: {task.fields[data_length]}", justify="right"
            ),
        )
        self.task_id = self.progress.add_task(
            description="Start Tasks",
            total=0,
            data_length=self.data_length,
        )
        self.progress.start()

    def add_task(self, func_name: str, spider):
        if self.force_stop:
            return
        # 提交任务实例并提交任务
        func = getattr(spider, func_name)
        future = self.executor.submit(self.execute_task, func)
        self.futures.append(future)

        # 更新进度条
        with self.lock:
            total = self.progress.tasks[0].total if self.progress.tasks[0].total else 0
            self.progress.update(self.task_id, total=total + 1)

    def execute_task(self, func: Callable):
        # 执行任务并存储结果
        result = func()
        self.save_result(result)

        # 更新进度条
        with self.lock:
            self.progress.update(self.task_id, advance=1, data_length=self.data_length)

    def cancel_all(self):
        # 捕获ctrl +c 中断
        for f in self.futures:
            cancelled = f.cancel()

    def join(self):
        try:
            # 等待所有任务完成
            for future in self.futures:
                future.result()
            self.progress.stop()
        except KeyboardInterrupt:
            logger.critical("Ctrl + C stop task!!!")
            self.cancel_all()
            self.executor.shutdown(wait=False)
            self.force_stop = True
            self.progress.stop()
            exit(0)
        finally:
            self.executor.shutdown(wait=True)

    def join_for_results(self):
        try:
            self.join()
            return self.get_results()
        except KeyboardInterrupt:
            return []

    def get_results(self):
        # 获取所有存储的数据并清空数据存储
        with self.lock:
            data_copy = copy.deepcopy(self.data_store)  # 使用深拷贝
            self.data_store.clear()  # 清空数据存储
        return data_copy

    def save_result(self, value):
        # 存储数据，使用锁以确保线程安全
        if value is None:
            logger.critical("save_result download result is None, Ignore!!!")
            return None
        elif isinstance(value, (list, dict, str, bytes)):  # 仅在结果不为 None 时存储
            with self.lock:
                self.data_store.append(value)
                if isinstance(value, (str, bytes, dict)):
                    self.data_length += 1
                if isinstance(value, list):
                    self.data_length += len(value)
        else:
            logger.critical(
                "save_result download result is not in (list, dict, str, bytes), Ignore!!!"
            )
            return None

    def map(self, func_name: str, spiders):
        # 使用线程池的 map 方法
        return list(
            self.executor.map(lambda spider: getattr(spider, func_name)(), spiders)
        )

    def __del__(self):
        # 确保在析构函数中关闭线程池
        self.executor.shutdown(wait=True)
