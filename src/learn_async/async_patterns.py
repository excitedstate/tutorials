"""异步设计模式示例"""

import asyncio
from typing import AsyncGenerator, AsyncIterator


async def async_producer_consumer():
    """异步生产者-消费者模式"""

    # 创建一个异步队列，最大容量为5
    queue = asyncio.Queue(maxsize=5)

    async def producer(name: str, items: int):
        """异步生产者"""
        for i in range(items):
            # 生产一个item
            item = f"{name}-{i}"

            # 异步等待队列有空间
            await queue.put(item)
            print(f"生产者 {name} 生产: {item}，队列大小: {queue.qsize()}")

            # 模拟生产速度
            await asyncio.sleep(0.5)

        # 生产结束信号
        await queue.put(None)
        print(f"生产者 {name} 完成生产")

    async def consumer(name: str):
        """异步消费者"""
        while True:
            # 异步获取队列中的item
            item = await queue.get()

            # 检查结束信号
            if item is None:
                # 放回结束信号，让其他消费者知道
                await queue.put(None)
                print(f"消费者 {name} 收到结束信号")
                break

            print(f"消费者 {name} 消费: {item}，队列大小: {queue.qsize()}")

            # 模拟消费速度
            await asyncio.sleep(1)

            # 标记任务完成
            queue.task_done()

    print("=== 异步生产者-消费者模式 ===")

    # 创建生产者和消费者任务
    producer1 = asyncio.create_task(producer("P1", 5))
    producer2 = asyncio.create_task(producer("P2", 5))
    consumer1 = asyncio.create_task(consumer("C1"))
    consumer2 = asyncio.create_task(consumer("C2"))

    # 等待所有生产者完成
    await asyncio.gather(producer1, producer2)

    # 等待队列中的所有item被消费
    await queue.join()

    # 取消消费者（它们已经收到结束信号并退出）
    consumer1.cancel()
    consumer2.cancel()

    print("生产者-消费者模式演示完成")


async def async_event_loop_demo():
    """异步事件循环演示"""

    async def task1():
        """任务1"""
        print("任务1开始")
        await asyncio.sleep(1)
        print("任务1结束")
        return "任务1结果"

    async def task2():
        """任务2"""
        print("任务2开始")
        await asyncio.sleep(0.5)
        print("任务2结束")
        return "任务2结果"

    print("=== 异步事件循环演示 ===")

    # 获取当前事件循环
    loop = asyncio.get_running_loop()
    print(f"当前事件循环: {loop}")
    print(f"事件循环是否运行: {loop.is_running()}")

    # 创建任务
    print("\n创建任务...")
    task1_obj = loop.create_task(task1())
    task2_obj = loop.create_task(task2())

    print(f"任务1状态: {task1_obj._state}")
    print(f"任务2状态: {task2_obj._state}")

    # 等待任务完成
    print("\n等待任务完成...")
    results = await asyncio.gather(task1_obj, task2_obj)

    print(f"\n任务1状态: {task1_obj._state}")
    print(f"任务2状态: {task2_obj._state}")
    print(f"任务结果: {results}")

    print("\n事件循环演示完成")


async def async_context_manager():
    """异步上下文管理器示例"""

    class AsyncResource:
        """异步资源类，实现异步上下文管理器"""

        def __init__(self, name: str):
            self.name = name

        async def __aenter__(self):
            """异步进入上下文"""
            print(f"获取异步资源: {self.name}")
            await asyncio.sleep(0.5)  # 模拟资源初始化
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            """异步退出上下文"""
            print(f"释放异步资源: {self.name}")
            await asyncio.sleep(0.5)  # 模拟资源清理

        async def do_something(self):
            """使用资源执行操作"""
            print(f"使用异步资源 {self.name} 执行操作")
            await asyncio.sleep(1)

    # 使用异步上下文管理器
    async def use_async_resource():
        """使用异步资源"""
        async with AsyncResource("Resource-1") as resource:
            await resource.do_something()

        # 嵌套使用异步上下文管理器
        async with (
            AsyncResource("Resource-2") as resource2,
            AsyncResource("Resource-3") as resource3,
        ):
            await resource2.do_something()
            await resource3.do_something()

    print("\n=== 异步上下文管理器示例 ===")
    await use_async_resource()

    # 演示使用asynccontextmanager装饰器
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def async_resource_decorator(name: str):
        """使用装饰器实现的异步上下文管理器"""
        print(f"装饰器: 获取资源 {name}")
        await asyncio.sleep(0.5)

        try:
            yield name  # 返回资源给上下文
        finally:
            print(f"装饰器: 释放资源 {name}")
            await asyncio.sleep(0.5)

    # 使用装饰器实现的异步上下文管理器
    async def use_decorator_resource():
        """使用装饰器实现的异步资源"""
        async with async_resource_decorator("Decorator-Resource") as resource:
            print(f"使用装饰器资源: {resource}")
            await asyncio.sleep(1)

    print("\n--- 使用装饰器实现的异步上下文管理器 ---")
    await use_decorator_resource()


async def async_iterators():
    """异步迭代器示例"""

    class AsyncCounter:
        """异步计数器，实现异步迭代器"""

        def __init__(self, start: int, end: int, delay: float = 0.5):
            self.start = start
            self.end = end
            self.delay = delay

        def __aiter__(self) -> AsyncIterator[int]:
            """返回异步迭代器对象"""
            return self

        async def __anext__(self) -> int:
            """异步获取下一个元素"""
            if self.start >= self.end:
                raise StopAsyncIteration

            # 获取当前值
            current = self.start
            self.start += 1

            # 模拟异步操作
            await asyncio.sleep(self.delay)

            return current

    # 使用异步迭代器
    async def use_async_counter():
        """使用异步计数器"""
        print("异步迭代器示例:")

        counter = AsyncCounter(1, 6, delay=0.3)
        async for number in counter:
            print(f"迭代得到: {number}")

    print("\n=== 异步迭代器示例 ===")
    await use_async_counter()

    # 演示异步生成器
    async def async_generator_example() -> AsyncGenerator[int, None]:
        """异步生成器示例"""
        for i in range(1, 6):
            await asyncio.sleep(0.3)
            yield i

    # 使用异步生成器
    async def use_async_generator():
        """使用异步生成器"""
        print("\n异步生成器示例:")

        async for number in async_generator_example():
            print(f"生成器产生: {number}")

    await use_async_generator()

    # 演示异步列表推导式
    async def async_list_comprehension():
        """异步列表推导式示例"""
        print("\n异步列表推导式示例:")

        # 异步生成器
        async def generate_numbers():
            for i in range(1, 6):
                await asyncio.sleep(0.2)
                yield i

        # 异步列表推导式
        numbers = [number async for number in generate_numbers()]
        print(f"异步列表推导结果: {numbers}")

    await async_list_comprehension()


async def async_state_machine():
    """异步状态机示例"""

    class AsyncStateMachine:
        """异步状态机"""

        def __init__(self):
            self.state = "idle"

        async def run(self):
            """运行状态机"""
            while True:
                if self.state == "idle":
                    await self.handle_idle()
                elif self.state == "running":
                    await self.handle_running()
                elif self.state == "paused":
                    await self.handle_paused()
                elif self.state == "stopped":
                    await self.handle_stopped()
                    break
                else:
                    raise ValueError(f"未知状态: {self.state}")

        async def handle_idle(self):
            """处理idle状态"""
            print(f"状态: {self.state} -> 准备运行")
            self.state = "running"
            await asyncio.sleep(0.5)

        async def handle_running(self):
            """处理running状态"""
            print(f"状态: {self.state} -> 正在运行")

            # 模拟工作
            for i in range(3):
                print(f"  工作中... {i+1}/3")
                await asyncio.sleep(0.5)

            # 随机切换到paused或stopped状态
            import random

            if random.random() < 0.5:
                self.state = "paused"
            else:
                self.state = "stopped"

        async def handle_paused(self):
            """处理paused状态"""
            print(f"状态: {self.state} -> 暂停中")
            await asyncio.sleep(1)

            # 从暂停恢复到运行
            self.state = "running"

        async def handle_stopped(self):
            """处理stopped状态"""
            print(f"状态: {self.state} -> 已停止")

    print("\n=== 异步状态机示例 ===")

    # 创建并运行状态机
    state_machine = AsyncStateMachine()
    await state_machine.run()


async def async_future_demo():
    """异步Future示例"""

    async def compute_slow_result():
        """计算慢速结果"""
        print("开始计算慢速结果")
        await asyncio.sleep(2)
        return 42

    print("\n=== 异步Future示例 ===")

    # 获取事件循环
    loop = asyncio.get_running_loop()

    # 创建一个Future对象
    future = loop.create_future()

    # 定义一个完成Future的回调
    async def complete_future():
        """完成Future"""
        result = await compute_slow_result()
        # 设置Future的结果
        future.set_result(result)

    # 启动完成Future的任务
    loop.create_task(complete_future())

    # 等待Future完成
    print("等待Future完成...")
    result = await future
    print(f"Future结果: {result}")

    # 演示使用Future的add_done_callback
    future2 = loop.create_future()

    def done_callback(fut):
        """Future完成回调"""
        print(f"Future完成回调被调用，结果: {fut.result()}")

    # 添加完成回调
    future2.add_done_callback(done_callback)

    # 设置Future结果
    loop.call_later(1, lambda: future2.set_result("Callback result"))

    # 等待Future2完成
    await future2


async def async_cooperative_cancellation():
    """异步协作取消示例"""

    async def cooperative_task():
        """协作式取消的任务"""
        try:
            print("开始协作式任务")

            for i in range(10):
                print(f"执行步骤 {i+1}/10")

                task = asyncio.current_task()

                # 检查是否被取消
                if task and task.cancelled():
                    print("检测到取消请求，清理资源...")
                    await asyncio.sleep(0.5)  # 模拟清理操作
                    raise asyncio.CancelledError("任务被协作式取消")

                await asyncio.sleep(0.5)

            return "任务完成"
        except asyncio.CancelledError as e:
            print(f"捕获到CancelledError: {e}")
            # 可以在这里进行资源清理
            raise  # 重新抛出，让调用者知道任务被取消

    print("\n=== 异步协作取消示例 ===")

    # 创建并启动任务
    task = asyncio.create_task(cooperative_task())

    # 等待2秒后取消任务
    await asyncio.sleep(2)
    print("\n请求取消任务...")
    task.cancel()

    try:
        result = await task
        print(f"任务结果: {result}")
    except asyncio.CancelledError:
        print("任务被取消")


async def async_main_entry():
    """异步主入口示例，演示各种异步设计模式"""

    print("=== 异步设计模式综合演示 ===")

    # 运行各种异步设计模式示例
    await async_producer_consumer()
    await async_event_loop_demo()
    await async_context_manager()
    await async_iterators()
    await async_state_machine()
    await async_future_demo()
    await async_cooperative_cancellation()

    print("\n=== 异步设计模式演示完成 ===")
