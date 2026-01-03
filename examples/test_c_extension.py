#!/usr/bin/env python3
"""
示例：调用C扩展模块 fib_c
"""

import sys
import os
import time
from src.cpu_intensive import fibonacci_iter as py_fib_iter

# 将lib目录添加到Python路径
lib_dir = os.path.abspath('../lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

def test_c_extension():
    """测试C扩展模块的性能"""
    print("=== 测试C扩展模块 fib_c ===")
    
    try:
        import fib_c
        print("✅ 成功导入C扩展模块 fib_c")
    except ImportError as e:
        print(f"❌ 无法导入C扩展模块: {e}")
        print("请先编译C扩展：python setup.py build_ext --inplace")
        return
    
    # 性能对比测试
    test_n = 40
    print(f"\n测试 fib({test_n}) 计算性能：")
    
    # Python实现
    start_time = time.time()
    py_result = py_fib_iter(test_n)
    py_time = time.time() - start_time
    print(f"Python实现: 结果={py_result}, 耗时={py_time:.6f}秒")
    
    # C扩展实现
    start_time = time.time()
    c_result = fib_c.fibonacci_iter(test_n)
    c_time = time.time() - start_time
    print(f"C扩展实现: 结果={c_result}, 耗时={c_time:.6f}秒")
    
    # 递归版本对比
    print(f"\n测试递归 fib({test_n}) 计算性能：")
    
    start_time = time.time()
    c_recursive_result = fib_c.fibonacci(test_n)
    c_recursive_time = time.time() - start_time
    print(f"C扩展递归: 结果={c_recursive_result}, 耗时={c_recursive_time:.6f}秒")
    
    print(f"\n性能提升：")
    print(f"- 迭代版: {py_time/c_time:.2f}倍")
    print(f"- 递归版: Python递归过慢，仅展示C扩展递归结果")

def batch_test():
    """批量测试，展示C扩展在多任务下的优势"""
    print("\n=== 批量测试 ===")
    
    try:
        import fib_c
    except ImportError:
        return
    
    # 测试多个斐波那契数计算
    test_cases = [35, 36, 37, 38]
    
    print("\n批量计算斐波那契数：")
    start_time = time.time()
    results = [fib_c.fibonacci_iter(n) for n in test_cases]
    total_time = time.time() - start_time
    
    for i, (n, result) in enumerate(zip(test_cases, results)):
        print(f"fib({n}) = {result}")
    
    print(f"\n总耗时: {total_time:.4f}秒")
    print(f"平均耗时: {total_time/len(test_cases):.4f}秒/个")

if __name__ == "__main__":
    test_c_extension()
    batch_test()