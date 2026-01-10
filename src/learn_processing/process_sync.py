"""进程同步机制示例"""

import multiprocessing
import time


def process_lock_demo():
    """进程锁示例"""

    # 共享计数器
    shared_counter = multiprocessing.Value("i", 0)
    # 创建进程锁
    lock = multiprocessing.Lock()

    def increment():
        """使用锁递增计数器"""
        for _ in range(10000):
            with lock:
                shared_counter.value += 1

    print("=== 进程锁示例 ===")
    print(f"初始计数器值: {shared_counter.value}")

    # 创建两个进程同时递增计数器
    p1 = multiprocessing.Process(target=increment, name="Increment-1")
    p2 = multiprocessing.Process(target=increment, name="Increment-2")

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"最终计数器值: {shared_counter.value}")
    print(f"预期计数器值: 20000")
    print(f"计数器是否正确: {shared_counter.value == 20000}")


def process_semaphore_demo():
    """进程信号量示例"""

    # 创建信号量，限制同时访问资源的进程数为2
    semaphore = multiprocessing.Semaphore(2)

    def access_resource(process_id):
        """访问受信号量保护的资源"""
        print(f"进程 {process_id} 尝试访问资源")
        with semaphore:
            print(f"进程 {process_id} 成功访问资源")
            time.sleep(1)  # 模拟资源访问
            print(f"进程 {process_id} 释放资源")

    print("\n=== 进程信号量示例 ===")

    # 创建5个进程同时访问资源
    processes = []
    for i in range(5):
        p = multiprocessing.Process(
            target=access_resource, args=(i,), name=f"Resource-User-{i}"
        )
        processes.append(p)
        p.start()

    # 等待所有进程结束
    for p in processes:
        p.join()

    print("所有进程访问资源完成")


def process_event_demo():
    """进程事件示例"""

    # 创建事件
    event = multiprocessing.Event()

    def wait_for_event(process_id):
        """等待事件触发的进程"""
        print(f"进程 {process_id} 等待事件触发")
        event.wait()  # 等待事件被设置
        print(f"进程 {process_id} 收到事件，开始执行")
        time.sleep(0.5)  # 模拟事件处理
        print(f"进程 {process_id} 事件处理完成")

    print("\n=== 进程事件示例 ===")

    # 创建3个等待事件的进程
    processes = []
    for i in range(3):
        p = multiprocessing.Process(
            target=wait_for_event, args=(i,), name=f"Event-Waiter-{i}"
        )
        processes.append(p)
        p.start()

    # 主进程休眠1秒后触发事件
    time.sleep(1)
    print("主进程触发事件")
    event.set()  # 设置事件

    # 等待所有进程结束
    for p in processes:
        p.join()

    print("所有事件处理进程完成")


def process_condition_demo():
    """进程条件变量示例"""

    # 创建条件变量
    condition = multiprocessing.Condition()
    # 共享资源
    shared_list = multiprocessing.Manager().list()

    def producer():
        """生产者进程"""
        for i in range(5):
            time.sleep(0.5)  # 模拟生产过程
            with condition:
                shared_list.append(f"item-{i}")
                print(f"生产者生产: item-{i}")
                # 通知消费者有新物品可用
                condition.notify_all()

    def consumer(process_id):
        """消费者进程"""
        for _ in range(3):
            with condition:
                # 等待直到列表不为空
                while not shared_list:
                    condition.wait()
                # 消费物品
                item = shared_list.pop(0)
                print(f"消费者 {process_id} 消费: {item}")

    print("\n=== 进程条件变量示例 ===")

    # 创建生产者和消费者进程
    producer_process = multiprocessing.Process(target=producer, name="Producer")
    consumer1 = multiprocessing.Process(target=consumer, args=(1,), name="Consumer-1")
    consumer2 = multiprocessing.Process(target=consumer, args=(2,), name="Consumer-2")

    # 启动进程
    producer_process.start()
    consumer1.start()
    consumer2.start()

    # 等待所有进程结束
    producer_process.join()
    consumer1.join()
    consumer2.join()

    print("生产消费过程完成")


def process_barrier_demo():
    """进程屏障示例"""

    # 创建屏障，等待3个进程到达
    barrier = multiprocessing.Barrier(3)

    def worker(process_id):
        """工作进程"""
        print(f"进程 {process_id} 开始执行")
        time.sleep(process_id * 0.5)  # 不同进程休眠不同时间
        print(f"进程 {process_id} 到达屏障")
        barrier.wait()  # 等待所有进程到达屏障
        print(f"进程 {process_id} 穿过屏障，继续执行")

    print("\n=== 进程屏障示例 ===")

    # 创建3个进程
    processes = []
    for i in range(3):
        p = multiprocessing.Process(
            target=worker, args=(i,), name=f"Barrier-Worker-{i}"
        )
        processes.append(p)
        p.start()

    # 等待所有进程结束
    for p in processes:
        p.join()

    print("所有进程完成执行")


def process_race_condition_demo():
    """进程竞态条件示例"""

    # 共享计数器（无锁保护）
    shared_counter = multiprocessing.Value("i", 0)

    def increment():
        """递增计数器，存在竞态条件"""
        for _ in range(10000):
            # 这里存在竞态条件
            temp = shared_counter.value
            temp += 1
            shared_counter.value = temp

    print("\n=== 进程竞态条件示例 ===")
    print(f"初始计数器值: {shared_counter.value}")

    # 创建两个进程同时递增计数器
    p1 = multiprocessing.Process(target=increment, name="Race-1")
    p2 = multiprocessing.Process(target=increment, name="Race-2")

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"最终计数器值: {shared_counter.value}")
    print(f"预期计数器值: 20000")
    print(f"是否发生竞态条件: {shared_counter.value < 20000}")
