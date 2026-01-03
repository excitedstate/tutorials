"""多线程编程示例"""

import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import List, Tuple, Callable, Any

# ===============================================
# 基础线程操作示例
# ===============================================

def basic_thread_demo():
    """基础线程创建和使用示例"""
    
    def worker():
        """线程执行的函数"""
        print(f"线程 {threading.current_thread().name} 开始执行")
        time.sleep(1)
        print(f"线程 {threading.current_thread().name} 执行结束")
    
    print("=== 基础线程示例 ===")
    
    # 创建线程
    t1 = threading.Thread(target=worker, name="Worker-1")
    t2 = threading.Thread(target=worker, name="Worker-2")
    
    # 启动线程
    t1.start()
    t2.start()
    
    # 等待线程结束
    t1.join()
    t2.join()
    
    print("所有线程执行完毕")

def thread_with_args():
    """带参数的线程示例"""
    
    def worker_with_args(name: str, delay: float):
        """带参数的线程函数"""
        print(f"线程 {name} 开始执行，延迟 {delay} 秒")
        time.sleep(delay)
        print(f"线程 {name} 执行结束")
    
    print("\n=== 带参数的线程示例 ===")
    
    # 创建带参数的线程
    threads = []
    for i in range(3):
        delay = random.uniform(0.5, 1.5)
        t = threading.Thread(
            target=worker_with_args, 
            name=f"Worker-{i+1}",
            args=(f"Worker-{i+1}", delay)
        )
        threads.append(t)
        t.start()
    
    # 等待所有线程结束
    for t in threads:
        t.join()
    
    print("所有带参数的线程执行完毕")

def thread_with_return_value():
    """获取线程返回值的示例"""
    
    def worker_with_result(n: int) -> int:
        """计算斐波那契数的线程函数"""
        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n+1):
                a, b = b, a + b
            return b
        
        result = fib(n)
        print(f"线程 {threading.current_thread().name} 计算 fib({n}) = {result}")
        return result
    
    print("\n=== 获取线程返回值示例 ===")
    
    # 使用列表存储结果
    results = []
    
    def worker_wrapper(n: int):
        """线程包装函数，用于存储返回值"""
        result = worker_with_result(n)
        results.append(result)
    
    # 创建并启动线程
    t1 = threading.Thread(target=worker_wrapper, args=(35,), name="Fib-1")
    t2 = threading.Thread(target=worker_wrapper, args=(36,), name="Fib-2")
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"线程返回结果: {results}")

# ===============================================
# 线程同步机制示例
# ===============================================

# 共享变量示例
shared_counter = 0
def race_condition_demo():
    """竞态条件示例"""
    global shared_counter
    shared_counter = 0
    
    def increment_counter():
        """递增共享计数器"""
        global shared_counter
        for _ in range(100000):
            # 这里存在竞态条件
            temp = shared_counter
            temp += 1
            shared_counter = temp
    
    print("\n=== 竞态条件示例 ===")
    print(f"初始计数器值: {shared_counter}")
    
    # 创建两个线程同时修改共享变量
    t1 = threading.Thread(target=increment_counter)
    t2 = threading.Thread(target=increment_counter)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"最终计数器值: {shared_counter}")
    print(f"期望计数器值: 200000")
    print(f"差异: {200000 - shared_counter}")

def lock_demo():
    """使用锁解决竞态条件示例"""
    global shared_counter
    shared_counter = 0
    
    # 创建锁
    lock = threading.Lock()
    
    def increment_counter_safe():
        """使用锁安全地递增共享计数器"""
        global shared_counter
        for _ in range(100000):
            with lock:  # 获取锁，自动释放
                temp = shared_counter
                temp += 1
                shared_counter = temp
    
    print("\n=== 使用锁解决竞态条件示例 ===")
    print(f"初始计数器值: {shared_counter}")
    
    # 创建两个线程同时修改共享变量
    t1 = threading.Thread(target=increment_counter_safe)
    t2 = threading.Thread(target=increment_counter_safe)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print(f"最终计数器值: {shared_counter}")
    print(f"期望计数器值: 200000")

def rlock_demo():
    """可重入锁示例"""
    
    def recursive_function(level: int):
        """递归函数，演示可重入锁"""
        if level > 0:
            print(f"递归层级 {level}: 尝试获取锁")
            with rlock:  # 可重入锁允许同一线程多次获取
                print(f"递归层级 {level}: 成功获取锁")
                recursive_function(level - 1)
            print(f"递归层级 {level}: 释放锁")
    
    print("\n=== 可重入锁示例 ===")
    
    rlock = threading.RLock()
    recursive_function(3)

def condition_variable_demo():
    """条件变量示例"""
    
    queue = Queue(maxsize=5)
    condition = threading.Condition()
    
    def producer():
        """生产者线程"""
        for i in range(10):
            with condition:
                # 等待队列不满
                while queue.full():
                    print(f"生产者: 队列已满，等待消费者消费")
                    condition.wait()
                
                # 生产数据
                item = f"item-{i}"
                queue.put(item)
                print(f"生产者: 生产了 {item}")
                
                # 通知消费者
                condition.notify_all()
            time.sleep(random.uniform(0.1, 0.3))
    
    def consumer(consumer_id: int):
        """消费者线程"""
        for _ in range(5):
            with condition:
                # 等待队列不为空
                while queue.empty():
                    print(f"消费者 {consumer_id}: 队列空，等待生产者生产")
                    condition.wait()
                
                # 消费数据
                item = queue.get()
                print(f"消费者 {consumer_id}: 消费了 {item}")
                
                # 通知生产者
                condition.notify_all()
            time.sleep(random.uniform(0.2, 0.5))
    
    print("\n=== 条件变量示例 (生产者-消费者模式) ===")
    
    # 创建生产者和消费者线程
    producer_thread = threading.Thread(target=producer, name="Producer")
    consumer1 = threading.Thread(target=consumer, args=(1,), name="Consumer-1")
    consumer2 = threading.Thread(target=consumer, args=(2,), name="Consumer-2")
    
    # 启动线程
    producer_thread.start()
    consumer1.start()
    consumer2.start()
    
    # 等待线程结束
    producer_thread.join()
    consumer1.join()
    consumer2.join()

def semaphore_demo():
    """信号量示例"""
    
    # 信号量控制同时访问资源的线程数
    semaphore = threading.Semaphore(2)
    
    def access_resource(thread_id: int):
        """访问受信号量保护的资源"""
        print(f"线程 {thread_id}: 尝试访问资源")
        with semaphore:
            print(f"线程 {thread_id}: 成功访问资源")
            time.sleep(random.uniform(0.5, 1.5))
            print(f"线程 {thread_id}: 释放资源")
    
    print("\n=== 信号量示例 ===")
    
    # 创建多个线程同时访问资源
    threads = []
    for i in range(5):
        t = threading.Thread(target=access_resource, args=(i+1,), name=f"Thread-{i+1}")
        threads.append(t)
        t.start()
    
    # 等待所有线程结束
    for t in threads:
        t.join()

def event_demo():
    """事件示例"""
    
    # 创建事件对象
    event = threading.Event()
    
    def wait_for_event(thread_id: int):
        """等待事件触发的线程"""
        print(f"线程 {thread_id}: 等待事件触发")
        event.wait()  # 等待事件被设置
        print(f"线程 {thread_id}: 事件已触发，继续执行")
    
    print("\n=== 事件示例 ===")
    
    # 创建多个等待事件的线程
    threads = []
    for i in range(3):
        t = threading.Thread(target=wait_for_event, args=(i+1,), name=f"Waiter-{i+1}")
        threads.append(t)
        t.start()
    
    # 主线程等待一段时间后触发事件
    time.sleep(2)
    print("主线程: 触发事件")
    event.set()  # 设置事件
    
    # 等待所有线程结束
    for t in threads:
        t.join()

def barrier_demo():
    """屏障示例"""
    
    # 创建屏障，等待5个线程到达
    barrier = threading.Barrier(5)
    
    def worker(thread_id: int):
        """工作线程，到达屏障后继续执行"""
        print(f"线程 {thread_id}: 开始执行")
        time.sleep(random.uniform(0.5, 2.0))
        print(f"线程 {thread_id}: 到达屏障")
        
        # 等待所有线程到达屏障
        barrier.wait()
        
        print(f"线程 {thread_id}: 屏障已通过，继续执行")
    
    print("\n=== 屏障示例 ===")
    
    # 创建5个工作线程
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i+1,), name=f"Worker-{i+1}")
        threads.append(t)
        t.start()
    
    # 等待所有线程结束
    for t in threads:
        t.join()

# ===============================================
# 线程池示例
# ===============================================

def thread_pool_demo():
    """线程池示例"""
    
    def task(n: int) -> Tuple[int, int]:
        """线程池执行的任务"""
        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n+1):
                a, b = b, a + b
            return b
        
        result = fib(n)
        print(f"线程 {threading.current_thread().name} 计算 fib({n}) = {result}")
        return n, result
    
    print("\n=== 线程池示例 ===")
    
    # 创建线程池，最大线程数为4
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交任务到线程池
        futures = [executor.submit(task, i) for i in [35, 36, 37, 38, 39, 40]]
        
        # 获取任务结果
        results = []
        for future in futures:
            n, result = future.result()
            results.append((n, result))
    
    print(f"线程池执行结果: {results}")

def thread_pool_map_demo():
    """线程池map方法示例"""
    
    def task(n: int) -> int:
        """线程池执行的任务"""
        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n+1):
                a, b = b, a + b
            return b
        
        result = fib(n)
        print(f"线程 {threading.current_thread().name} 计算 fib({n}) = {result}")
        return result
    
    print("\n=== 线程池map方法示例 ===")
    
    # 创建线程池
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 使用map方法执行任务
        inputs = [35, 36, 37, 38]
        results = list(executor.map(task, inputs))
    
    print(f"输入: {inputs}")
    print(f"输出: {results}")

# ===============================================
# 经典多线程模式示例
# ===============================================

def producer_consumer_with_queue():
    """使用Queue实现生产者-消费者模式"""
    
    # 创建线程安全的队列
    queue = Queue(maxsize=10)
    
    def producer(name: str, items: int):
        """生产者函数"""
        for i in range(items):
            item = f"{name}-item-{i}"
            queue.put(item)
            print(f"生产者 {name}: 生产了 {item}, 队列大小: {queue.qsize()}")
            time.sleep(random.uniform(0.1, 0.5))
        # 生产结束标志
        queue.put(None)
    
    def consumer(name: str):
        """消费者函数"""
        while True:
            item = queue.get()
            if item is None:
                # 把结束标志放回队列，让其他消费者知道
                queue.put(None)
                break
            print(f"消费者 {name}: 消费了 {item}, 队列大小: {queue.qsize()}")
            time.sleep(random.uniform(0.2, 0.8))
    
    print("\n=== 使用Queue实现生产者-消费者模式 ===")
    
    # 创建生产者和消费者线程
    producer1 = threading.Thread(target=producer, args=("P1", 10), name="Producer-1")
    producer2 = threading.Thread(target=producer, args=("P2", 10), name="Producer-2")
    consumer1 = threading.Thread(target=consumer, args=("C1",), name="Consumer-1")
    consumer2 = threading.Thread(target=consumer, args=("C2",), name="Consumer-2")
    
    # 启动线程
    producer1.start()
    producer2.start()
    consumer1.start()
    consumer2.start()
    
    # 等待线程结束
    producer1.join()
    producer2.join()
    consumer1.join()
    consumer2.join()
    
    print("所有生产者和消费者线程执行完毕")

# ===============================================
# 多线程与不同类型任务结合示例
# ===============================================

def multithreaded_io_tasks():
    """多线程处理IO密集型任务示例"""
    
    def io_task(task_id: int):
        """模拟IO密集型任务"""
        print(f"IO任务 {task_id}: 开始执行")
        time.sleep(random.uniform(1.0, 2.0))  # 模拟IO等待
        result = f"IO任务 {task_id} 结果"
        print(f"IO任务 {task_id}: 执行完毕")
        return result
    
    print("\n=== 多线程处理IO密集型任务 ===")
    
    # 使用线程池处理IO任务
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(io_task, i) for i in range(10)]
        results = [future.result() for future in futures]
    
    end_time = time.time()
    
    print(f"\n所有IO任务执行完毕，耗时: {end_time - start_time:.2f}秒")
    print(f"结果: {results}")

def multithreaded_cpu_tasks():
    """多线程处理CPU密集型任务示例"""
    
    def cpu_task(n: int) -> int:
        """模拟CPU密集型任务（计算斐波那契数）"""
        def fib(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n+1):
                a, b = b, a + b
            return b
        
        result = fib(n)
        print(f"CPU任务 fib({n}) = {result} 执行完毕")
        return result
    
    print("\n=== 多线程处理CPU密集型任务 ===")
    
    # 使用线程池处理CPU任务
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        inputs = [38, 38, 38, 38]
        results = list(executor.map(cpu_task, inputs))
    
    end_time = time.time()
    
    print(f"\n所有CPU任务执行完毕，耗时: {end_time - start_time:.2f}秒")
    print(f"结果: {results}")

# ===============================================
# 运行所有示例
# ===============================================

if __name__ == "__main__":
    # 运行基础线程示例
    basic_thread_demo()
    thread_with_args()
    thread_with_return_value()
    
    # 运行线程同步示例
    race_condition_demo()
    lock_demo()
    rlock_demo()
    condition_variable_demo()
    semaphore_demo()
    event_demo()
    barrier_demo()
    
    # 运行线程池示例
    thread_pool_demo()
    thread_pool_map_demo()
    
    # 运行经典模式示例
    producer_consumer_with_queue()
    
    # 运行不同类型任务示例
    multithreaded_io_tasks()
    multithreaded_cpu_tasks()
