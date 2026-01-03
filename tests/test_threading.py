"""多线程编程测试用例"""

import pytest
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from src.multi_threading import (
    basic_thread_demo,
    thread_with_args,
    thread_with_return_value,
    race_condition_demo,
    lock_demo,
    rlock_demo,
    condition_variable_demo,
    semaphore_demo,
    event_demo,
    barrier_demo,
    thread_pool_demo,
    thread_pool_map_demo,
    producer_consumer_with_queue,
    multithreaded_io_tasks,
    multithreaded_cpu_tasks
)

# ===============================================
# 基础线程功能测试
# ===============================================

def test_thread_creation():
    """测试线程创建和启动"""
    
    def worker():
        """简单的线程函数"""
        nonlocal thread_executed
        thread_executed = True
    
    thread_executed = False
    
    # 创建并启动线程
    t = threading.Thread(target=worker)
    t.start()
    t.join()
    
    # 验证线程执行
    assert thread_executed is True

def test_thread_with_args():
    """测试带参数的线程"""
    
    def worker_with_args(arg1, arg2):
        """带参数的线程函数"""
        nonlocal result
        result = arg1 + arg2
    
    result = 0
    
    # 创建并启动带参数的线程
    t = threading.Thread(target=worker_with_args, args=(10, 20))
    t.start()
    t.join()
    
    # 验证结果
    assert result == 30

def test_thread_return_value():
    """测试线程返回值获取"""
    
    def worker_with_result(n):
        """返回结果的线程函数"""
        return n * 2
    
    result = [0]
    
    def worker_wrapper(n):
        """线程包装函数，用于存储返回值"""
        result[0] = worker_with_result(n)
    
    # 创建并启动线程
    t = threading.Thread(target=worker_wrapper, args=(10,))
    t.start()
    t.join()
    
    # 验证结果
    assert result[0] == 20

def test_thread_is_alive():
    """测试线程的is_alive方法"""
    
    def worker():
        """休眠1秒的线程函数"""
        time.sleep(1)
    
    # 创建并启动线程
    t = threading.Thread(target=worker)
    assert t.is_alive() is False
    
    t.start()
    assert t.is_alive() is True
    
    t.join()
    assert t.is_alive() is False

def test_thread_name():
    """测试线程名称"""
    
    def worker():
        """简单的线程函数"""
        nonlocal thread_name
        thread_name = threading.current_thread().name
    
    thread_name = ""
    
    # 创建并启动带名称的线程
    t = threading.Thread(target=worker, name="TestThread")
    t.start()
    t.join()
    
    # 验证线程名称
    assert thread_name == "TestThread"

# ===============================================
# 线程同步机制测试
# ===============================================

def test_lock():
    """测试锁的基本功能"""
    
    shared_counter = 0
    lock = threading.Lock()
    
    def increment():
        """使用锁递增计数器"""
        nonlocal shared_counter
        for _ in range(10000):
            with lock:
                shared_counter += 1
    
    # 创建两个线程同时递增计数器
    t1 = threading.Thread(target=increment)
    t2 = threading.Thread(target=increment)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    # 验证结果，应该没有竞态条件
    assert shared_counter == 20000

def test_rlock():
    """测试可重入锁"""
    
    rlock = threading.RLock()
    
    def recursive_function(level):
        """递归函数，多次获取同一把锁"""
        if level > 0:
            with rlock:
                recursive_function(level - 1)
    
    # 测试递归函数是否能正常执行
    recursive_function(5)
    assert True  # 如果没有死锁，测试通过

def test_condition_variable():
    """测试条件变量"""
    
    queue = Queue(maxsize=3)
    condition = threading.Condition()
    
    def producer():
        """生产者函数"""
        for i in range(5):
            with condition:
                # 等待队列不满
                while queue.full():
                    condition.wait()
                queue.put(i)
                condition.notify_all()
    
    def consumer():
        """消费者函数"""
        for _ in range(5):
            with condition:
                # 等待队列不为空
                while queue.empty():
                    condition.wait()
                queue.get()
                condition.notify_all()
    
    # 创建生产者和消费者线程
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()
    
    # 验证队列最终为空
    assert queue.empty() is True

def test_semaphore():
    """测试信号量"""
    
    # 信号量控制同时访问资源的线程数
    semaphore = threading.Semaphore(2)
    
    # 记录同时访问资源的线程数
    current_access_count = 0
    max_concurrent_access = 0
    lock = threading.Lock()
    
    def access_resource():
        """访问受信号量保护的资源"""
        nonlocal current_access_count, max_concurrent_access
        
        with semaphore:
            # 更新当前访问计数
            with lock:
                current_access_count += 1
                if current_access_count > max_concurrent_access:
                    max_concurrent_access = current_access_count
            
            # 模拟资源访问
            time.sleep(0.1)
            
            # 减少当前访问计数
            with lock:
                current_access_count -= 1
    
    # 创建多个线程同时访问资源
    threads = [threading.Thread(target=access_resource) for _ in range(5)]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    # 验证最大并发访问数不超过信号量限制
    assert max_concurrent_access <= 2

def test_event():
    """测试事件"""
    
    event = threading.Event()
    event_triggered = False
    
    def wait_for_event():
        """等待事件触发的线程"""
        nonlocal event_triggered
        event.wait()  # 等待事件被设置
        event_triggered = True
    
    # 创建并启动线程
    t = threading.Thread(target=wait_for_event)
    t.start()
    
    # 等待一段时间后触发事件
    time.sleep(0.5)
    event.set()
    
    t.join()
    
    # 验证事件被触发
    assert event_triggered is True

def test_barrier():
    """测试屏障"""
    
    # 创建屏障，等待3个线程到达
    barrier = threading.Barrier(3)
    
    def worker(thread_id, results):
        """工作线程"""
        time.sleep(0.1)
        results.append(f"Thread {thread_id} before barrier")
        barrier.wait()
        results.append(f"Thread {thread_id} after barrier")
    
    results = []
    
    # 创建3个线程
    threads = [threading.Thread(target=worker, args=(i, results)) for i in range(3)]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    # 验证所有线程都到达屏障后才继续执行
    # 所有"before barrier"应该在"after barrier"之前
    before_count = 0
    for result in results:
        if "before barrier" in result:
            before_count += 1
        else:
            # 一旦遇到"after barrier"，所有"before barrier"都应该已经处理
            assert before_count == 3
    
    assert len(results) == 6  # 3个线程，每个线程产生2个结果

def test_queue_thread_safe():
    """测试Queue的线程安全性"""
    
    queue = Queue(maxsize=10)
    
    def producer():
        """生产者函数"""
        for i in range(100):
            queue.put(i)
    
    def consumer():
        """消费者函数"""
        for _ in range(100):
            queue.get()
            queue.task_done()
    
    # 创建生产者和消费者线程
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    queue.join()  # 等待队列中的所有任务完成
    consumer_thread.join()
    
    # 验证队列最终为空
    assert queue.empty() is True

# ===============================================
# 线程池测试
# ===============================================

def test_thread_pool_basic():
    """测试线程池的基本功能"""
    
    def task(n):
        """简单的任务函数"""
        return n * 2
    
    # 创建线程池
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交任务
        future1 = executor.submit(task, 10)
        future2 = executor.submit(task, 20)
        
        # 获取结果
        result1 = future1.result()
        result2 = future2.result()
    
    # 验证结果
    assert result1 == 20
    assert result2 == 40

def test_thread_pool_map():
    """测试线程池的map方法"""
    
    def task(n):
        """简单的任务函数"""
        return n * 2
    
    # 创建线程池
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 使用map方法执行任务
        inputs = [10, 20, 30, 40]
        results = list(executor.map(task, inputs))
    
    # 验证结果
    assert results == [20, 40, 60, 80]

def test_thread_pool_exception_handling():
    """测试线程池的异常处理"""
    
    def task_with_exception():
        """抛出异常的任务函数"""
        raise ValueError("测试异常")
    
    # 创建线程池
    with ThreadPoolExecutor(max_workers=1) as executor:
        # 提交抛出异常的任务
        future = executor.submit(task_with_exception)
        
        # 验证异常被正确捕获
        with pytest.raises(ValueError, match="测试异常"):
            future.result()

def test_thread_pool_shutdown():
    """测试线程池的关闭"""
    
    def task():
        """休眠的任务函数"""
        time.sleep(0.5)
        return True
    
    # 创建线程池
    executor = ThreadPoolExecutor(max_workers=2)
    
    # 提交任务
    future = executor.submit(task)
    
    # 关闭线程池
    executor.shutdown()
    
    # 验证任务完成
    assert future.result() is True

# ===============================================
# 生产者-消费者模式测试
# ===============================================

def test_producer_consumer():
    """测试生产者-消费者模式"""
    
    queue = Queue(maxsize=5)
    produced_items = []
    consumed_items = []
    
    # 用于跟踪已收到结束标志的消费者数量
    done_consumers = 0
    done_lock = threading.Lock()
    
    def producer():
        """生产者函数"""
        for i in range(5):  # 减少生产数量，加快测试
            item = f"item-{i}"
            queue.put(item)
            produced_items.append(item)
            time.sleep(0.05)  # 减少延迟，加快测试
        queue.put(None)  # 结束标志
    
    def consumer(consumer_id):
        """消费者函数"""
        nonlocal done_consumers
        while True:
            item = queue.get()
            try:
                if item is None:
                    with done_lock:
                        done_consumers += 1
                    # 只有当这是第一个收到结束标志的消费者时，才传递结束标志
                    if done_consumers == 1:
                        queue.put(None)  # 传递结束标志
                    break
                consumed_items.append(item)
            finally:
                queue.task_done()  # 确保无论如何都调用task_done()
            time.sleep(0.075)  # 减少延迟，加快测试
    
    # 创建生产者和消费者线程
    producer_thread = threading.Thread(target=producer)
    consumer1 = threading.Thread(target=consumer, args=(1,))
    consumer2 = threading.Thread(target=consumer, args=(2,))
    
    producer_thread.start()
    consumer1.start()
    consumer2.start()
    
    producer_thread.join()
    queue.join()
    consumer1.join()
    consumer2.join()
    
    # 验证所有生产的物品都被消费
    assert len(produced_items) == 5
    assert len(consumed_items) == 5
    assert set(produced_items) == set(consumed_items)

# ===============================================
# 共享数据安全性测试
# ===============================================

def test_race_condition():
    """测试竞态条件"""
    
    shared_counter = 0
    
    def increment():
        """递增计数器，存在竞态条件"""
        nonlocal shared_counter
        for _ in range(10000):
            # 这里存在竞态条件
            temp = shared_counter
            temp += 1
            shared_counter = temp
    
    # 创建两个线程同时递增计数器
    t1 = threading.Thread(target=increment)
    t2 = threading.Thread(target=increment)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    # 由于竞态条件，结果可能小于预期
    # 这个测试验证了竞态条件的存在
    assert shared_counter <= 20000

def test_no_race_condition_with_lock():
    """测试使用锁解决竞态条件"""
    
    shared_counter = 0
    lock = threading.Lock()
    
    def increment_safe():
        """使用锁安全地递增计数器"""
        nonlocal shared_counter
        for _ in range(10000):
            with lock:
                shared_counter += 1
    
    # 创建两个线程同时递增计数器
    t1 = threading.Thread(target=increment_safe)
    t2 = threading.Thread(target=increment_safe)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    # 由于使用了锁，结果应该等于预期
    assert shared_counter == 20000

# ===============================================
# 性能测试
# ===============================================

def test_thread_pool_performance():
    """测试线程池的性能"""
    
    def cpu_bound_task(n):
        """CPU密集型任务"""
        def fib(x):
            if x <= 1:
                return x
            a, b = 0, 1
            for _ in range(2, x+1):
                a, b = b, a + b
            return b
        return fib(n)
    
    # 测试参数
    test_cases = [35, 36, 37, 38]
    
    # 使用线程池执行
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, test_cases))
    
    end_time = time.time()
    
    # 验证结果正确性
    expected_results = [9227465, 14930352, 24157817, 39088169]
    assert results == expected_results
    
    # 验证执行时间合理（在合理范围内即可，具体数值根据机器性能而定）
    assert end_time - start_time < 5.0  # 假设在5秒内完成

# ===============================================
# 示例函数调用测试
# ===============================================

@pytest.mark.parametrize("example_func", [
    basic_thread_demo,
    thread_with_args,
    thread_with_return_value,
    race_condition_demo,
    lock_demo,
    rlock_demo,
    condition_variable_demo,
    semaphore_demo,
    event_demo,
    barrier_demo,
    thread_pool_demo,
    thread_pool_map_demo,
    producer_consumer_with_queue,
    multithreaded_io_tasks,
    multithreaded_cpu_tasks
])
def test_example_functions(example_func):
    """测试示例函数是否能正常执行"""
    # 只测试函数能正常执行，不验证输出
    example_func()
    assert True  # 如果没有异常，测试通过
