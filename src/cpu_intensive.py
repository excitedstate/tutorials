"""CPU密集型任务示例"""

import time
import numpy as np

def fibonacci(n: int) -> int:
    """递归计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_iter(n: int) -> int:
    """迭代计算斐波那契数列"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

def matrix_multiply(size: int) -> np.ndarray:
    """矩阵乘法计算"""
    # 生成两个随机矩阵
    matrix1 = np.random.rand(size, size)
    matrix2 = np.random.rand(size, size)
    
    # 矩阵乘法运算
    result = np.dot(matrix1, matrix2)
    return result

def cpu_bound_task(task_type: str, n: int) -> tuple[float, any]:
    """执行CPU密集型任务并返回执行时间和结果"""
    start_time = time.time()
    
    if task_type == "fibonacci":
        result = fibonacci(n)
    elif task_type == "fibonacci_iter":
        result = fibonacci_iter(n)
    elif task_type == "matrix":
        result = matrix_multiply(n)
    else:
        raise ValueError(f"Unknown task type: {task_type}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return execution_time, result

if __name__ == "__main__":
    # 测试斐波那契数列计算
    print("=== 斐波那契数列计算 ===")
    time_taken, result = cpu_bound_task("fibonacci", 35)
    print(f"递归计算 fib(35) = {result}, 耗时: {time_taken:.4f}秒")
    
    time_taken, result = cpu_bound_task("fibonacci_iter", 35)
    print(f"迭代计算 fib(35) = {result}, 耗时: {time_taken:.4f}秒")
    
    # 测试矩阵乘法
    print("\n=== 矩阵乘法计算 ===")
    time_taken, result = cpu_bound_task("matrix", 1000)
    print(f"1000x1000 矩阵乘法, 耗时: {time_taken:.4f}秒")
    print(f"结果矩阵形状: {result.shape}")