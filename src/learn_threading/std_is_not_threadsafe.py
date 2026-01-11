from random import randint
import time
import threading


# # 实践中, 我们不关心 g() 的实现细节, 只把他当成一个可迭代对象
def g():
    for i in range(10):
        time.sleep(randint(0, 5) * 0.01)
        yield i


def test():
    # # 并发
    shared_data = []

    def worker():
        shared_data.extend(g())

    threads = []
    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Data: {shared_data}, length: {len(shared_data)}")

    # # 串行
    shared_data = []
    for _ in range(5):
        worker()
    print(f"Data: {shared_data}, length: {len(shared_data)}")


test()
