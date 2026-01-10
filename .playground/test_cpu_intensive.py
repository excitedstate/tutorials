"""CPU密集型任务测试用例"""

import pytest
from src.cpu_intensive import fibonacci, fibonacci_iter, matrix_multiply, cpu_bound_task


def test_fibonacci():
    """测试斐波那契数列计算"""
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55
    assert fibonacci(20) == 6765


def test_fibonacci_iter():
    """测试迭代版斐波那契数列计算"""
    assert fibonacci_iter(0) == 0
    assert fibonacci_iter(1) == 1
    assert fibonacci_iter(10) == 55
    assert fibonacci_iter(20) == 6765
    # 测试大数计算，确保迭代版不会栈溢出
    assert fibonacci_iter(100) > 0


def test_matrix_multiply():
    """测试矩阵乘法"""
    # 测试小矩阵乘法
    result = matrix_multiply(10)
    assert result.shape == (10, 10)

    # 测试中等大小矩阵乘法
    result = matrix_multiply(100)
    assert result.shape == (100, 100)


def test_cpu_bound_task():
    """测试CPU密集型任务执行器"""
    # 测试斐波那契递归
    time_taken, result = cpu_bound_task("fibonacci", 20)
    assert result == 6765
    assert time_taken > 0

    # 测试斐波那契迭代
    time_taken, result = cpu_bound_task("fibonacci_iter", 20)
    assert result == 6765
    assert time_taken > 0

    # 测试矩阵乘法
    time_taken, result = cpu_bound_task("matrix", 50)
    assert result.shape == (50, 50)
    assert time_taken > 0

    # 测试错误任务类型
    with pytest.raises(ValueError):
        cpu_bound_task("unknown", 10)
