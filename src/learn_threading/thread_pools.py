"""线程池示例"""

import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple


def thread_pool_demo():
    """线程池示例"""

    def task(n: int) -> Tuple[int, int]:
        """线程池执行的任务"""

        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

        result = fib(n)
        print(f"线程 {threading.current_thread().name} 计算 fib({n}) = {result}")
        return n, result

    print("\n=== 线程池示例 ===")

    # 创建线程池，最大线程数为4
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交任务到线程池
        futures = [executor.submit(task, i) for i in [35, 36, 37, 38, 39, 40]]
        # 获取任务结果
        results = []
        for future in futures:
            n, result = future.result()
            results.append((n, result))

    print(f"线程池执行结果: {results}")


def thread_pool_map_demo():
    """线程池map方法示例"""

    def task(n: int) -> int:
        """线程池执行的任务"""

        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

        result = fib(n)
        print(f"线程 {threading.current_thread().name} 计算 fib({n}) = {result}")
        return result

    print("\n=== 线程池map方法示例 ===")

    # 创建线程池
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 使用map方法执行任务
        inputs = [35, 36, 37, 38]
        results = list(executor.map(task, inputs))

    print(f"输入: {inputs}")
    print(f"输出: {results}")
