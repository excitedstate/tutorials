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
    
    # 测试参数 - 减少任务数量和延迟时间
    delays = [0.05] * 10  # 10个IO密集型任务，每个延迟0.05秒
    
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
    
    # 测试不同规模的并发任务 - 减少任务数量
    for num_tasks in [10, 50, 100]:  # 只测试到100个任务
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
    
    # 测试参数 - 减少任务数量
    num_tasks = 50
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
    
    # 测试参数 - 减少任务数量和延迟时间
    num_tasks = 10
    delay = 0.05
    
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


@pytest.mark.skip(reason="跳过网络相关测试，避免依赖外部环境")
async def test_async_http_performance():
    """测试异步HTTP请求性能"""
    pass


@pytest.mark.skip(reason="跳过CPU密集型测试，避免长时间运行")
async def test_async_vs_multiprocessing_cpu_bound():
    """测试异步与多进程在CPU密集型任务上的性能对比"""
    pass
