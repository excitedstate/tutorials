import threading
import time


def create_thread_with_subclass():
    class MyThread(threading.Thread):
        def __init__(self):
            super().__init__()
            self.result = None

        def run(self):
            print(f"Thread {threading.current_thread().name} running")
            time.sleep(1)
            self.result = 42  # 示例返回值

        def get_result(self):
            return self.result

    # 创建并启动线程
    t1 = MyThread()
    t1.start()
    t1.join()  # 等待线程结束


def create_thread_with_target():
    def worker():
        print(f"Thread {threading.current_thread().name} running")
        time.sleep(1)

    # 创建线程
    t2 = threading.Thread(target=worker, name="WorkerThread")
    t2.start()
    t2.join()  # 等待线程结束


def create_thread_pool():
    from concurrent.futures import ThreadPoolExecutor

    def task(n):
        print(f"Thread {threading.current_thread().name} processing {n}")
        time.sleep(1)
        return n * n

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(task, range(5)))
    print("Results:", results)


if __name__ == "__main__":
    print("Creating thread using subclassing:")
    create_thread_with_subclass()

    print("\nCreating thread using target function:")
    create_thread_with_target()

    print("\nCreating thread pool:")
    create_thread_pool()
