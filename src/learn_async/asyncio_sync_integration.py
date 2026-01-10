"""asyncio与同步函数集成示例"""

import asyncio
import time
import concurrent.futures


async def run_sync_in_async_context():
    """在异步上下文中运行长耗时的同步函数"""

    print("=== 在异步上下文中运行长耗时的同步函数 ===")

    # 模拟一个长耗时的同步函数
    def long_running_sync_func(duration: float, name: str) -> str:
        """长耗时的同步函数"""
        print(f"同步函数 {name} 开始执行，预计耗时 {duration} 秒")
        time.sleep(duration)  # 模拟CPU密集型或IO密集型操作
        result = f"{name} 完成，耗时 {duration} 秒"
        print(result)
        return result

    # 方法1: 直接在异步函数中调用同步函数（不推荐，会阻塞事件循环）
    print("\n1. 直接调用同步函数（会阻塞事件循环）:")
    start_time = time.time()

    # 直接调用会阻塞整个事件循环
    result1 = long_running_sync_func(1.0, "Sync1")
    result2 = long_running_sync_func(1.0, "Sync2")

    elapsed = time.time() - start_time
    print(f"直接调用总耗时: {elapsed:.2f}秒")
    print(f"结果1: {result1}")
    print(f"结果2: {result2}")

    # 方法2: 使用asyncio.to_thread()在单独线程中运行同步函数（推荐）
    print("\n2. 使用asyncio.to_thread()在单独线程中运行同步函数:")
    start_time = time.time()

    # 使用asyncio.to_thread()并行运行两个同步函数
    task1 = asyncio.to_thread(long_running_sync_func, 1.0, "ToThread1")
    task2 = asyncio.to_thread(long_running_sync_func, 1.0, "ToThread2")

    result3, result4 = await asyncio.gather(task1, task2)

    elapsed = time.time() - start_time
    print(f"to_thread调用总耗时: {elapsed:.2f}秒")
    print(f"结果3: {result3}")
    print(f"结果4: {result4}")

    # 方法3: 使用自定义线程池
    print("\n3. 使用自定义线程池:")
    start_time = time.time()

    # 创建自定义线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # 使用loop.run_in_executor在自定义线程池中运行同步函数
        loop = asyncio.get_running_loop()

        task3 = loop.run_in_executor(executor, long_running_sync_func, 1.0, "Executor1")
        task4 = loop.run_in_executor(executor, long_running_sync_func, 1.0, "Executor2")
        task5 = loop.run_in_executor(executor, long_running_sync_func, 1.0, "Executor3")

        results = await asyncio.gather(task3, task4, task5)

    elapsed = time.time() - start_time
    print(f"自定义线程池总耗时: {elapsed:.2f}秒")
    print(f"结果: {results}")

    # 方法4: 处理同步函数的异常
    print("\n4. 处理同步函数的异常:")

    def sync_func_with_exception():
        """会抛出异常的同步函数"""
        print("同步函数开始执行，即将抛出异常")
        time.sleep(0.5)
        raise ValueError("这是一个测试异常")

    try:
        result = await asyncio.to_thread(sync_func_with_exception)
        print(f"结果: {result}")
    except ValueError as e:
        print(f"捕获到同步函数抛出的异常: {e}")


async def run_async_in_sync_context():
    """在同步上下文中高效执行异步函数"""

    print("\n=== 在同步上下文中高效执行异步函数 ===")

    # 模拟一个异步函数
    async def async_operation(duration: float, name: str) -> str:
        """异步操作"""
        print(f"异步函数 {name} 开始执行，预计耗时 {duration} 秒")
        await asyncio.sleep(duration)
        result = f"{name} 完成，耗时 {duration} 秒"
        print(result)
        return result

    # 定义一个同步函数，在其中执行异步操作
    def sync_function():
        """同步函数，内部执行异步操作"""
        print("\n同步函数开始执行")

        # 方法1: 使用asyncio.run()（最简洁的方式）
        print("\n1. 使用asyncio.run()执行异步函数:")
        start_time = time.time()

        result1 = asyncio.run(async_operation(0.5, "Run1"))

        elapsed = time.time() - start_time
        print(f"asyncio.run总耗时: {elapsed:.2f}秒")
        print(f"结果1: {result1}")

        # 方法2: 使用new_event_loop和run_until_complete
        print("\n2. 使用new_event_loop和run_until_complete:")
        start_time = time.time()

        loop = asyncio.new_event_loop()
        try:
            result2 = loop.run_until_complete(async_operation(0.5, "Loop1"))

            # 并行执行多个异步函数
            tasks = [
                async_operation(0.5, "Loop2"),
                async_operation(0.5, "Loop3"),
                async_operation(0.5, "Loop4"),
            ]
            results = loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()

        elapsed = time.time() - start_time
        print(f"new_event_loop总耗时: {elapsed:.2f}秒")
        print(f"结果2: {result2}")
        print(f"并行结果: {results}")

        # 方法3: 复用事件循环（适用于长时间运行的同步程序）
        print("\n3. 复用事件循环:")
        start_time = time.time()

        # 检查是否已有事件循环
        try:
            loop = asyncio.get_running_loop()
            print("已有事件循环，直接使用")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            print("创建新的事件循环")

        # 使用run_until_complete执行异步操作
        result3 = loop.run_until_complete(async_operation(0.5, "Reuse1"))

        elapsed = time.time() - start_time
        print(f"复用事件循环总耗时: {elapsed:.2f}秒")
        print(f"结果3: {result3}")

        return f"Sync function completed with results: {result1}, {result2}, {result3}"

    # 调用同步函数，它内部会执行异步操作
    sync_result = sync_function()
    print(f"\n同步函数最终结果: {sync_result}")


async def run_async_in_sync_with_executor():
    """在同步上下文中使用执行器执行异步函数"""

    print("\n=== 在同步上下文中使用执行器执行异步函数 ===")

    async def async_task(duration: float, name: str) -> str:
        """异步任务"""
        print(f"异步任务 {name} 开始")
        await asyncio.sleep(duration)
        return f"{name} 结果"

    # 在同步上下文中使用ThreadPoolExecutor执行异步函数
    def sync_with_executor():
        """同步函数，使用执行器执行异步操作"""
        print("\n同步函数开始，使用执行器执行异步操作")

        # 创建线程池执行器
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            # 提交异步函数到执行器
            future = executor.submit(asyncio.run, async_task(1.0, "ExecutorTask"))

            # 获取结果
            result = future.result()
            print(f"执行器返回结果: {result}")

        return result

    # 测试同步函数
    sync_result = await asyncio.to_thread(sync_with_executor)
    print(f"测试结果: {sync_result}")


async def performance_comparison():
    """性能比较示例"""

    print("\n=== 性能比较示例 ===")

    # 定义一个CPU密集型同步函数
    def cpu_bound_sync_func(n: int) -> int:
        """CPU密集型同步函数"""
        result = 0
        for i in range(n):
            result += i * i
        return result

    # 定义一个异步版本的CPU密集型函数
    async def cpu_bound_async_func(n: int) -> int:
        """异步版本的CPU密集型函数"""
        # 注意：纯CPU密集型操作在异步函数中直接执行会阻塞事件循环
        return cpu_bound_sync_func(n)

    # 测试参数
    test_size = 10**7

    # 测试1: 直接在异步上下文中调用CPU密集型同步函数
    print("\n1. 直接在异步上下文中调用CPU密集型同步函数:")
    start_time = time.time()

    # 这会阻塞整个事件循环
    result1 = cpu_bound_sync_func(test_size)

    elapsed1 = time.time() - start_time
    print(f"直接调用耗时: {elapsed1:.2f}秒")
    print(f"结果: {result1}")

    # 测试2: 使用asyncio.to_thread()调用CPU密集型同步函数
    print("\n2. 使用asyncio.to_thread()调用CPU密集型同步函数:")
    start_time = time.time()

    result2 = await asyncio.to_thread(cpu_bound_sync_func, test_size)

    elapsed2 = time.time() - start_time
    print(f"to_thread调用耗时: {elapsed2:.2f}秒")
    print(f"结果: {result2}")

    # 测试3: 使用asyncio.to_thread()并行调用多个CPU密集型同步函数
    print("\n3. 使用asyncio.to_thread()并行调用多个CPU密集型同步函数:")
    start_time = time.time()

    tasks = [
        asyncio.to_thread(cpu_bound_sync_func, test_size // 2),
        asyncio.to_thread(cpu_bound_sync_func, test_size // 2),
        asyncio.to_thread(cpu_bound_sync_func, test_size // 2),
    ]
    results3 = await asyncio.gather(*tasks)

    elapsed3 = time.time() - start_time
    print(f"并行to_thread调用耗时: {elapsed3:.2f}秒")
    print(f"结果: {results3}")

    # 测试4: 直接在异步上下文中调用异步CPU密集型函数
    print("\n4. 直接在异步上下文中调用异步CPU密集型函数:")
    start_time = time.time()

    result4 = await cpu_bound_async_func(test_size)

    elapsed4 = time.time() - start_time
    print(f"异步函数直接调用耗时: {elapsed4:.2f}秒")
    print(f"结果: {result4}")

    # 性能比较总结
    print("\n=== 性能比较总结 ===")
    print(f"直接调用: {elapsed1:.2f}秒")
    print(f"to_thread调用: {elapsed2:.2f}秒")
    print(f"并行to_thread调用: {elapsed3:.2f}秒")
    print(f"异步函数直接调用: {elapsed4:.2f}秒")
    print("\n结论:")
    print("1. 纯CPU密集型操作在异步上下文中直接调用会阻塞事件循环")
    print(
        "2. 使用asyncio.to_thread()可以将同步函数放在单独线程中运行，避免阻塞事件循环"
    )
    print("3. 并行使用to_thread()可以提高多个CPU密集型任务的执行效率")
    print("4. 异步函数中的CPU密集型操作仍然会阻塞事件循环，应该使用to_thread()")


async def advanced_integration_techniques():
    """高级集成技巧"""

    print("\n=== 高级集成技巧 ===")

    # 1. 在异步上下文中使用自定义线程池
    print("\n1. 在异步上下文中使用自定义线程池:")

    def sync_task(name: str, duration: float) -> str:
        """同步任务"""
        print(f"同步任务 {name} 开始，耗时 {duration} 秒")
        time.sleep(duration)
        return f"{name} 完成"

    # 创建自定义线程池
    custom_executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=4, thread_name_prefix="CustomPool"
    )

    try:
        loop = asyncio.get_running_loop()

        # 使用自定义线程池执行多个同步任务
        tasks = [
            loop.run_in_executor(custom_executor, sync_task, f"Task-{i}", 0.5)
            for i in range(6)
        ]

        results = await asyncio.gather(*tasks)
        print(f"自定义线程池结果: {results}")
    finally:
        custom_executor.shutdown()

    # 2. 在长时间运行的同步程序中集成异步代码
    print("\n2. 在长时间运行的同步程序中集成异步代码:")

    async def long_running_async_service():
        """长时间运行的异步服务"""
        print("异步服务启动")

        for i in range(3):
            await asyncio.sleep(1)
            print(f"异步服务执行中... {i+1}/3")

        print("异步服务完成")
        return "Async service completed"

    def long_running_sync_program():
        """长时间运行的同步程序"""
        print("同步程序启动")

        # 运行一段时间
        time.sleep(1)
        print("同步程序执行中...")
        time.sleep(1)

        # 集成异步服务
        print("\n集成异步服务:")
        async_result = asyncio.run(long_running_async_service())

        # 继续运行同步程序
        print(f"\n异步服务返回结果: {async_result}")
        print("同步程序继续执行...")
        time.sleep(1)

        print("同步程序完成")
        return "Sync program completed"

    # 运行长时间运行的同步程序
    sync_result = await asyncio.to_thread(long_running_sync_program)
    print(f"\n长时间运行的同步程序结果: {sync_result}")

    # 3. 处理异步和同步之间的异常
    print("\n3. 处理异步和同步之间的异常:")

    def sync_with_exception():
        """会抛出异常的同步函数"""
        print("同步函数开始，即将抛出异常")
        time.sleep(0.5)
        raise ValueError("同步函数异常")

    async def async_caller():
        """调用同步函数的异步函数"""
        try:
            result = await asyncio.to_thread(sync_with_exception)
            return result
        except ValueError as e:
            print(f"捕获到同步函数异常: {e}")
            # 可以在这里处理异常，或者重新抛出
            raise RuntimeError(f"异步调用失败: {e}") from e

    try:
        await async_caller()
    except RuntimeError as e:
        print(f"最终捕获到的异常: {e}")
        print(f"异常链: {e.__cause__}")


async def main():
    """主函数"""
    print("asyncio与同步函数集成示例")
    print("=" * 60)

    await run_sync_in_async_context()
    await run_async_in_sync_context()
    await run_async_in_sync_with_executor()
    await performance_comparison()
    await advanced_integration_techniques()

    print("\n" + "=" * 60)
    print("示例总结:")
    print("\n在异步上下文中运行长耗时同步函数的最佳实践:")
    print("1. 使用asyncio.to_thread()将同步函数放在单独线程中运行")
    print("2. 对于多个同步任务，使用asyncio.gather()并行执行")
    print("3. 对于大量同步任务，使用自定义ThreadPoolExecutor控制线程数量")
    print("4. 始终处理同步函数可能抛出的异常")
    print("5. 避免在异步函数中直接调用阻塞的同步函数")

    print("\n在同步上下文中执行异步函数的最佳实践:")
    print("1. 使用asyncio.run()（最简洁，适合一次性调用）")
    print("2. 使用new_event_loop()和run_until_complete()（适合需要复用事件循环的场景）")
    print("3. 对于长时间运行的同步程序，考虑使用执行器隔离异步代码")
    print("4. 始终处理异步函数可能抛出的异常")
    print("5. 避免在异步函数中执行CPU密集型操作，应使用to_thread()")

    print("\n高级建议:")
    print("1. 了解你的代码是CPU密集型还是IO密集型，选择合适的执行方式")
    print("2. 使用性能测试比较不同方法的效率")
    print("3. 考虑使用AnyIO库，它提供了更统一的API来处理异步和同步集成")
    print("4. 对于复杂的集成场景，考虑重构代码，尽量减少异步和同步之间的切换")


if __name__ == "__main__":
    asyncio.run(main())
