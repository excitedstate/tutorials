"""异步并发示例"""

import asyncio
import time
from typing import List, Any


async def async_concurrency_with_gather():
    """使用asyncio.gather()实现并发"""
    
    async def task(name: str, delay: float) -> str:
        """异步任务"""
        print(f"任务 {name} 开始执行，延迟 {delay} 秒")
        await asyncio.sleep(delay)
        result = f"任务 {name} 完成"
        print(result)
        return result
    
    print("=== 使用asyncio.gather()实现并发 ===")
    
    # 记录开始时间
    start_time = time.time()
    
    # 使用asyncio.gather并发执行多个任务
    results = await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3),
        task("D", 1.5)
    )
    
    # 计算总耗时
    total_time = time.time() - start_time
    
    print(f"\n所有任务完成，总耗时: {total_time:.2f}秒")
    print(f"任务结果: {results}")
    print(f"预期最小耗时: 3秒 (由最慢的任务C决定)")


async def async_concurrency_with_wait():
    """使用asyncio.wait()实现并发"""
    
    async def task(name: str, delay: float) -> str:
        """异步任务"""
        print(f"任务 {name} 开始执行，延迟 {delay} 秒")
        await asyncio.sleep(delay)
        result = f"任务 {name} 完成"
        print(result)
        return result
    
    print("\n=== 使用asyncio.wait()实现并发 ===")
    
    # 创建任务列表
    tasks = [
        asyncio.create_task(task("A", 1)),
        asyncio.create_task(task("B", 2)),
        asyncio.create_task(task("C", 0.5))
    ]
    
    # 使用asyncio.wait等待所有任务完成
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    
    print(f"\n已完成任务数: {len(done)}")
    print(f"待完成任务数: {len(pending)}")
    
    # 获取任务结果
    results = [task.result() for task in done]
    print(f"任务结果: {results}")
    
    # 演示FIRST_COMPLETED模式
    print("\n--- 使用FIRST_COMPLETED模式 ---")
    tasks2 = [
        asyncio.create_task(task("X", 2)),
        asyncio.create_task(task("Y", 1)),
        asyncio.create_task(task("Z", 3))
    ]
    
    done2, pending2 = await asyncio.wait(tasks2, return_when=asyncio.FIRST_COMPLETED)
    print(f"第一个完成的任务: {[task.result() for task in done2]}")
    print(f"剩余任务数: {len(pending2)}")
    
    # 取消剩余任务
    for task in pending2:
        task.cancel()


async def async_concurrency_with_as_completed():
    """使用asyncio.as_completed()实现并发"""
    
    async def task(name: str, delay: float) -> str:
        """异步任务"""
        print(f"任务 {name} 开始执行，延迟 {delay} 秒")
        await asyncio.sleep(delay)
        result = f"任务 {name} 完成"
        return result
    
    print("\n=== 使用asyncio.as_completed()实现并发 ===")
    
    # 创建任务列表
    task_coros = [
        task("A", 2),
        task("B", 1),
        task("C", 3),
        task("D", 1.5)
    ]
    
    # 使用asyncio.as_completed迭代完成的任务
    for future in asyncio.as_completed(task_coros):
        result = await future
        print(f"收到任务结果: {result}")
        print(f"可以立即处理这个结果，不需要等待所有任务完成")


async def async_limits_with_semaphore():
    """使用信号量限制并发数量"""
    
    async def limited_task(semaphore: asyncio.Semaphore, name: str, delay: float) -> str:
        """受信号量限制的异步任务"""
        async with semaphore:
            print(f"任务 {name} 获得信号量，开始执行")
            await asyncio.sleep(delay)
            result = f"任务 {name} 完成"
            print(result)
            return result
    
    print("\n=== 使用信号量限制并发数量 ===")
    
    # 创建信号量，限制最大并发数为2
    semaphore = asyncio.Semaphore(2)
    
    # 创建多个任务
    task_coros = [
        limited_task(semaphore, f"Task-{i}", 1) for i in range(5)
    ]
    
    # 并发执行所有任务，但受信号量限制
    results = await asyncio.gather(*task_coros)
    print(f"\n所有任务完成，结果: {results}")


async def async_error_handling():
    """异步任务中的错误处理"""
    
    async def task_with_error(name: str, delay: float, should_error: bool = False):
        """可能抛出错误的异步任务"""
        print(f"任务 {name} 开始执行")
        await asyncio.sleep(delay)
        
        if should_error:
            raise ValueError(f"任务 {name} 故意抛出错误")
        
        return f"任务 {name} 成功完成"
    
    print("\n=== 异步任务中的错误处理 ===")
    
    try:
        # 执行包含错误任务的并发操作
        results = await asyncio.gather(
            task_with_error("A", 0.5),
            task_with_error("B", 1.0, should_error=True),  # 这个任务会出错
            task_with_error("C", 0.7)
        )
        print(f"所有任务成功完成: {results}")
    except ValueError as e:
        print(f"捕获到错误: {e}")
    
    # 演示gather的return_exceptions参数
    print("\n--- 使用return_exceptions参数 ---")
    results_with_exceptions = await asyncio.gather(
        task_with_error("X", 0.5),
        task_with_error("Y", 1.0, should_error=True),  # 这个任务会出错
        task_with_error("Z", 0.7),
        return_exceptions=True  # 错误会被当作结果返回，而不是抛出
    )
    
    print(f"任务结果: {results_with_exceptions}")
    
    # 处理结果中的错误
    for i, result in enumerate(results_with_exceptions):
        if isinstance(result, Exception):
            print(f"任务 {chr(88+i)} 出错: {result}")
        else:
            print(f"任务 {chr(88+i)} 成功: {result}")


async def async_task_group_demo():
    """使用TaskGroup管理异步任务（Python 3.11+）"""
    
    async def task(name: str, delay: float) -> str:
        """异步任务"""
        print(f"任务 {name} 开始执行")
        await asyncio.sleep(delay)
        result = f"任务 {name} 完成"
        print(result)
        return result
    
    print("\n=== 使用TaskGroup管理异步任务 ===")
    
    try:
        # 使用asyncio.TaskGroup（Python 3.11+）
        async with asyncio.TaskGroup() as tg:
            # 创建任务
            task1 = tg.create_task(task("A", 1))
            task2 = tg.create_task(task("B", 2))
            task3 = tg.create_task(task("C", 1.5))
            
            # 可以在TaskGroup内部执行其他操作
            print("在TaskGroup内部执行其他操作")
        
        # TaskGroup完成后获取结果
        results = [task1.result(), task2.result(), task3.result()]
        print(f"\n所有任务完成，结果: {results}")
        
    except AttributeError:
        print("当前Python版本不支持TaskGroup（需要Python 3.11+）")


async def async_timeout_demo():
    """异步任务超时处理"""
    
    async def long_running_task(name: str, delay: float) -> str:
        """长时间运行的异步任务"""
        print(f"长时间任务 {name} 开始执行，预计耗时 {delay} 秒")
        await asyncio.sleep(delay)
        return f"任务 {name} 完成"
    
    print("\n=== 异步任务超时处理 ===")
    
    # 使用asyncio.timeout限制任务执行时间
    try:
        async with asyncio.timeout(2.0):
            result = await long_running_task("A", 3)
            print(f"任务结果: {result}")
    except asyncio.TimeoutError:
        print("任务执行超时！")
    
    # 演示成功的超时情况
    try:
        async with asyncio.timeout(2.0):
            result = await long_running_task("B", 1)
            print(f"任务结果: {result}")
    except asyncio.TimeoutError:
        print("任务执行超时！")
    
    # 演示多个任务的超时处理
    try:
        async with asyncio.timeout(2.5):
            results = await asyncio.gather(
                long_running_task("C", 2),
                long_running_task("D", 1),
                long_running_task("E", 3)  # 这个任务会导致超时
            )
            print(f"所有任务结果: {results}")
    except asyncio.TimeoutError:
        print("多个任务执行超时！")


async def async_cancellation_demo():
    """异步任务取消"""
    
    async def cancellable_task(name: str, delay: float) -> str:
        """可取消的异步任务"""
        try:
            print(f"可取消任务 {name} 开始执行")
            for i in range(delay * 10):
                await asyncio.sleep(0.1)
                print(f"任务 {name} 执行中... {i+1}/{delay*10}")
            return f"任务 {name} 完成"
        except asyncio.CancelledError:
            print(f"任务 {name} 被取消！")
            raise  # 重新抛出取消异常
    
    print("\n=== 异步任务取消 ===")
    
    # 创建任务
    task1 = asyncio.create_task(cancellable_task("A", 3))
    task2 = asyncio.create_task(cancellable_task("B", 2))
    
    # 等待1秒后取消任务
    await asyncio.sleep(1)
    print("\n取消任务A...")
    task1.cancel()
    
    # 等待任务完成
    try:
        await task1
    except asyncio.CancelledError:
        print("确认任务A被取消")
    
    # 等待任务B完成
    result2 = await task2
    print(f"任务B结果: {result2}")


async def async_performance_comparison():
    """异步并发性能比较"""
    
    async def async_task(n: int) -> int:
        """异步任务"""
        await asyncio.sleep(0.01)  # 10ms延迟
        return n * n
    
    def sync_task(n: int) -> int:
        """同步任务"""
        time.sleep(0.01)  # 10ms延迟
        return n * n
    
    print("\n=== 异步并发性能比较 ===")
    
    # 测试参数
    num_tasks = 100
    
    # 异步执行
    start_time = time.time()
    task_coros = [async_task(i) for i in range(num_tasks)]
    async_results = await asyncio.gather(*task_coros)
    async_time = time.time() - start_time
    
    # 同步执行
    start_time = time.time()
    sync_results = [sync_task(i) for i in range(num_tasks)]
    sync_time = time.time() - start_time
    
    # 验证结果一致性
    assert async_results == sync_results
    
    print(f"任务数量: {num_tasks}")
    print(f"异步执行时间: {async_time:.2f}秒")
    print(f"同步执行时间: {sync_time:.2f}秒")
    print(f"异步比同步快: {sync_time / async_time:.2f}倍")
