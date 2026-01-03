#!/usr/bin/env python3
"""
示例：调用Rust扩展模块 fib_rust
"""

import sys
import os
import time
import random

# 将lib目录添加到Python路径
lib_dir = os.path.abspath('../lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

def test_rust_extension():
    """测试Rust扩展模块的性能"""
    print("=== 测试Rust扩展模块 fib_rust ===")
    
    try:
        import fib_rust
        print("✅ 成功导入Rust扩展模块 fib_rust")
    except ImportError as e:
        print(f"❌ 无法导入Rust扩展模块: {e}")
        print("请先编译Rust扩展：")
        print("  cd rust_extension")
        print("  cargo build --release")
        print("  cp target/release/libfib_rust.dylib ../lib/fib_rust.so")
        return
    
    print("\n=== 1. 斐波那契数列计算 ===")
    test_n = 40
    
    # Rust迭代实现
    start_time = time.time()
    rust_iter_result = fib_rust.fibonacci_iter_py(test_n)
    rust_iter_time = time.time() - start_time
    print(f"Rust迭代 fib({test_n}) = {rust_iter_result}")
    print(f"耗时: {rust_iter_time:.6f}秒")
    
    # Rust递归实现
    start_time = time.time()
    rust_recursive_result = fib_rust.fibonacci_py(test_n)
    rust_recursive_time = time.time() - start_time
    print(f"Rust递归 fib({test_n}) = {rust_recursive_result}")
    print(f"耗时: {rust_recursive_time:.6f}秒")
    
    print("\n=== 2. 快速排序算法 ===")
    # 生成随机测试数据
    test_list = [random.random() * 100 for _ in range(10000)]
    test_list_copy = test_list.copy()
    
    # Rust快速排序
    start_time = time.time()
    rust_sorted = fib_rust.quick_sort_py(test_list)
    rust_sort_time = time.time() - start_time
    
    # Python内置排序
    start_time = time.time()
    test_list_copy.sort()
    python_sort_time = time.time() - start_time
    
    print(f"排序10000个随机数：")
    print(f"Rust快速排序耗时: {rust_sort_time:.6f}秒")
    print(f"Python内置排序耗时: {python_sort_time:.6f}秒")
    print(f"排序结果一致: {rust_sorted == test_list_copy}")
    
    if python_sort_time > rust_sort_time:
        print(f"性能提升: {python_sort_time/rust_sort_time:.2f}倍")
    else:
        print(f"Python内置排序更快: {rust_sort_time/python_sort_time:.2f}倍")

def batch_test():
    """批量测试，展示Rust扩展在多任务下的优势"""
    print("\n=== 批量测试 ===")
    
    try:
        import fib_rust
    except ImportError:
        return
    
    # 测试多个斐波那契数计算
    test_cases = [35, 36, 37, 38]
    
    print("\n批量计算斐波那契数：")
    start_time = time.time()
    results = [fib_rust.fibonacci_iter_py(n) for n in test_cases]
    total_time = time.time() - start_time
    
    for i, (n, result) in enumerate(zip(test_cases, results)):
        print(f"fib({n}) = {result}")
    
    print(f"\n总耗时: {total_time:.4f}秒")
    print(f"平均耗时: {total_time/len(test_cases):.4f}秒/个")

def compare_with_c():
    """与C扩展进行性能对比"""
    print("\n=== 与C扩展性能对比 ===")
    
    try:
        import fib_rust
        import fib_c
    except ImportError as e:
        print(f"无法导入扩展模块: {e}")
        return
    
    test_n = 40
    
    print(f"\n比较 fib({test_n}) 计算性能：")
    
    # C扩展
    start_time = time.time()
    c_result = fib_c.fibonacci_iter(test_n)
    c_time = time.time() - start_time
    
    # Rust扩展
    start_time = time.time()
    rust_result = fib_rust.fibonacci_iter_py(test_n)
    rust_time = time.time() - start_time
    
    print(f"C扩展: 结果={c_result}, 耗时={c_time:.6f}秒")
    print(f"Rust扩展: 结果={rust_result}, 耗时={rust_time:.6f}秒")
    
    if c_time > rust_time:
        print(f"Rust比C快: {c_time/rust_time:.2f}倍")
    else:
        print(f"C比Rust快: {rust_time/c_time:.2f}倍")

if __name__ == "__main__":
    test_rust_extension()
    batch_test()
    compare_with_c()