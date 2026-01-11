import threading
import time


def try_to_cancel_thread():
    def worker(stop_event):
        while not stop_event.is_set():
            print("线程工作中...")
            # 使用wait可以更及时响应停止信号
            stop_event.wait(timeout=1)
        print("线程收到停止信号，正在清理...")

    # 创建Event对象
    stop_event = threading.Event()

    # 启动线程
    thread = threading.Thread(target=worker, args=(stop_event,))
    thread.start()
    threading.Event
    # 运行一段时间后停止
    time.sleep(4)
    stop_event.set()  # 设置事件，通知线程停止
    thread.join()

