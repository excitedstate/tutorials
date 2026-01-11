import threading
import time


def daemon_func():
    while True:
        print("Daemon thread running")
        time.sleep(1)


# 创建守护线程
daemon_thread = threading.Thread(target=daemon_func)
daemon_thread.daemon = True  # 设置为守护线程
daemon_thread.start()

# 主线程运行5秒后结束
time.sleep(5)
print("Main thread ending")
# 此时守护线程会自动终止
