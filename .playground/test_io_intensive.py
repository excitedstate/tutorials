"""IO密集型任务测试用例"""

import pytest
import os
from src.io_intensive import (
    write_large_file,
    read_large_file,
    sync_http_request,
    io_bound_task,
    TEST_URLS
)

@pytest.fixture
def test_file():
    """创建测试文件的fixture"""
    file_path = "test_temp_file.dat"
    yield file_path
    # 清理测试文件
    if os.path.exists(file_path):
        os.remove(file_path)

def test_write_large_file(test_file):
    """测试写入大文件"""
    time_taken = write_large_file(test_file, 1)
    assert time_taken > 0
    assert os.path.exists(test_file)
    assert os.path.getsize(test_file) == 1024 * 1024  # 1MB

def test_read_large_file(test_file):
    """测试读取大文件"""
    # 先写入文件
    write_large_file(test_file, 1)
    
    # 再读取文件
    time_taken = read_large_file(test_file)
    assert time_taken > 0

def test_sync_http_request():
    """测试同步HTTP请求"""
    url = "https://httpbin.org/get"
    time_taken, status_code = sync_http_request(url)
    assert time_taken > 0
    assert status_code == 200

def test_io_bound_task_file_ops(test_file):
    """测试IO密集型任务执行器 - 文件操作"""
    # 测试写入文件
    write_time = io_bound_task("write_file", file_path=test_file, size_mb=1)
    assert write_time > 0
    assert os.path.exists(test_file)
    
    # 测试读取文件
    read_time = io_bound_task("read_file", file_path=test_file)
    assert read_time > 0

def test_io_bound_task_http_ops():
    """测试IO密集型任务执行器 - HTTP请求"""
    # 只测试少量URL，避免测试时间过长
    test_urls = TEST_URLS[:2]
    
    # 测试同步HTTP请求
    sync_time = io_bound_task("sync_http", urls=test_urls)
    assert sync_time > 0
    
    # 测试异步HTTP请求
    async_time = io_bound_task("async_http", urls=test_urls)
    assert async_time > 0
    
    # 异步应该比同步快
    assert async_time < sync_time

def test_io_bound_task_async_file_ops(test_file):
    """测试IO密集型任务执行器 - 异步文件操作"""
    # 测试异步写入文件
    write_time = io_bound_task("async_write_file", file_path=test_file, size_mb=1)
    assert write_time > 0
    assert os.path.exists(test_file)
    
    # 测试异步读取文件
    read_time = io_bound_task("async_read_file", file_path=test_file)
    assert read_time > 0

def test_io_bound_task_invalid_type():
    """测试无效任务类型"""
    with pytest.raises(ValueError):
        io_bound_task("invalid_type")