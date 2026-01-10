"""IO密集型任务示例"""

import time
import os
import requests
import asyncio
import aiohttp
import aiofiles

# 测试用的URL列表
TEST_URLS = [
    "https://httpbin.org/get?delay=1",
    "https://httpbin.org/get?delay=1",
    "https://httpbin.org/get?delay=1",
    "https://httpbin.org/get?delay=1",
    "https://httpbin.org/get?delay=1",
]


def write_large_file(file_path: str, size_mb: int) -> float:
    """写入大文件"""
    start_time = time.time()

    # 创建指定大小的字节数据
    data = b"0" * (1024 * 1024)  # 1MB数据块

    with open(file_path, "wb") as f:
        for _ in range(size_mb):
            f.write(data)

    end_time = time.time()
    return end_time - start_time


def read_large_file(file_path: str) -> float:
    """读取大文件"""
    start_time = time.time()

    with open(file_path, "rb") as f:
        # 分块读取文件
        while f.read(1024 * 1024):
            pass

    end_time = time.time()
    return end_time - start_time


def sync_http_request(url: str) -> tuple[float, int]:
    """同步HTTP请求"""
    start_time = time.time()

    response = requests.get(url)
    status_code = response.status_code

    end_time = time.time()
    return end_time - start_time, status_code


def sync_http_requests(urls: list[str]) -> float:
    """批量同步HTTP请求"""
    start_time = time.time()

    for url in urls:
        sync_http_request(url)

    end_time = time.time()
    return end_time - start_time


async def async_http_request(session: aiohttp.ClientSession, url: str) -> int:
    """异步HTTP请求"""
    async with session.get(url) as response:
        return response.status


async def async_http_requests(urls: list[str]) -> float:
    """批量异步HTTP请求"""
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [async_http_request(session, url) for url in urls]
        await asyncio.gather(*tasks)

    end_time = time.time()
    return end_time - start_time


async def async_write_file(file_path: str, size_mb: int) -> float:
    """异步写入文件"""
    start_time = time.time()

    data = b"0" * (1024 * 1024)  # 1MB数据块

    async with aiofiles.open(file_path, "wb") as f:
        for _ in range(size_mb):
            await f.write(data)

    end_time = time.time()
    return end_time - start_time


async def async_read_file(file_path: str) -> float:
    """异步读取文件"""
    start_time = time.time()

    async with aiofiles.open(file_path, "rb") as f:
        while await f.read(1024 * 1024):
            pass

    end_time = time.time()
    return end_time - start_time


def io_bound_task(task_type: str, **kwargs) -> float:
    """执行IO密集型任务并返回执行时间"""
    if task_type == "write_file":
        return write_large_file(kwargs["file_path"], kwargs["size_mb"])
    elif task_type == "read_file":
        return read_large_file(kwargs["file_path"])
    elif task_type == "sync_http":
        return sync_http_requests(kwargs["urls"])
    elif task_type == "async_http":
        return asyncio.run(async_http_requests(kwargs["urls"]))
    elif task_type == "async_write_file":
        return asyncio.run(async_write_file(kwargs["file_path"], kwargs["size_mb"]))
    elif task_type == "async_read_file":
        return asyncio.run(async_read_file(kwargs["file_path"]))
    else:
        raise ValueError(f"Unknown task type: {task_type}")


if __name__ == "__main__":
    # 测试文件IO
    test_file = "test_large_file.dat"
    print("=== 文件IO测试 ===")

    # 写入文件
    write_time = io_bound_task("write_file", file_path=test_file, size_mb=100)
    print(f"写入100MB文件耗时: {write_time:.4f}秒")

    # 读取文件
    read_time = io_bound_task("read_file", file_path=test_file)
    print(f"读取100MB文件耗时: {read_time:.4f}秒")

    # 清理测试文件
    os.remove(test_file)

    # 测试HTTP请求
    print("\n=== HTTP请求测试 ===")

    # 同步HTTP请求
    sync_time = io_bound_task("sync_http", urls=TEST_URLS)
    print(f"同步5个HTTP请求耗时: {sync_time:.4f}秒")

    # 异步HTTP请求
    async_time = io_bound_task("async_http", urls=TEST_URLS)
    print(f"异步5个HTTP请求耗时: {async_time:.4f}秒")
    print(f"异步比同步快: {sync_time/async_time:.2f}倍")
