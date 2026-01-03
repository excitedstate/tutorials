"""经典多线程模式示例"""

import threading
import time
import random
from queue import Queue


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
            queue.task_done()
    
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
    queue.join()
    consumer1.join()
    consumer2.join()
    
    print("所有生产者和消费者线程执行完毕")
