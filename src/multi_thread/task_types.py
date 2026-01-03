"""多线程与不同类型任务结合示例"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor
import random


def multithreaded_io_tasks():
    """多线程处理IO密集型任务示例"""
    
    def io_task(task_id: int):
        """模拟IO密集型任务"""
        print(f"IO任务 {task_id}: 开始执行")
        time.sleep(random.uniform(1.0, 2.0))  # 模拟IO等待
        result = f"IO任务 {task_id} 结果"
        print(f"IO任务 {task_id}: 执行完毕")
        return result
    
    print("\n=== 多线程处理IO密集型任务 ===")
    
    # 使用线程池处理IO任务
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(io_task, i) for i in range(10)]
        results = [future.result() for future in futures]
    
    end_time = time.time()
    
    print(f"\n所有IO任务执行完毕，耗时: {end_time - start_time:.2f}秒")
    print(f"结果: {results}")

def multithreaded_cpu_tasks():
    """多线程处理CPU密集型任务示例"""
    
    def cpu_task(n: int) -> int:
        """模拟CPU密集型任务（计算斐波那契数）"""
        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n+1):
                a, b = b, a + b
            return b
        
        result = fib(n)
        print(f"CPU任务 fib({n}) = {result} 执行完毕")
        return result
    
    print("\n=== 多线程处理CPU密集型任务 ===")
    
    # 使用线程池处理CPU任务
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        inputs = [38, 38, 38, 38]
        results = list(executor.map(cpu_task, inputs))
    
    end_time = time.time()
    
    print(f"\n所有CPU任务执行完毕，耗时: {end_time - start_time:.2f}秒")
    print(f"结果: {results}")
