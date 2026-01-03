#!/usr/bin/env python3
"""
示例：调用C++扩展模块 matrix_cpp
"""

import sys
import os
import time
import numpy as np

# 将lib目录添加到Python路径
lib_dir = os.path.abspath('../lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

def test_cpp_extension():
    """测试C++扩展模块的性能"""
    print("=== 测试C++扩展模块 matrix_cpp ===")
    
    try:
        import matrix_cpp
        print("✅ 成功导入C++扩展模块 matrix_cpp")
    except ImportError as e:
        print(f"❌ 无法导入C++扩展模块: {e}")
        print("请先编译C++扩展：python setup.py build_ext --inplace")
        return
    
    # 创建矩阵操作对象
    mo = matrix_cpp.MatrixOperations()
    
    print("\n=== 1. 斐波那契数列计算 ===")
    test_n = 40
    
    start_time = time.time()
    result = mo.fibonacci(test_n)
    cpp_time = time.time() - start_time
    
    print(f"fib({test_n}) = {result}")
    print(f"C++扩展耗时: {cpp_time:.6f}秒")
    
    print("\n=== 2. 快速排序算法 ===")
    # 生成随机测试数据
    import random
    test_list = [random.random() * 100 for _ in range(10000)]
    test_list_copy = test_list.copy()
    
    # C++快速排序
    start_time = time.time()
    mo.quick_sort(test_list)
    cpp_sort_time = time.time() - start_time
    
    # Python内置排序
    start_time = time.time()
    test_list_copy.sort()
    python_sort_time = time.time() - start_time
    
    print(f"排序10000个随机数：")
    print(f"C++快速排序耗时: {cpp_sort_time:.6f}秒")
    print(f"Python内置排序耗时: {python_sort_time:.6f}秒")
    print(f"排序结果一致: {test_list == test_list_copy}")
    print(f"性能提升: {python_sort_time/cpp_sort_time:.2f}倍")
    
    print("\n=== 3. 矩阵乘法 ===")
    # 创建两个测试矩阵
    size = 100
    matrix1 = [[random.random() for _ in range(size)] for _ in range(size)]
    matrix2 = [[random.random() for _ in range(size)] for _ in range(size)]
    
    # C++矩阵乘法
    start_time = time.time()
    result_cpp = mo.multiply(matrix1, matrix2)
    cpp_mat_time = time.time() - start_time
    
    # NumPy矩阵乘法作为参考
    np_matrix1 = np.array(matrix1)
    np_matrix2 = np.array(matrix2)
    
    start_time = time.time()
    result_np = np.dot(np_matrix1, np_matrix2)
    np_time = time.time() - start_time
    
    print(f"{size}x{size}矩阵乘法：")
    print(f"C++扩展耗时: {cpp_mat_time:.6f}秒")
    print(f"NumPy耗时: {np_time:.6f}秒")
    print(f"性能对比: C++ / NumPy = {cpp_mat_time/np_time:.2f}倍")
    
    # 验证结果（允许浮点误差）
    result_cpp_np = np.array(result_cpp)
    max_diff = np.max(np.abs(result_cpp_np - result_np))
    print(f"最大误差: {max_diff:.6e}")

def example_usage():
    """展示C++扩展的基本用法"""
    print("\n=== C++扩展基本用法示例 ===")
    
    try:
        import matrix_cpp
        mo = matrix_cpp.MatrixOperations()
    except ImportError:
        return
    
    # 示例1：计算斐波那契数
    print("\n1. 计算斐波那契数：")
    print(f"fib(10) = {mo.fibonacci(10)}")
    print(f"fib(20) = {mo.fibonacci(20)}")
    print(f"fib(30) = {mo.fibonacci(30)}")
    
    # 示例2：排序
    print("\n2. 排序：")
    test_list = [3.1, 1.4, 1.5, 9.2, 6.5, 3.5, 8.9]
    print(f"原始列表: {test_list}")
    mo.quick_sort(test_list)
    print(f"排序后: {test_list}")
    
    # 示例3：直接调用模块函数
    print("\n3. 直接调用模块函数：")
    print(f"fib(15) = {matrix_cpp.fibonacci(15)}")

if __name__ == "__main__":
    test_cpp_extension()
    example_usage()