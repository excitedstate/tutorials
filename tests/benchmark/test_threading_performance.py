"""多线程性能测试"""

import pytest
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def test_threading_vs_serial_performance():
    """测试多线程与串行执行的性能对比"""
    
    def cpu_bound_task(n):
        """CPU密集型任务"""
        def fib(x):
            if x <= 1:
                return x
            a, b = 0, 1
            for _ in range(2, x+1):
                a, b = b, a + b
            return b
        return fib(n)
    
    # 测试参数
    test_cases = [35, 36, 37, 38]
    
    # 1. 串行执行
    start_time = time.time()
    serial_results = [cpu_bound_task(n) for n in test_cases]
    serial_time = time.time() - start_time
    
    # 2. 多线程执行
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        thread_results = list(executor.map(cpu_bound_task, test_cases))
    thread_time = time.time() - start_time
    
    # 验证结果一致性
    assert serial_results == thread_results
    
    # 输出性能对比
    print(f"串行执行时间: {serial_time:.2f}秒")
    print(f"多线程执行时间: {thread_time:.2f}秒")
    print(f"加速比: {serial_time / thread_time:.2f}x")
    
    # 多线程应该比串行快（在CPU密集型任务中，加速比可能小于CPU核心数）
    assert thread_time < serial_time


def test_thread_pool_scaling():
    """测试线程池大小对性能的影响"""
    
    def io_bound_task(delay):
        """IO密集型任务"""
        time.sleep(delay)
        return delay
    
    # 测试参数
    delays = [0.1] * 20  # 20个IO密集型任务
    
    # 测试不同线程池大小
    for max_workers in [1, 2, 4, 8, 16]:
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(io_bound_task, delays))
        elapsed = time.time() - start_time
        
        print(f"线程池大小 {max_workers}: {elapsed:.2f}秒")
    
    # 验证结果
    assert sum(results) == sum(delays)


def test_thread_creation_overhead():
    """测试线程创建的开销"""
    
    def simple_task():
        """简单任务"""
        pass
    
    # 测试创建大量线程的开销
    num_threads = 1000
    
    start_time = time.time()
    threads = []
    
    for i in range(num_threads):
        t = threading.Thread(target=simple_task)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"创建和启动 {num_threads} 个线程耗时: {elapsed:.2f}秒")
    print(f"平均每个线程耗时: {elapsed / num_threads * 1000:.2f}毫秒")


def test_lock_contention_performance():
    """测试锁竞争对性能的影响"""
    
    # 共享计数器
    counter = 0
    lock = threading.Lock()
    
    def increment_with_lock():
        """使用锁递增计数器"""
        nonlocal counter
        for _ in range(10000):
            with lock:
                counter += 1
    
    def increment_without_lock():
        """不使用锁递增计数器"""
        nonlocal counter
        for _ in range(10000):
            # 存在竞态条件
            counter += 1
    
    # 测试使用锁的情况
    counter = 0
    start_time = time.time()
    
    threads = [threading.Thread(target=increment_with_lock) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    lock_time = time.time() - start_time
    lock_result = counter
    
    # 测试不使用锁的情况
    counter = 0
    start_time = time.time()
    
    threads = [threading.Thread(target=increment_without_lock) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    no_lock_time = time.time() - start_time
    no_lock_result = counter
    
    print(f"使用锁耗时: {lock_time:.2f}秒，结果: {lock_result}")
    print(f"不使用锁耗时: {no_lock_time:.2f}秒，结果: {no_lock_result}")
    print(f"锁开销: {(lock_time - no_lock_time) * 1000:.2f}毫秒")
    
    # 验证使用锁的结果正确
    assert lock_result == 40000
    # 不使用锁的结果可能不正确
    assert no_lock_result <= 40000


def test_thread_pool_submit_vs_map():
    """测试ThreadPoolExecutor的submit vs map性能"""
    
    def task(n):
        """简单任务"""
        time.sleep(0.01)
        return n * 2
    
    # 测试数据
    data = list(range(100))
    
    # 使用submit
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(task, n) for n in data]
        submit_results = [f.result() for f in futures]
    submit_time = time.time() - start_time
    
    # 使用map
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        map_results = list(executor.map(task, data))
    map_time = time.time() - start_time
    
    # 验证结果一致性
    assert submit_results == map_results
    assert submit_results == [n * 2 for n in data]
    
    print(f"submit方式耗时: {submit_time:.2f}秒")
    print(f"map方式耗时: {map_time:.2f}秒")
    print(f"map比submit快: {submit_time / map_time:.2f}x")
