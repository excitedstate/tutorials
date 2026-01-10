"""进程池示例"""

import multiprocessing
import time
from typing import List, Any


def process_pool_demo():
    """进程池基本使用示例"""

    def worker(n: int) -> int:
        """进程池执行的任务函数"""
        print(f"进程 {multiprocessing.current_process().name} 执行任务: {n}")
        time.sleep(0.5)
        result = n * 2
        print(
            f"进程 {multiprocessing.current_process().name} 完成任务: {n} -> {result}"
        )
        return result

    print("=== 进程池基本使用示例 ===")

    # 创建进程池，使用4个进程
    with multiprocessing.Pool(processes=4) as pool:
        # 提交多个任务
        tasks = [1, 2, 3, 4, 5, 6, 7, 8]

        # 使用apply_async异步执行任务
        print("提交异步任务...")
        results = [pool.apply_async(worker, (task,)) for task in tasks]

        # 获取所有结果
        print("获取任务结果...")
        final_results = [result.get() for result in results]

        print(f"任务结果: {final_results}")
        print(f"预期结果: {[task * 2 for task in tasks]}")


def process_pool_map_demo():
    """进程池map方法示例"""

    def square(n: int) -> int:
        """计算平方的任务函数"""
        print(f"进程 {multiprocessing.current_process().name} 计算 {n} 的平方")
        time.sleep(0.3)
        return n * n

    print("\n=== 进程池map方法示例 ===")

    # 创建进程池
    with multiprocessing.Pool(processes=3) as pool:
        # 使用map方法执行任务
        inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        print(f"输入数据: {inputs}")

        # map方法会阻塞直到所有任务完成
        results = pool.map(square, inputs)

        print(f"map结果: {results}")
        print(f"预期结果: {[n * n for n in inputs]}")


def process_pool_starmap_demo():
    """进程池starmap方法示例"""

    def multiply(a: int, b: int) -> int:
        """计算乘积的任务函数"""
        print(f"进程 {multiprocessing.current_process().name} 计算 {a} * {b}")
        time.sleep(0.4)
        return a * b

    print("\n=== 进程池starmap方法示例 ===")

    # 创建进程池
    with multiprocessing.Pool(processes=3) as pool:
        # 使用starmap方法执行多参数任务
        inputs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
        print(f"输入数据: {inputs}")

        # starmap方法会将元组中的元素作为单独的参数传递给任务函数
        results = pool.starmap(multiply, inputs)

        print(f"starmap结果: {results}")
        print(f"预期结果: {[a * b for a, b in inputs]}")


def process_pool_async_demo():
    """进程池异步任务示例"""

    def long_running_task(n: int) -> int:
        """长时间运行的任务"""
        print(f"进程 {multiprocessing.current_process().name} 开始长时间任务: {n}")
        time.sleep(1)
        result = n * 10
        print(
            f"进程 {multiprocessing.current_process().name} 完成长时间任务: {n} -> {result}"
        )
        return result

    print("\n=== 进程池异步任务示例 ===")

    # 创建进程池
    pool = multiprocessing.Pool(processes=2)

    try:
        # 提交多个异步任务
        tasks = [1, 2, 3, 4]
        futures = [pool.apply_async(long_running_task, (task,)) for task in tasks]

        # 主进程可以继续执行其他工作
        print("主进程继续执行其他工作...")
        time.sleep(0.5)
        print("主进程完成其他工作，等待异步任务结果...")

        # 获取所有结果
        results = [future.get() for future in futures]
        print(f"异步任务结果: {results}")
    finally:
        # 确保进程池被关闭
        pool.close()
        pool.join()


def process_pool_exception_demo():
    """进程池异常处理示例"""

    def task_with_exception(n: int) -> int:
        """可能抛出异常的任务函数"""
        print(f"进程 {multiprocessing.current_process().name} 执行任务: {n}")
        time.sleep(0.3)

        if n == 3:
            raise ValueError(f"任务 {n} 抛出异常")

        return n * 2

    print("\n=== 进程池异常处理示例 ===")

    # 创建进程池
    with multiprocessing.Pool(processes=2) as pool:
        tasks = [1, 2, 3, 4, 5]
        futures = [pool.apply_async(task_with_exception, (task,)) for task in tasks]

        results = []
        for i, future in enumerate(futures):
            try:
                result = future.get()
                results.append(result)
                print(f"任务 {tasks[i]} 成功: {result}")
            except ValueError as e:
                results.append(None)
                print(f"任务 {tasks[i]} 失败: {e}")

        print(f"最终结果列表: {results}")


def process_pool_performance_demo():
    """进程池性能测试示例"""

    def cpu_bound_task(n: int) -> int:
        """CPU密集型任务"""

        def fib(x: int) -> int:
            if x <= 1:
                return x
            a, b = 0, 1
            for _ in range(2, x + 1):
                a, b = b, a + b
            return b

        return fib(n)

    print("\n=== 进程池性能测试示例 ===")

    # 测试参数
    test_cases = [35, 36, 37, 38, 39, 40]

    # 串行执行
    print("串行执行开始...")
    start_time = time.time()
    serial_results = [cpu_bound_task(n) for n in test_cases]
    serial_time = time.time() - start_time
    print(f"串行执行时间: {serial_time:.2f}秒")

    # 并行执行
    print("并行执行开始...")
    start_time = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        parallel_results = pool.map(cpu_bound_task, test_cases)
    parallel_time = time.time() - start_time
    print(f"并行执行时间: {parallel_time:.2f}秒")

    # 验证结果一致性
    print(f"结果一致: {serial_results == parallel_results}")
    print(f"加速比: {serial_time / parallel_time:.2f}x")
    print(f"并行效率: {serial_time / (parallel_time * 4) * 100:.1f}%")
