"""多进程编程测试用例"""

import pytest
import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor
from src.learn_processing import (
    basic_process_demo,
    process_with_args,
    process_with_return_value,
    process_daemon_demo,
    process_exit_codes,
    process_termination,
    process_lock_demo,
    process_semaphore_demo,
    process_event_demo,
    process_condition_demo,
    process_barrier_demo,
    process_race_condition_demo,
    process_pool_demo,
    process_pool_map_demo,
    process_pool_starmap_demo,
    process_pool_async_demo,
    process_pool_exception_demo,
    process_pool_performance_demo,
    producer_consumer_with_queue,
    pipe_communication_demo,
    shared_memory_demo,
    manager_demo,
    reader_writer_pattern,
)

# ===============================================
# 基础进程功能测试
# ===============================================


def test_process_creation():
    """测试进程创建和启动"""

    def worker():
        """简单的进程函数"""
        nonlocal process_executed
        process_executed = True

    process_executed = False

    # 创建并启动进程
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()

    # 验证进程执行
    assert process_executed is True


def test_process_with_args():
    """测试带参数的进程"""

    def worker_with_args(arg1, arg2):
        """带参数的进程函数"""
        nonlocal result
        result = arg1 + arg2

    result = 0

    # 创建并启动带参数的进程
    p = multiprocessing.Process(target=worker_with_args, args=(10, 20))
    p.start()
    p.join()

    # 验证结果
    assert result == 30


def test_process_name():
    """测试进程名称"""

    def worker():
        """简单的进程函数"""
        nonlocal current_process_name
        current_process_name = multiprocessing.current_process().name

    current_process_name = ""

    # 创建并启动带名称的进程
    p = multiprocessing.Process(target=worker, name="TestProcess")
    p.start()
    p.join()

    # 验证进程名称
    assert current_process_name == "TestProcess"


def test_process_is_alive():
    """测试进程的is_alive方法"""

    def worker():
        """休眠1秒的进程函数"""
        time.sleep(1)

    # 创建并启动进程
    p = multiprocessing.Process(target=worker)
    assert p.is_alive() is False

    p.start()
    assert p.is_alive() is True

    p.join()
    assert p.is_alive() is False


def test_process_exit_code():
    """测试进程退出码"""

    def normal_worker():
        """正常结束的进程函数"""
        pass

    def error_worker():
        """异常结束的进程函数"""
        raise ValueError("测试异常")

    # 测试正常结束的进程
    p1 = multiprocessing.Process(target=normal_worker)
    p1.start()
    p1.join()
    assert p1.exitcode == 0

    # 测试异常结束的进程
    p2 = multiprocessing.Process(target=error_worker)
    p2.start()
    p2.join()
    assert p2.exitcode != 0


# ===============================================
# 进程同步机制测试
# ===============================================


def test_process_lock():
    """测试进程锁"""

    # 使用共享内存
    shared_counter = multiprocessing.Value("i", 0)
    lock = multiprocessing.Lock()

    def increment():
        """使用锁递增计数器"""
        for _ in range(10000):
            with lock:
                shared_counter.value += 1

    # 创建两个进程同时递增计数器
    p1 = multiprocessing.Process(target=increment)
    p2 = multiprocessing.Process(target=increment)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # 验证结果，应该没有竞态条件
    assert shared_counter.value == 20000


def test_process_semaphore():
    """测试进程信号量"""

    # 创建信号量，限制同时访问资源的进程数
    semaphore = multiprocessing.Semaphore(2)

    # 记录同时访问资源的进程数
    current_access_count = multiprocessing.Value("i", 0)
    max_concurrent_access = multiprocessing.Value("i", 0)
    access_lock = multiprocessing.Lock()

    def access_resource():
        """访问受信号量保护的资源"""
        with semaphore:
            # 更新当前访问计数
            with access_lock:
                current_access_count.value += 1
                if current_access_count.value > max_concurrent_access.value:
                    max_concurrent_access.value = current_access_count.value

            # 模拟资源访问
            time.sleep(0.1)

            # 减少当前访问计数
            with access_lock:
                current_access_count.value -= 1

    # 创建多个进程同时访问资源
    processes = [multiprocessing.Process(target=access_resource) for _ in range(5)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    # 验证最大并发访问数不超过信号量限制
    assert max_concurrent_access.value <= 2


def test_process_event():
    """测试进程事件"""

    event = multiprocessing.Event()
    event_triggered = multiprocessing.Value("b", False)

    def wait_for_event():
        """等待事件触发的进程"""
        event.wait()  # 等待事件被设置
        event_triggered.value = True

    # 创建并启动进程
    p = multiprocessing.Process(target=wait_for_event)
    p.start()

    # 等待一段时间后触发事件
    time.sleep(0.5)
    event.set()

    p.join()

    # 验证事件被触发
    assert event_triggered.value is True


def test_process_queue():
    """测试进程队列"""

    # 创建进程队列
    queue = multiprocessing.Queue()

    def producer():
        """生产者进程"""
        for i in range(5):
            queue.put(i)

    def consumer():
        """消费者进程"""
        while True:
            try:
                item = queue.get(timeout=1)
                consumed_items.append(item)
                queue.task_done()
            except multiprocessing.queues.Empty:
                break

    consumed_items = []

    # 创建并启动进程
    p1 = multiprocessing.Process(target=producer)
    p2 = multiprocessing.Process(target=consumer)

    p1.start()
    p2.start()

    p1.join()
    queue.join()
    p2.join()

    # 验证队列操作
    assert sorted(consumed_items) == [0, 1, 2, 3, 4]
    assert queue.empty() is True


# ===============================================
# 进程池测试
# ===============================================


def test_process_pool_basic():
    """测试进程池的基本功能"""

    def task(n):
        """简单的任务函数"""
        return n * 2

    # 创建进程池
    with multiprocessing.Pool(processes=2) as pool:
        # 提交任务
        future1 = pool.apply_async(task, (10,))
        future2 = pool.apply_async(task, (20,))

        # 获取结果
        result1 = future1.get()
        result2 = future2.get()

    # 验证结果
    assert result1 == 20
    assert result2 == 40


def test_process_pool_map():
    """测试进程池的map方法"""

    def task(n):
        """简单的任务函数"""
        return n * 2

    # 创建进程池
    with multiprocessing.Pool(processes=3) as pool:
        # 使用map方法执行任务
        inputs = [10, 20, 30, 40]
        results = pool.map(task, inputs)

    # 验证结果
    assert results == [20, 40, 60, 80]


def test_process_pool_starmap():
    """测试进程池的starmap方法"""

    def multiply(a, b):
        """计算乘积的任务函数"""
        return a * b

    # 创建进程池
    with multiprocessing.Pool(processes=2) as pool:
        # 使用starmap方法执行任务
        inputs = [(10, 2), (20, 3), (30, 4)]
        results = pool.starmap(multiply, inputs)

    # 验证结果
    assert results == [20, 60, 120]


def test_process_pool_exception_handling():
    """测试进程池的异常处理"""

    def task_with_exception(n):
        """抛出异常的任务函数"""
        if n == 3:
            raise ValueError(f"测试异常 for {n}")
        return n * 2

    # 创建进程池
    with multiprocessing.Pool(processes=2) as pool:
        # 提交任务
        futures = [pool.apply_async(task_with_exception, (i,)) for i in range(5)]

        # 验证异常被正确捕获
        results = []
        for i, future in enumerate(futures):
            if i == 3:
                with pytest.raises(ValueError, match="测试异常 for 3"):
                    future.get()
            else:
                result = future.get()
                results.append(result)

    # 验证正常结果
    assert results == [0, 2, 4, 8]


# ===============================================
# 经典多进程模式测试
# ===============================================


def test_producer_consumer_simple():
    """测试简单的生产者-消费者模式"""

    queue = multiprocessing.Queue(maxsize=5)

    def producer():
        """简单的生产者"""
        for i in range(5):
            queue.put(i)
            time.sleep(0.1)

    def consumer():
        """简单的消费者"""
        while True:
            try:
                item = queue.get(timeout=1)
                consumed_items.append(item)
                queue.task_done()
            except multiprocessing.queues.Empty:
                break

    consumed_items = []

    # 创建并启动进程
    p1 = multiprocessing.Process(target=producer)
    p2 = multiprocessing.Process(target=consumer)

    p1.start()
    p2.start()

    p1.join()
    queue.join()
    p2.join()

    # 验证所有生产的物品都被消费
    assert len(consumed_items) == 5
    assert set(consumed_items) == {0, 1, 2, 3, 4}


def test_pipe_communication():
    """测试管道通信"""

    def sender(conn):
        """发送数据的进程"""
        messages = ["Hello", "World", 42, None]
        for msg in messages:
            conn.send(msg)
            time.sleep(0.1)
        conn.close()

    def receiver(conn):
        """接收数据的进程"""
        while True:
            try:
                msg = conn.recv()
                if msg is None:
                    break
                received_messages.append(msg)
            except EOFError:
                break

    received_messages = []

    # 创建管道
    parent_conn, child_conn = multiprocessing.Pipe()

    # 创建并启动进程
    p1 = multiprocessing.Process(target=sender, args=(child_conn,))
    p2 = multiprocessing.Process(target=receiver, args=(parent_conn,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # 验证数据传输
    assert received_messages == ["Hello", "World", 42]


def test_shared_memory():
    """测试共享内存"""

    # 创建共享内存变量
    shared_int = multiprocessing.Value("i", 0)
    shared_array = multiprocessing.Array("i", [0] * 5)

    def update_shared():
        """更新共享内存"""
        shared_int.value = 42
        for i in range(len(shared_array)):
            shared_array[i] = i * 2

    # 创建并启动进程
    p = multiprocessing.Process(target=update_shared)
    p.start()
    p.join()

    # 验证共享内存更新
    assert shared_int.value == 42
    assert list(shared_array) == [0, 2, 4, 6, 8]


# ===============================================
# 示例函数调用测试
# ===============================================


@pytest.mark.parametrize(
    "example_func",
    [
        basic_process_demo,
        process_with_args,
        process_with_return_value,
        process_daemon_demo,
        process_exit_codes,
        process_termination,
        process_lock_demo,
        process_semaphore_demo,
        process_event_demo,
        process_condition_demo,
        process_barrier_demo,
        process_race_condition_demo,
        process_pool_demo,
        process_pool_map_demo,
        process_pool_starmap_demo,
        process_pool_async_demo,
        process_pool_exception_demo,
        process_pool_performance_demo,
        producer_consumer_with_queue,
        pipe_communication_demo,
        shared_memory_demo,
        manager_demo,
        reader_writer_pattern,
    ],
)
def test_example_functions(example_func):
    """测试示例函数是否能正常执行"""
    # 只测试函数能正常执行，不验证输出
    example_func()
    assert True  # 如果没有异常，测试通过


# ===============================================
# 性能测试
# ===============================================


def test_process_vs_thread_performance():
    """测试进程与线程在CPU密集型任务上的性能差异"""

    def cpu_bound_task(n):
        """CPU密集型任务"""

        def fib(x):
            if x <= 1:
                return x
            a, b = 0, 1
            for _ in range(2, x + 1):
                a, b = b, a + b
            return b

        return fib(n)

    # 测试参数
    test_cases = [35, 36, 37, 38]

    # 使用进程池执行
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=4) as executor:
        process_results = list(executor.map(cpu_bound_task, test_cases))

    process_time = time.time() - start_time

    # 验证结果正确性
    expected_results = [9227465, 14930352, 24157817, 39088169]
    assert process_results == expected_results

    # 验证执行时间合理
    assert process_time < 10.0  # 在合理范围内即可
