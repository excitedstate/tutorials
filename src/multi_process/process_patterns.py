"""经典多进程模式示例"""

import multiprocessing
import time
from typing import List, Any


def producer_consumer_with_queue():
    """使用队列的生产者-消费者模式示例"""
    
    # 创建一个队列，用于进程间通信
    queue = multiprocessing.Queue(maxsize=5)
    
    def producer():
        """生产者进程"""
        for i in range(10):
            item = f"item-{i}"
            print(f"生产者生产: {item}")
            queue.put(item)  # 将物品放入队列
            print(f"队列大小: {queue.qsize()}")
            time.sleep(0.3)  # 模拟生产速度
    
    def consumer(consumer_id):
        """消费者进程"""
        while True:
            try:
                # 从队列获取物品，设置超时时间
                item = queue.get(timeout=2)
                print(f"消费者 {consumer_id} 消费: {item}")
                queue.task_done()  # 标记任务完成
                time.sleep(0.5)  # 模拟消费速度
            except multiprocessing.queues.Empty:
                print(f"消费者 {consumer_id} 等待超时，退出")
                break
    
    print("=== 生产者-消费者模式示例 ===")
    
    # 创建生产者和消费者进程
    producer_process = multiprocessing.Process(target=producer, name="Producer")
    consumer1 = multiprocessing.Process(target=consumer, args=(1,), name="Consumer-1")
    consumer2 = multiprocessing.Process(target=consumer, args=(2,), name="Consumer-2")
    
    # 启动进程
    producer_process.start()
    consumer1.start()
    consumer2.start()
    
    # 等待生产者完成
    producer_process.join()
    
    # 等待队列中的所有物品被消费
    queue.join()
    
    # 通知消费者退出
    # 由于消费者使用了超时机制，不需要额外的退出信号
    
    # 等待消费者退出
    consumer1.join()
    consumer2.join()
    
    print("生产消费过程完成")


def pipe_communication_demo():
    """管道通信示例"""
    
    def sender(conn):
        """发送数据的进程"""
        try:
            # 发送不同类型的数据
            messages = [
                "Hello from sender",
                42,
                [1, 2, 3, 4, 5],
                {"key": "value", "number": 123},
                None  # 结束标志
            ]
            
            for message in messages:
                print(f"发送方发送: {message}")
                conn.send(message)
                time.sleep(0.5)
        finally:
            conn.close()  # 关闭连接
    
    def receiver(conn):
        """接收数据的进程"""
        try:
            while True:
                message = conn.recv()  # 接收数据
                print(f"接收方接收: {message}")
                
                if message is None:
                    print("接收方收到结束标志，退出")
                    break
        finally:
            conn.close()  # 关闭连接
    
    print("\n=== 管道通信示例 ===")
    
    # 创建管道，返回两个连接对象
    parent_conn, child_conn = multiprocessing.Pipe()
    
    # 创建发送和接收进程
    sender_process = multiprocessing.Process(target=sender, args=(child_conn,), name="Sender")
    receiver_process = multiprocessing.Process(target=receiver, args=(parent_conn,), name="Receiver")
    
    # 启动进程
    sender_process.start()
    receiver_process.start()
    
    # 等待进程结束
    sender_process.join()
    receiver_process.join()
    
    print("管道通信完成")


def shared_memory_demo():
    """共享内存示例"""
    
    # 创建共享内存变量
    # 'i' 表示整数类型，初始值为0
    shared_int = multiprocessing.Value('i', 0)
    
    # 'd' 表示双精度浮点数类型，初始值为0.0
    shared_double = multiprocessing.Value('d', 0.0)
    
    # 使用Array创建共享数组
    # 'i' 表示整数类型，数组长度为5，初始值全为0
    shared_array = multiprocessing.Array('i', [0] * 5)
    
    def update_shared_memory():
        """更新共享内存的进程"""
        # 修改共享整数
        shared_int.value = 42
        
        # 修改共享浮点数
        shared_double.value = 3.14159
        
        # 修改共享数组
        for i in range(len(shared_array)):
            shared_array[i] = i * 2
    
    print("\n=== 共享内存示例 ===")
    
    # 打印初始值
    print(f"初始共享整数: {shared_int.value}")
    print(f"初始共享浮点数: {shared_double.value}")
    print(f"初始共享数组: {list(shared_array)}")
    
    # 创建进程更新共享内存
    update_process = multiprocessing.Process(target=update_shared_memory, name="Update-Process")
    update_process.start()
    update_process.join()
    
    # 打印更新后的值
    print(f"更新后共享整数: {shared_int.value}")
    print(f"更新后共享浮点数: {shared_double.value}")
    print(f"更新后共享数组: {list(shared_array)}")
    
    print("共享内存操作完成")


def manager_demo():
    """使用Manager进行进程间共享数据示例"""
    
    # 创建一个Manager对象
    with multiprocessing.Manager() as manager:
        # 使用Manager创建共享数据结构
        shared_dict = manager.dict()
        shared_list = manager.list()
        shared_namespace = manager.Namespace()
        
        # 设置初始值
        shared_namespace.counter = 0
        
        def worker(process_id):
            """修改共享数据的进程"""
            # 修改共享字典
            shared_dict[f"process-{process_id}"] = process_id * 10
            
            # 修改共享列表
            shared_list.append(f"item-from-{process_id}")
            
            # 修改共享命名空间
            shared_namespace.counter += 1
            
            # 模拟工作时间
            time.sleep(0.2)
        
        print("\n=== Manager共享数据示例 ===")
        print(f"初始共享字典: {dict(shared_dict)}")
        print(f"初始共享列表: {list(shared_list)}")
        print(f"初始计数器: {shared_namespace.counter}")
        
        # 创建多个进程修改共享数据
        processes = []
        for i in range(5):
            p = multiprocessing.Process(target=worker, args=(i,), name=f"Worker-{i}")
            processes.append(p)
            p.start()
        
        # 等待所有进程结束
        for p in processes:
            p.join()
        
        # 打印最终结果
        print(f"最终共享字典: {dict(shared_dict)}")
        print(f"最终共享列表: {list(shared_list)}")
        print(f"最终计数器: {shared_namespace.counter}")
        
        print("Manager共享数据操作完成")


def reader_writer_pattern():
    """读者-写者模式示例"""
    
    # 创建读写锁
    # 注意：Python标准库中没有直接的读写锁，这里使用Rlock模拟
    # 在实际应用中，可以使用第三方库如readerwriterlock
    lock = multiprocessing.RLock()
    shared_data = multiprocessing.Value('i', 0)
    
    def reader(reader_id):
        """读者进程"""
        for _ in range(5):
            with lock:
                print(f"读者 {reader_id} 读取数据: {shared_data.value}")
            time.sleep(0.2)
    
    def writer():
        """写者进程"""
        for i in range(1, 6):
            with lock:
                shared_data.value = i
                print(f"写者写入数据: {shared_data.value}")
            time.sleep(0.5)
    
    print("\n=== 读者-写者模式示例 ===")
    
    # 创建写者进程
    writer_process = multiprocessing.Process(target=writer, name="Writer")
    
    # 创建读者进程
    readers = []
    for i in range(3):
        reader_process = multiprocessing.Process(target=reader, args=(i,), name=f"Reader-{i}")
        readers.append(reader_process)
    
    # 启动进程
    writer_process.start()
    for reader_process in readers:
        reader_process.start()
    
    # 等待所有进程结束
    writer_process.join()
    for reader_process in readers:
        reader_process.join()
    
    print("读者-写者模式演示完成")
