"""AnyIO库介绍和示例"""

import anyio
import asyncio
import time

import anyio.to_thread


async def anyio_basic_demo():
    """AnyIO基础示例"""

    print("=== AnyIO基础示例 ===")
    print("AnyIO是一个异步编程库，提供了统一的API来处理不同的异步后端（asyncio和trio）")

    async def anyio_task(name: str, delay: float) -> str:
        """AnyIO任务"""
        print(f"任务 {name} 开始执行")
        await anyio.sleep(delay)
        result = f"任务 {name} 完成"
        print(result)
        return result

    # 使用anyio.run()运行异步代码
    print("\n1. 使用anyio.run()运行异步代码:")
    result = await anyio_task("Basic", 1)
    print(f"任务结果: {result}")


async def anyio_concurrency_demo():
    """AnyIO并发执行示例"""

    print("\n=== AnyIO并发执行示例 ===")

    async def task(name: str, delay: float) -> str:
        """简单的AnyIO任务"""
        print(f"任务 {name} 开始，延迟 {delay} 秒")
        await anyio.sleep(delay)
        return f"{name} 结果"

    # 使用anyio.gather并发执行多个任务
    print("\n1. 使用anyio.gather并发执行多个任务:")
    results = anyio.gather((task("A", 1.5), task("B", 1.0), task("C", 0.5)))
    print(f"并发任务结果: {results}")

    # 使用anyio.move_on_after设置超时
    print("\n2. 使用anyio.move_on_after设置超时:")
    try:
        with anyio.move_on_after(1.0):
            result = await task("Long", 2.0)
            print(f"任务完成: {result}")
    except TimeoutError:
        print("任务超时")


async def anyio_file_operations():
    """AnyIO文件操作示例"""

    print("\n=== AnyIO文件操作示例 ===")

    # 异步写入文件
    print("\n1. 异步写入文件:")
    async with await anyio.open_file("anyio_test.txt", "w") as f:
        await f.write("Hello, AnyIO!\n")
        await f.write("This is a test file.\n")
        await f.write("AnyIO provides async file operations.\n")
    print("文件写入完成")

    # 异步读取文件
    print("\n2. 异步读取文件:")
    async with await anyio.open_file("anyio_test.txt", "r") as f:
        content = await f.read()
        print("文件内容:")
        print(content)

    # 异步追加文件
    print("\n3. 异步追加文件:")
    async with await anyio.open_file("anyio_test.txt", "a") as f:
        await f.write("This is appended content.\n")
    print("文件追加完成")

    # 再次读取文件验证
    async with await anyio.open_file("anyio_test.txt", "r") as f:
        content = await f.read()
        print("\n追加后的文件内容:")
        print(content)


async def anyio_sync_primitives():
    """AnyIO同步原语示例"""

    print("\n=== AnyIO同步原语示例 ===")

    # 使用AnyIO锁
    print("\n1. 使用AnyIO锁:")
    lock = anyio.Lock()
    shared_counter = 0

    async def increment_with_lock():
        """使用锁递增计数器"""
        nonlocal shared_counter
        async with lock:
            current = shared_counter
            await anyio.sleep(0.1)  # 模拟复杂操作
            shared_counter = current + 1

    # 并发执行多个递增操作
    anyio.gather(*[increment_with_lock() for _ in range(10)])
    print(f"使用锁后的计数器值: {shared_counter}")

    # 使用AnyIO信号量
    print("\n2. 使用AnyIO信号量:")
    semaphore = anyio.Semaphore(2)  # 限制最大并发数为2

    async def task_with_semaphore(name: str):
        """受信号量限制的任务"""
        async with semaphore:
            print(f"任务 {name} 获得信号量，开始执行")
            await anyio.sleep(0.5)
            print(f"任务 {name} 释放信号量")

    # 并发执行5个任务，但受信号量限制
    anyio.gather(*[task_with_semaphore(f"Task-{i}") for i in range(5)])

    # 使用AnyIO事件
    print("\n3. 使用AnyIO事件:")
    event = anyio.Event()

    async def wait_for_event():
        """等待事件的任务"""
        print("等待事件触发...")
        await event.wait()
        print("事件已触发!")

    async def trigger_event():
        """触发事件的任务"""
        await anyio.sleep(1)
        print("触发事件")
        event.set()

    # 同时运行两个任务
    anyio.gather((wait_for_event(), trigger_event()))


async def anyio_task_groups():
    """AnyIO任务组示例"""

    print("\n=== AnyIO任务组示例 ===")
    print("AnyIO任务组提供了一种安全的方式来管理并发任务")

    async def failing_task():
        """会失败的任务"""
        await anyio.sleep(0.5)
        print("任务即将失败")
        raise ValueError("任务故意失败")

    async def successful_task():
        """成功的任务"""
        await anyio.sleep(0.3)
        print("成功任务完成")
        return "success"

    # 使用任务组
    print("\n1. 使用任务组运行多个任务:")
    try:
        async with anyio.create_task_group() as tg:
            tg.start_soon(failing_task)
            tg.start_soon(successful_task)
        print("所有任务完成")
    except ValueError as e:
        print(f"捕获到任务组中的异常: {e}")

    # 演示任务组的取消行为
    print("\n2. 任务组的取消行为:")

    async def cancellable_task(name: str, delay: float):
        """可取消的任务"""
        try:
            print(f"可取消任务 {name} 开始")
            await anyio.sleep(delay)
            print(f"可取消任务 {name} 完成")
            return name
        except anyio.get_cancelled_exc_class():
            print(f"可取消任务 {name} 被取消")
            raise

    try:
        with anyio.move_on_after(1.0):
            async with anyio.create_task_group() as tg:
                tg.start_soon(cancellable_task, "Task-1", 0.5)
                tg.start_soon(cancellable_task, "Task-2", 1.5)
                tg.start_soon(cancellable_task, "Task-3", 2.0)
    except anyio.get_cancelled_exc_class():
        print("任务组被整体取消")


async def anyio_asyncio_compatibility():
    """AnyIO与asyncio兼容性示例"""

    print("\n=== AnyIO与asyncio兼容性示例 ===")
    print("AnyIO可以与asyncio代码无缝协作")

    # 从AnyIO调用asyncio代码
    print("\n1. 从AnyIO调用asyncio代码:")

    async def asyncio_task():
        """asyncio任务"""
        print("这是一个asyncio任务")
        await asyncio.sleep(0.5)
        return "asyncio任务结果"

    # 使用anyio.to_thread.run_sync在单独的线程中运行同步代码
    print("\n2. 使用anyio.to_thread.run_sync运行同步代码:")

    def sync_function(x: int, y: int) -> int:
        """同步函数"""
        print(f"这是一个同步函数，计算 {x} + {y}")
        time.sleep(1)  # 同步睡眠
        return x + y

    # 在AnyIO中运行同步函数
    result = await anyio.to_thread.run_sync(sync_function, 10, 20)
    print(f"同步函数结果: {result}")

    # 使用anyio.from_thread.run在主线程中运行异步代码
    print("\n3. 使用anyio.from_thread.run在主线程中运行异步代码:")

    async def async_function_to_run():
        """要在主线程中运行的异步函数"""
        print("在主线程中运行异步函数")
        await anyio.sleep(0.5)
        return "主线程异步函数结果"

    # 这个功能通常在同步代码中调用异步函数时使用
    print("注意: from_thread.run通常在同步代码中调用异步函数时使用")


async def anyio_stream_demo():
    """AnyIO流示例"""

    print("\n=== AnyIO流示例 ===")
    print("AnyIO提供了高级的流API，支持TCP、UDP等")

    # 简单的TCP回显客户端和服务器示例
    print("\n1. TCP回显客户端和服务器示例:")

    async def echo_server(server_sock):
        """简单的回显服务器"""
        async with await server_sock.accept() as (client_sock, addr):
            print(f"客户端 {addr} 连接")
            async with client_sock:
                async for data in client_sock:
                    print(f"收到数据: {data.decode()}")
                    await client_sock.sendall(data)

    async def echo_client():
        """简单的回显客户端"""
        try:
            # 等待服务器启动
            await anyio.sleep(0.5)

            # 连接到服务器
            async with await anyio.connect_tcp("127.0.0.1", 12345) as client_sock:
                # 发送数据
                message = "Hello, AnyIO TCP!"
                print(f"发送数据: {message}")
                await client_sock.send(message.encode())

                # 接收响应
                response = await client_sock.receive(1024)
                print(f"收到响应: {response.decode()}")

                return response.decode() == message
        except Exception as e:
            print(f"客户端连接失败: {e}")
            return False

    # 启动服务器和客户端
    try:
        async with await anyio.create_tcp_listener(
            local_host="127.0.0.1", local_port=12345
        ) as server_sock:
            # 同时运行服务器和客户端
            async with anyio.create_task_group() as tg:
                tg.start_soon(echo_server, server_sock)
                tg.start_soon(echo_client)
            print(f"TCP示例完成")
    except Exception as e:
        print(f"TCP示例失败: {e}")


async def anyio_main_demo():
    """AnyIO综合演示"""

    print("=== AnyIO综合演示 ===")
    print("AnyIO是一个功能强大的异步编程库，提供了统一的API来处理不同的异步后端")
    print("它的主要特点包括:")
    print("1. 统一的API，支持asyncio和trio后端")
    print("2. 高级的并发原语")
    print("3. 异步文件I/O")
    print("4. 网络编程支持")
    print("5. 与asyncio代码的兼容性")
    print("6. 强大的任务组")
    print("7. 优雅的取消机制")

    # 运行各个示例
    await anyio_basic_demo()
    await anyio_concurrency_demo()
    await anyio_file_operations()
    await anyio_sync_primitives()
    await anyio_task_groups()
    await anyio_asyncio_compatibility()
    await anyio_stream_demo()

    print("\n=== AnyIO综合演示完成 ===")
    print("AnyIO提供了一种现代、安全、高效的异步编程方式")
    print("它结合了asyncio和trio的优点，提供了一致的API")
    print("适合构建高性能的异步应用程序，尤其是网络服务和IO密集型应用")


if __name__ == "__main__":
    # 使用anyio.run()运行主演示
    anyio.run(anyio_main_demo)
