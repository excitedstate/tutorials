"""基础进程操作示例"""

import multiprocessing
import time
from typing import List


def basic_process_demo():
    """基础进程创建和使用示例"""
    
    def worker():
        """进程执行的函数"""
        print(f"进程 {multiprocessing.current_process().name} 开始执行")
        time.sleep(1)
        print(f"进程 {multiprocessing.current_process().name} 执行结束")
    
    print("=== 基础进程示例 ===")
    
    # 创建进程
    p1 = multiprocessing.Process(target=worker, name="Worker-1")
    p2 = multiprocessing.Process(target=worker, name="Worker-2")
    
    # 启动进程
    p1.start()
    p2.start()
    
    # 等待进程结束
    p1.join()
    p2.join()
    
    print("所有进程执行完毕")


def process_with_args():
    """带参数的进程示例"""
    
    def worker_with_args(name: str, delay: float):
        """带参数的进程函数"""
        print(f"进程 {name} 开始执行，延迟 {delay} 秒")
        time.sleep(delay)
        print(f"进程 {name} 执行结束")
    
    print("\n=== 带参数的进程示例 ===")
    
    # 创建带参数的进程
    processes = []
    for i in range(3):
        delay = 0.5  # 使用固定延迟，避免随机数导致的不确定性
        p = multiprocessing.Process(
            target=worker_with_args, 
            name=f"Worker-{i+1}",
            args=(f"Worker-{i+1}", delay)
        )
        processes.append(p)
        p.start()
    
    # 等待所有进程结束
    for p in processes:
        p.join()
    
    print("所有带参数的进程执行完毕")


def process_with_return_value():
    """获取进程返回值的示例"""
    
    def worker_with_result(n: int) -> int:
        """计算斐波那契数的进程函数"""
        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n+1):
                a, b = b, a + b
            return b
        
        result = fib(n)
        print(f"进程 {multiprocessing.current_process().name} 计算 fib({n}) = {result}")
        return result
    
    print("\n=== 获取进程返回值示例 ===")
    
    # 使用multiprocessing.Pool获取返回值
    with multiprocessing.Pool(processes=2) as pool:
        # 提交任务
        future1 = pool.apply_async(worker_with_result, (35,))
        future2 = pool.apply_async(worker_with_result, (36,))
        
        # 获取结果
        result1 = future1.get()
        result2 = future2.get()
        
        print(f"进程返回结果: [{result1}, {result2}]")


def process_daemon_demo():
    """守护进程示例"""
    
    def daemon_worker():
        """守护进程执行的函数"""
        print(f"守护进程 {multiprocessing.current_process().name} 开始执行")
        time.sleep(2)
        print(f"守护进程 {multiprocessing.current_process().name} 执行结束")
    
    print("\n=== 守护进程示例 ===")
    
    # 创建守护进程
    daemon_process = multiprocessing.Process(
        target=daemon_worker, 
        name="Daemon-Worker",
        daemon=True
    )
    
    # 启动守护进程
    daemon_process.start()
    
    # 主进程休眠1秒后结束
    print("主进程休眠1秒后结束")
    time.sleep(1)
    print("主进程结束，守护进程将被终止")
    
    # 注意：这里不调用join()，因为守护进程会随着主进程结束而终止


def process_exit_codes():
    """进程退出码示例"""
    
    def normal_worker():
        """正常结束的进程函数"""
        print("正常进程执行")
        return 0
    
    def error_worker():
        """异常结束的进程函数"""
        print("异常进程执行")
        raise ValueError("进程执行异常")
    
    print("\n=== 进程退出码示例 ===")
    
    # 创建正常进程
    p1 = multiprocessing.Process(target=normal_worker, name="Normal-Process")
    p1.start()
    p1.join()
    print(f"正常进程退出码: {p1.exitcode}")
    
    # 创建异常进程
    p2 = multiprocessing.Process(target=error_worker, name="Error-Process")
    p2.start()
    p2.join()
    print(f"异常进程退出码: {p2.exitcode}")


def process_termination():
    """进程终止示例"""
    
    def long_running_worker():
        """长时间运行的进程函数"""
        print("长时间运行的进程开始执行")
        for i in range(10):
            print(f"进程运行中... {i}")
            time.sleep(1)
        print("长时间运行的进程执行结束")
    
    print("\n=== 进程终止示例 ===")
    
    # 创建并启动长时间运行的进程
    p = multiprocessing.Process(target=long_running_worker, name="Long-Running-Process")
    p.start()
    
    # 主进程休眠3秒后终止子进程
    print("主进程休眠3秒后终止子进程")
    time.sleep(3)
    
    if p.is_alive():
        print(f"终止进程 {p.name}")
        p.terminate()
        p.join()  # 等待进程终止
        print(f"进程 {p.name} 已终止，退出码: {p.exitcode}")
    else:
        print(f"进程 {p.name} 已经结束")
