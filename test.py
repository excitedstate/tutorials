import time
from concurrent.futures import (
    InterpreterPoolExecutor,
    ThreadPoolExecutor,
    ProcessPoolExecutor,
)


def worker() -> int:
    a = 1
    for _ in range(10000000):
        a *= 1
    return a


if __name__ == "__main__":
    for executor_class, label in [
        (ThreadPoolExecutor, "多线程"),
        (ProcessPoolExecutor, "多进程"),
        (InterpreterPoolExecutor, "多解释器"),
    ]:
        for workers in [2, 4, 6, 8, 10]:
            s = time.time()
            with executor_class(max_workers=workers) as executor:
                futures = [executor.submit(worker) for _ in range(50)]
                results = [future.result() for future in futures]
            print(f"{label}耗时: {time.time() - s} 秒")
