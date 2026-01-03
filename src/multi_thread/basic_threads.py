"""基础线程操作示例"""

import threading
import time
from typing import List


def basic_thread_demo():
    """基础线程创建和使用示例"""
    
    def worker():
        """线程执行的函数"""
        print(f"线程 {threading.current_thread().name} 开始执行")
        time.sleep(1)
        print(f"线程 {threading.current_thread().name} 执行结束")
    
    print("=== 基础线程示例 ===")
    
    # 创建线程
    t1 = threading.Thread(target=worker, name="Worker-1")
    t2 = threading.Thread(target=worker, name="Worker-2")
    
    # 启动线程
    t1.start()
    t2.start()
    
    # 等待线程结束
    t1.join()
    t2.join()
    
    print("所有线程执行完毕")

def thread_with_args():
    """带参数的线程示例"""
    
    def worker_with_args(name: str, delay: float):
        """带参数的线程函数"""
        print(f"线程 {name} 开始执行，延迟 {delay} 秒")
        time.sleep(delay)
        print(f"线程 {name} 执行结束")
    
    print("\n=== 带参数的线程示例 ===")
    
    # 创建带参数的线程
    threads = []
    for i in range(3):
        delay = 0.5  # 使用固定延迟，避免随机数导致的不确定性
        t = threading.Thread(
            target=worker_with_args, 
            name=f"Worker-{i+1}",
            args=(f"Worker-{i+1}", delay)
        )
        threads.append(t)
        t.start()
    
    # 等待所有线程结束
    for t in threads:
        t.join()
    
    print("所有带参数的线程执行完毕")

def thread_with_return_value():
    """获取线程返回值的示例"""
    
    def worker_with_result(n: int) -> int:
        """计算斐波那契数的线程函数"""
        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n+1):
                a, b = b, a + b
            return b
        
        result = fib(n)
        print(f"线程 {threading.current_thread().name} 计算 fib({n}) = {result}")
        return result
    
    print("\n=== 获取线程返回值示例 ===")
    
    # 使用列表存储结果
    results = []
    
    def worker_wrapper(n: int):
        """线程包装函数，用于存储返回值"""
        result = worker_with_result(n)
        results.append(result)
    
    # 创建并启动线程
    t1 = threading.Thread(target=worker_wrapper, args=(35,), name="Fib-1")
    t2 = threading.Thread(target=worker_wrapper, args=(36,), name="Fib-2")
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"线程返回结果: {results}")
