"""异步编程性能测试"""

import pytest
import asyncio
import time
import threading
from concurrent.futures import ThreadPoolExecutor


async def test_async_vs_sync_performance():
    """测试异步与同步执行的性能对比"""
    
    # IO密集型任务
    async def async_io_task(delay):
        """异步IO任务"""
        await asyncio.sleep(delay)
        return delay
    
    def sync_io_task(delay):
        """同步IO任务"""
        time.sleep(delay)
        return delay
    
    # 测试参数
    delays = [0.1] * 20  # 20个IO密集型任务
    
    # 1. 同步执行
    start_time = time.time()
    sync_results = [sync_io_task(delay) for delay in delays]
    sync_time = time.time() - start_time
    
    # 2. 异步执行
    start_time = time.time()
    async_results = await asyncio.gather(*[async_io_task(delay) for delay in delays])
    async_time = time.time() - start_time
    
    # 3. 多线程执行
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        thread_results = list(executor.map(sync_io_task, delays))
    thread_time = time.time() - start_time
    
    # 验证结果一致性
    assert sync_results == async_results == thread_results
    
    # 输出性能对比
    print(f"同步执行时间: {sync_time:.2f}秒")
    print(f"异步执行时间: {async_time:.2f}秒")
    print(f"多线程执行时间: {thread_time:.2f}秒")
    print(f"异步比同步快: {sync_time / async_time:.2f}x")
    print(f"异步比多线程快: {thread_time / async_time:.2f}x")
    
    # 异步应该比同步快很多，比多线程也快
    assert async_time < sync_time
    assert async_time < thread_time


async def test_async_concurrency_scaling():
    """测试异步并发规模对性能的影响"""
    
    async def async_task(delay):
        """异步任务"""
        await asyncio.sleep(delay)
        return delay
    
    # 测试不同规模的并发任务
    for num_tasks in [10, 50, 100, 500, 1000]:
        delays = [0.01] * num_tasks  # 每个任务延迟10ms
        
        start_time = time.time()
        await asyncio.gather(*[async_task(delay) for delay in delays])
        elapsed = time.time() - start_time
        
        print(f"异步执行 {num_tasks} 个任务耗时: {elapsed:.2f}秒")
        print(f"平均每个任务耗时: {elapsed / num_tasks * 1000:.2f}毫秒")


async def test_async_gather_vs_wait_performance():
    """测试asyncio.gather()与asyncio.wait()的性能对比"""
    
    async def async_task(delay, i):
        """异步任务"""
        await asyncio.sleep(delay)
        return i
    
    # 测试参数
    num_tasks = 100
    delays = [0.01] * num_tasks
    
    # 1. 使用asyncio.gather
    start_time = time.time()
    gather_results = await asyncio.gather(*[async_task(delays[i], i) for i in range(num_tasks)])
    gather_time = time.time() - start_time
    
    # 2. 使用asyncio.wait
    start_time = time.time()
    tasks = [asyncio.create_task(async_task(delays[i], i)) for i in range(num_tasks)]
    done, pending = await asyncio.wait(tasks)
    wait_results = [task.result() for task in done]
    wait_time = time.time() - start_time
    
    # 验证结果一致性
    assert sorted(gather_results) == sorted(wait_results)
    assert len(gather_results) == num_tasks
    assert len(wait_results) == num_tasks
    
    # 输出性能对比
    print(f"asyncio.gather 耗时: {gather_time:.2f}秒")
    print(f"asyncio.wait 耗时: {wait_time:.2f}秒")
    print(f"gather比wait快: {wait_time / gather_time:.2f}x")


async def test_async_with_asyncio_to_thread():
    """测试asyncio.to_thread()的性能"""
    
    def sync_task(delay):
        """同步任务"""
        time.sleep(delay)
        return delay
    
    async def async_task(delay):
        """异步任务"""
        await asyncio.sleep(delay)
        return delay
    
    # 测试参数
    num_tasks = 20
    delay = 0.1
    
    # 1. 直接异步任务
    start_time = time.time()
    async_results = await asyncio.gather(*[async_task(delay) for _ in range(num_tasks)])
    async_time = time.time() - start_time
    
    # 2. 使用asyncio.to_thread
    start_time = time.time()
    to_thread_results = await asyncio.gather(*[asyncio.to_thread(sync_task, delay) for _ in range(num_tasks)])
    to_thread_time = time.time() - start_time
    
    # 验证结果一致性
    assert async_results == to_thread_results
    
    # 输出性能对比
    print(f"直接异步任务耗时: {async_time:.2f}秒")
    print(f"asyncio.to_thread耗时: {to_thread_time:.2f}秒")
    print(f"直接异步比to_thread快: {to_thread_time / async_time:.2f}x")


async def test_async_http_performance():
    """测试异步HTTP请求性能"""
    
    # 注意：这个测试需要网络连接，可能会因网络环境不同而结果不同
    import aiohttp
    
    async def fetch_url(session, url):
        """异步获取URL"""
        async with session.get(url) as response:
            await response.text()
            return response.status
    
    urls = ["https://httpbin.org/get"] * 20
    
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        results = await asyncio.gather(*[fetch_url(session, url) for url in urls])
        elapsed = time.time() - start_time
        
        print(f"异步执行20个HTTP请求耗时: {elapsed:.2f}秒")
        print(f"平均每个请求耗时: {elapsed / len(urls) * 1000:.2f}毫秒")
        
        # 验证所有请求都成功
        assert all(status == 200 for status in results)


async def test_async_vs_multiprocessing_cpu_bound():
    """测试异步与多进程在CPU密集型任务上的性能对比"""
    
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
    
    # 1. 异步执行（CPU密集型任务，异步没有优势）
    async def async_cpu_task(n):
        """异步CPU任务"""
        return cpu_bound_task(n)
    
    start_time = time.time()
    async_results = await asyncio.gather(*[async_cpu_task(n) for n in test_cases])
    async_time = time.time() - start_time
    
    # 2. 多进程执行
    from concurrent.futures import ProcessPoolExecutor
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        process_results = list(executor.map(cpu_bound_task, test_cases))
    process_time = time.time() - start_time
    
    # 验证结果一致性
    assert async_results == process_results
    
    # 输出性能对比
    print(f"异步执行CPU密集型任务时间: {async_time:.2f}秒")
    print(f"多进程执行CPU密集型任务时间: {process_time:.2f}秒")
    print(f"多进程比异步快: {async_time / process_time:.2f}x")
    
    # 对于CPU密集型任务，多进程应该比异步快很多
    assert process_time < async_time
