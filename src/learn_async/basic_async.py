"""基础异步操作示例"""

import asyncio
import time


async def basic_async_demo():
    """基础异步函数示例"""

    async def async_worker():
        """异步工作函数"""
        print(f"异步函数开始执行")
        await asyncio.sleep(1)  # 模拟异步操作
        print(f"异步函数执行结束")

    print("=== 基础异步函数示例 ===")

    # 直接调用异步函数不会执行，只会返回一个协程对象
    coro = async_worker()
    print(f"直接调用异步函数返回: {coro}")

    # 使用asyncio.run()执行异步函数
    print("使用asyncio.run()执行异步函数:")
    await async_worker()

    print("基础异步函数示例完成")


async def async_with_return_value():
    """带有返回值的异步函数示例"""

    async def compute_square(n: int) -> int:
        """计算平方的异步函数"""
        print(f"开始计算 {n} 的平方")
        await asyncio.sleep(0.5)  # 模拟异步操作
        result = n * n
        print(f"计算完成: {n} 的平方是 {result}")
        return result

    print("\n=== 带有返回值的异步函数示例 ===")

    # 调用带有返回值的异步函数
    result = await compute_square(10)
    print(f"获取异步函数返回值: {result}")

    # 连续调用多个异步函数
    results = []
    for i in range(1, 5):
        res = await compute_square(i)
        results.append(res)

    print(f"多个异步函数结果: {results}")


async def async_await_demo():
    """async和await关键字示例"""

    async def nested_async_function():
        """嵌套的异步函数"""
        print("  进入嵌套异步函数")
        await asyncio.sleep(0.3)
        print("  嵌套异步函数执行完成")
        return "嵌套函数结果"

    async def main_async_function():
        """主异步函数"""
        print("进入主异步函数")

        # 等待嵌套异步函数执行完成
        nested_result = await nested_async_function()
        print(f"获取嵌套函数结果: {nested_result}")

        print("主异步函数执行完成")

    print("\n=== async和await关键字示例 ===")
    await main_async_function()


async def async_function_chaining():
    """异步函数链式调用示例"""

    async def step1():
        """第一步操作"""
        print("执行步骤1")
        await asyncio.sleep(0.5)
        return "步骤1结果"

    async def step2(prev_result):
        """第二步操作，依赖第一步结果"""
        print(f"执行步骤2，使用前一步结果: {prev_result}")
        await asyncio.sleep(0.5)
        return f"{prev_result} -> 步骤2结果"

    async def step3(prev_result):
        """第三步操作，依赖第二步结果"""
        print(f"执行步骤3，使用前一步结果: {prev_result}")
        await asyncio.sleep(0.5)
        return f"{prev_result} -> 步骤3结果"

    print("\n=== 异步函数链式调用示例 ===")

    # 链式调用异步函数
    result1 = await step1()
    result2 = await step2(result1)
    final_result = await step3(result2)

    print(f"最终结果: {final_result}")


async def async_sleep_vs_time_sleep():
    """asyncio.sleep()与time.sleep()的对比"""

    async def demo_async_sleep():
        """使用asyncio.sleep()的示例"""
        print("开始asyncio.sleep()示例")

        async def worker(name: str, delay: float):
            print(f"{name} 开始执行")
            await asyncio.sleep(delay)  # 非阻塞睡眠
            print(f"{name} 执行完成")

        # 并发执行多个异步任务
        await asyncio.gather(
            worker("任务1", 1.0), worker("任务2", 0.5), worker("任务3", 0.8)
        )

        print("asyncio.sleep()示例完成")

    def demo_time_sleep():
        """使用time.sleep()的示例"""
        print("\n开始time.sleep()示例")

        def worker(name: str, delay: float):
            print(f"{name} 开始执行")
            time.sleep(delay)  # 阻塞睡眠
            print(f"{name} 执行完成")

        # 串行执行多个同步任务
        worker("任务1", 1.0)
        worker("任务2", 0.5)
        worker("任务3", 0.8)

        print("time.sleep()示例完成")

    print("=== asyncio.sleep()与time.sleep()对比 ===")

    # 执行异步sleep示例
    await demo_async_sleep()

    # 执行同步sleep示例
    demo_time_sleep()


async def asyncio_run_example():
    """asyncio.run()函数示例"""

    # 注意：asyncio.run() 应该在程序的顶层调用，这里我们使用一个包装函数
    # 因为我们已经在一个异步函数中了

    async def standalone_async_function():
        """独立的异步函数"""
        print("这是一个独立的异步函数")
        await asyncio.sleep(0.5)
        return "独立函数的结果"

    print("\n=== asyncio.run()函数示例 ===")

    # 在实际应用中，你会这样使用：
    # result = asyncio.run(standalone_async_function())

    # 但在当前环境下，我们已经在异步函数中，所以直接调用
    result = await standalone_async_function()
    print(f"独立异步函数的结果: {result}")

    print("asyncio.run()示例完成")
