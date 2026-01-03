"""多进程性能测试"""

import pytest
import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor


def test_multiprocessing_vs_serial_performance():
    """测试多进程与串行执行的性能对比"""
    
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
    
    # 2. 多进程执行
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        process_results = list(executor.map(cpu_bound_task, test_cases))
    process_time = time.time() - start_time
    
    # 验证结果一致性
    assert serial_results == process_results
    
    # 输出性能对比
    print(f"串行执行时间: {serial_time:.2f}秒")
    print(f"多进程执行时间: {process_time:.2f}秒")
    print(f"加速比: {serial_time / process_time:.2f}x")
    
    # 多进程应该比串行快
    assert process_time < serial_time


def test_process_pool_scaling():
    """测试进程池大小对性能的影响"""
    
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
    test_cases = [35, 35, 35, 35, 35, 35, 35, 35]
    
    # 测试不同进程池大小
    for max_workers in [1, 2, 4, 8, 16]:
        start_time = time.time()
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(cpu_bound_task, test_cases))
        elapsed = time.time() - start_time
        
        print(f"进程池大小 {max_workers}: {elapsed:.2f}秒")
    
    # 验证结果
    assert len(results) == len(test_cases)


def test_process_creation_overhead():
    """测试进程创建的开销"""
    
    def simple_task():
        """简单任务"""
        return True
    
    # 测试创建大量进程的开销
    num_processes = 50
    
    start_time = time.time()
    processes = []
    
    for i in range(num_processes):
        p = multiprocessing.Process(target=simple_task)
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"创建和启动 {num_processes} 个进程耗时: {elapsed:.2f}秒")
    print(f"平均每个进程耗时: {elapsed / num_processes * 1000:.2f}毫秒")


def test_shared_memory_performance():
    """测试共享内存的性能"""
    
    # 使用共享内存
    shared_counter = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()
    
    def increment_shared():
        """使用共享内存递增计数器"""
        for _ in range(10000):
            with lock:
                shared_counter.value += 1
    
    # 测试共享内存性能
    start_time = time.time()
    
    processes = [multiprocessing.Process(target=increment_shared) for _ in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    
    shared_time = time.time() - start_time
    
    print(f"共享内存递增40000次耗时: {shared_time:.2f}秒")
    assert shared_counter.value == 40000


def test_process_vs_thread_performance():
    """测试多进程与多线程的性能对比"""
    
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
    test_cases = [36, 36, 36, 36]
    
    # 1. 多线程执行
    from concurrent.futures import ThreadPoolExecutor
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        thread_results = list(executor.map(cpu_bound_task, test_cases))
    thread_time = time.time() - start_time
    
    # 2. 多进程执行
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        process_results = list(executor.map(cpu_bound_task, test_cases))
    process_time = time.time() - start_time
    
    # 验证结果一致性
    assert thread_results == process_results
    
    # 输出性能对比
    print(f"多线程执行时间: {thread_time:.2f}秒")
    print(f"多进程执行时间: {process_time:.2f}秒")
    print(f"多进程比多线程快: {thread_time / process_time:.2f}x")
    
    # 对于CPU密集型任务，多进程应该比多线程快
    assert process_time < thread_time


def test_process_pool_submit_vs_map():
    """测试ProcessPoolExecutor的submit vs map性能"""
    
    def task(n):
        """简单任务"""
        time.sleep(0.1)
        return n * 2
    
    # 测试数据
    data = list(range(20))
    
    # 使用submit
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(task, n) for n in data]
        submit_results = [f.result() for f in futures]
    submit_time = time.time() - start_time
    
    # 使用map
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        map_results = list(executor.map(task, data))
    map_time = time.time() - start_time
    
    # 验证结果一致性
    assert submit_results == map_results
    assert submit_results == [n * 2 for n in data]
    
    print(f"submit方式耗时: {submit_time:.2f}秒")
    print(f"map方式耗时: {map_time:.2f}秒")
    print(f"map比submit快: {submit_time / map_time:.2f}x")
