#!/usr/bin/env python3
"""IO密集型性能测试主程序

合并了文件IO和网络IO性能测试，支持命令行选项控制测试类型
"""

import os
import time
import threading
import asyncio
import subprocess
import sys
import signal
import argparse
from concurrent.futures import ThreadPoolExecutor

# 尝试导入所需库
try:
    from fastapi import FastAPI
except ImportError:
    print("安装fastapi库...")
    subprocess.run([sys.executable, "-m", "pip", "install", "fastapi"], check=True)
    from fastapi import FastAPI

try:
    import uvicorn
except ImportError:
    print("安装uvicorn库...")
    subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn"], check=True)
    import uvicorn

try:
    import requests
except ImportError:
    print("安装requests库...")
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
    import requests

try:
    import aiohttp
except ImportError:
    print("安装aiohttp库...")
    subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp"], check=True)
    import aiohttp

# FastAPI应用定义
app = FastAPI()

@app.get("/")
async def root():
    """根路径，返回Hello World"""
    return {"message": "Hello World"}

@app.get("/fast")
def fast_endpoint():
    """快速端点，同步返回"""
    return {"message": "Fast Response"}

@app.get("/delayed/{delay_ms}")
async def delayed_endpoint(delay_ms: int):
    """延迟端点，用于模拟不同延迟的IO操作
    
    Args:
        delay_ms: 延迟时间（毫秒）
    """
    await asyncio.sleep(delay_ms / 1000)
    return {"message": f"Delayed {delay_ms}ms", "delay": delay_ms}


class IODensityPerformanceTest:
    """IO密集型任务性能测试类"""
    
    def __init__(self, num_files=50, file_size_kb=100, num_reads=10):
        """初始化测试参数
        
        Args:
            num_files: 生成的测试文件数量
            file_size_kb: 每个测试文件的大小（KB）
            num_reads: 每个文件读取的次数
        """
        self.num_files = num_files
        self.file_size_kb = file_size_kb
        self.num_reads = num_reads
        self.test_dir = "io_test_files"
        self.test_files = []
        
    def setup(self):
        """设置测试环境，生成测试文件"""
        print("=== 设置测试环境 ===")
        
        # 创建测试目录
        os.makedirs(self.test_dir, exist_ok=True)
        
        # 生成测试内容
        test_content = b'X' * (self.file_size_kb * 1024)  # 生成指定大小的内容
        
        # 生成测试文件
        self.test_files = []
        for i in range(self.num_files):
            file_path = os.path.join(self.test_dir, f"test_file_{i}.bin")
            with open(file_path, 'wb') as f:
                f.write(test_content)
            self.test_files.append(file_path)
        
        print(f"生成了 {self.num_files} 个测试文件")
        print(f"每个文件大小: {self.file_size_kb} KB")
        print(f"总数据量: {self.num_files * self.file_size_kb / 1024:.2f} MB")
        print(f"每个文件读取次数: {self.num_reads}")
    
    def cleanup(self):
        """清理测试环境"""
        print("\n=== 清理测试环境 ===")
        
        # 删除测试文件
        for file_path in self.test_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # 删除测试目录
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
        
        print("测试文件已清理")
    
    def sync_read(self):
        """同步方式读取文件"""
        print("\n=== 同步读取测试 ===")
        
        start_time = time.time()
        total_bytes = 0
        
        for _ in range(self.num_reads):
            for file_path in self.test_files:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    total_bytes += len(content)
        
        end_time = time.time()
        elapsed = end_time - start_time
        throughput = total_bytes / (1024 * 1024) / elapsed  # MB/s
        
        print(f"同步读取完成")
        print(f"总读取字节数: {total_bytes / (1024 * 1024):.2f} MB")
        print(f"耗时: {elapsed:.2f}秒")
        print(f"吞吐量: {throughput:.2f} MB/s")
        
        return elapsed, throughput
    
    def multithread_read(self, num_threads=4):
        """多线程方式读取文件"""
        print(f"\n=== 多线程读取测试 (线程数: {num_threads}) ===")
        
        def read_file(file_path):
            """线程任务：读取单个文件"""
            thread_total = 0
            for _ in range(self.num_reads):
                with open(file_path, 'rb') as f:
                    content = f.read()
                    thread_total += len(content)
            return thread_total
        
        start_time = time.time()
        total_bytes = 0
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = list(executor.map(read_file, self.test_files))
            total_bytes = sum(results)
        
        end_time = time.time()
        elapsed = end_time - start_time
        throughput = total_bytes / (1024 * 1024) / elapsed  # MB/s
        
        print(f"多线程读取完成")
        print(f"总读取字节数: {total_bytes / (1024 * 1024):.2f} MB")
        print(f"耗时: {elapsed:.2f}秒")
        print(f"吞吐量: {throughput:.2f} MB/s")
        
        return elapsed, throughput
    
    async def async_read_file(self, file_path):
        """异步任务：读取单个文件"""
        async_total = 0
        for _ in range(self.num_reads):
            # 使用标准asyncio文件I/O
            with open(file_path, 'rb') as f:
                content = await asyncio.to_thread(f.read)
                async_total += len(content)
        return async_total
    
    async def async_read(self):
        """异步方式读取文件"""
        print("\n=== 异步读取测试 ===")
        
        start_time = time.time()
        
        tasks = [self.async_read_file(file_path) for file_path in self.test_files]
        results = await asyncio.gather(*tasks)
        total_bytes = sum(results)
        
        end_time = time.time()
        elapsed = end_time - start_time
        throughput = total_bytes / (1024 * 1024) / elapsed  # MB/s
        
        print(f"异步读取完成")
        print(f"总读取字节数: {total_bytes / (1024 * 1024):.2f} MB")
        print(f"耗时: {elapsed:.2f}秒")
        print(f"吞吐量: {throughput:.2f} MB/s")
        
        return elapsed, throughput
    
    def run_all_tests(self):
        """运行所有文件IO测试"""
        print("文件IO密集型任务性能测试")
        print("=" * 60)
        
        try:
            # 设置测试环境
            self.setup()
            
            # 运行同步测试
            sync_time, sync_throughput = self.sync_read()
            
            # 运行多线程测试（不同线程数）
            thread_results = []
            for num_threads in [2, 4, 8, 16]:
                thread_time, thread_throughput = self.multithread_read(num_threads)
                thread_results.append((num_threads, thread_time, thread_throughput))
            
            # 运行异步测试
            async_time, async_throughput = asyncio.run(self.async_read())
            
            # 性能对比
            self.print_comparison(sync_time, sync_throughput, thread_results, async_time, async_throughput)
            
        finally:
            # 清理测试环境
            self.cleanup()
    
    def print_comparison(self, sync_time, sync_throughput, thread_results, async_time, async_throughput):
        """打印性能对比结果"""
        print("\n" + "=" * 60)
        print("性能对比总结")
        print("=" * 60)
        
        print(f"\n同步方式:")
        print(f"  耗时: {sync_time:.2f}秒")
        print(f"  吞吐量: {sync_throughput:.2f} MB/s")
        print(f"  相对速度: 1.0x")
        
        for num_threads, thread_time, thread_throughput in thread_results:
            speedup = sync_time / thread_time
            print(f"\n多线程 ({num_threads}线程):")
            print(f"  耗时: {thread_time:.2f}秒")
            print(f"  吞吐量: {thread_throughput:.2f} MB/s")
            print(f"  相对速度: {speedup:.2f}x")
        
        speedup = sync_time / async_time
        print(f"\n异步方式:")
        print(f"  耗时: {async_time:.2f}秒")
        print(f"  吞吐量: {async_throughput:.2f} MB/s")
        print(f"  相对速度: {speedup:.2f}x")
        
        # 找出最快的方式
        all_results = [
            ("同步", sync_time, sync_throughput)
        ] + [
            (f"多线程({num_threads})", thread_time, thread_throughput) 
            for num_threads, thread_time, thread_throughput in thread_results
        ] + [
            ("异步", async_time, async_throughput)
        ]
        
        # 按耗时排序
        all_results.sort(key=lambda x: x[1])
        
        print(f"\n" + "=" * 60)
        print("最快方式排行:")
        for i, (name, time_taken, throughput) in enumerate(all_results, 1):
            speedup = sync_time / time_taken
            print(f"{i}. {name}: 耗时 {time_taken:.2f}秒, 吞吐量 {throughput:.2f} MB/s, 速度提升 {speedup:.2f}x")
        
        print(f"\n" + "=" * 60)
        print("结论:")
        print("1. IO密集型任务中，多线程和异步方式通常比同步方式快")
        print("2. 异步方式在高并发IO场景下表现最佳")
        print("3. 多线程的最佳线程数取决于系统和IO设备性能")
        print("4. 对于文件IO，异步IO的优势可能不如网络IO明显")


class NetworkIODensityTest:
    """网络IO密集型任务性能测试类"""
    
    def __init__(self, num_requests=1000, concurrent_levels=None):
        """初始化测试参数
        
        Args:
            num_requests: 总请求数
            concurrent_levels: 并发级别列表
        """
        self.num_requests = num_requests
        self.concurrent_levels = concurrent_levels or [1, 2, 4, 8, 16, 32]
        self.server_url = "http://localhost:8000/fast"
        self.server_process = None
        
    def start_server(self):
        """启动FastAPI服务器"""
        print("=== 启动FastAPI服务器 ===")
        
        # 启动uvicorn服务器
        self.server_process = subprocess.Popen(
            [sys.executable, "-c", "from main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='error')"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务器启动
        time.sleep(2)
        
        # 检查服务器是否启动成功
        try:
            response = requests.get(self.server_url, timeout=5)
            if response.status_code == 200:
                print("FastAPI服务器启动成功")
                return True
            else:
                print(f"服务器启动失败，状态码: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"无法连接到服务器: {e}")
            return False
    
    def stop_server(self):
        """停止FastAPI服务器"""
        print("\n=== 停止FastAPI服务器 ===")
        
        if self.server_process:
            # 发送SIGTERM信号
            self.server_process.send_signal(signal.SIGTERM)
            
            # 等待进程结束
            try:
                self.server_process.wait(timeout=5)
                print("FastAPI服务器已停止")
            except subprocess.TimeoutExpired:
                # 如果超时，强制终止
                print("服务器停止超时，强制终止")
                self.server_process.terminate()
                self.server_process.wait(timeout=2)
            
            self.server_process = None
    
    def sync_requests(self):
        """同步方式发送HTTP请求"""
        print("\n=== 同步请求测试 ===")
        
        start_time = time.time()
        successful = 0
        
        for _ in range(self.num_requests):
            try:
                response = requests.get(self.server_url)
                if response.status_code == 200:
                    successful += 1
            except Exception as e:
                print(f"请求失败: {e}")
        
        end_time = time.time()
        elapsed = end_time - start_time
        requests_per_second = self.num_requests / elapsed
        
        print(f"同步请求完成")
        print(f"总请求数: {self.num_requests}")
        print(f"成功请求: {successful}")
        print(f"耗时: {elapsed:.2f}秒")
        print(f"吞吐量: {requests_per_second:.2f} 请求/秒")
        
        return elapsed, requests_per_second, successful
    
    def multithread_requests(self, concurrent):
        """多线程方式发送HTTP请求"""
        print(f"\n=== 多线程请求测试 (并发数: {concurrent}) ===")
        
        def send_request():
            """线程任务：发送单个HTTP请求"""
            try:
                response = requests.get(self.server_url)
                return response.status_code == 200
            except Exception:
                return False
        
        start_time = time.time()
        successful = 0
        
        with ThreadPoolExecutor(max_workers=concurrent) as executor:
            # 计算每个线程需要发送的请求数
            requests_per_thread = self.num_requests // concurrent
            remaining = self.num_requests % concurrent
            
            # 创建任务列表
            tasks = []
            for i in range(concurrent):
                # 分配请求数，最后一个线程处理剩余请求
                count = requests_per_thread + (1 if i < remaining else 0)
                for _ in range(count):
                    tasks.append(executor.submit(send_request))
            
            # 收集结果
            for future in tasks:
                if future.result():
                    successful += 1
        
        end_time = time.time()
        elapsed = end_time - start_time
        requests_per_second = self.num_requests / elapsed
        
        print(f"多线程请求完成")
        print(f"总请求数: {self.num_requests}")
        print(f"成功请求: {successful}")
        print(f"耗时: {elapsed:.2f}秒")
        print(f"吞吐量: {requests_per_second:.2f} 请求/秒")
        
        return elapsed, requests_per_second, successful
    
    async def async_requests(self, concurrent=100):
        """异步方式发送HTTP请求"""
        print(f"\n=== 异步请求测试 ===")
        
        async def send_request(session):
            """异步任务：发送单个HTTP请求"""
            try:
                async with session.get(self.server_url) as response:
                    return response.status == 200
            except Exception:
                return False
        
        async def main():
            """异步主函数"""
            successful = 0
            
            async with aiohttp.ClientSession() as session:
                # 分批发送请求，避免同时创建太多任务
                batch_size = min(concurrent, self.num_requests)
                batches = (self.num_requests + batch_size - 1) // batch_size
                
                for batch in range(batches):
                    start_idx = batch * batch_size
                    end_idx = min((batch + 1) * batch_size, self.num_requests)
                    current_batch_size = end_idx - start_idx
                    
                    # 创建当前批次的任务
                    tasks = [send_request(session) for _ in range(current_batch_size)]
                    results = await asyncio.gather(*tasks)
                    successful += sum(results)
            
            return successful
        
        start_time = time.time()
        successful = await main()
        end_time = time.time()
        
        elapsed = end_time - start_time
        requests_per_second = self.num_requests / elapsed
        
        print(f"异步请求完成")
        print(f"总请求数: {self.num_requests}")
        print(f"成功请求: {successful}")
        print(f"耗时: {elapsed:.2f}秒")
        print(f"吞吐量: {requests_per_second:.2f} 请求/秒")
        
        return elapsed, requests_per_second, successful
    
    def run_all_tests(self):
        """运行所有网络IO测试"""
        print("网络IO密集型任务性能测试")
        print("=" * 60)
        print(f"测试配置: {self.num_requests}个请求")
        print("=" * 60)
        
        try:
            # 启动服务器
            if not self.start_server():
                print("无法启动服务器，测试终止")
                return
            
            # 运行同步测试
            sync_time, sync_rps, sync_success = self.sync_requests()
            
            # 运行多线程测试
            thread_results = []
            for concurrent in self.concurrent_levels:
                thread_time, thread_rps, thread_success = self.multithread_requests(concurrent)
                thread_results.append((concurrent, thread_time, thread_rps, thread_success))
            
            # 运行异步测试
            async_time, async_rps, async_success = asyncio.run(self.async_requests())
            
            # 打印性能对比
            self.print_comparison(sync_time, sync_rps, sync_success, thread_results, async_time, async_rps, async_success)
            
        finally:
            # 停止服务器
            self.stop_server()
    
    def print_comparison(self, sync_time, sync_rps, sync_success, thread_results, async_time, async_rps, async_success):
        """打印性能对比结果"""
        print("\n" + "=" * 60)
        print("性能对比总结")
        print("=" * 60)
        
        print(f"\n同步方式:")
        print(f"  耗时: {sync_time:.2f}秒")
        print(f"  吞吐量: {sync_rps:.2f} 请求/秒")
        print(f"  成功请求: {sync_success}/{self.num_requests}")
        print(f"  成功率: {sync_success / self.num_requests * 100:.1f}%")
        print(f"  相对速度: 1.0x")
        
        for concurrent, thread_time, thread_rps, thread_success in thread_results:
            speedup = sync_rps / thread_rps if thread_rps > 0 else 0
            print(f"\n多线程 ({concurrent}并发):")
            print(f"  耗时: {thread_time:.2f}秒")
            print(f"  吞吐量: {thread_rps:.2f} 请求/秒")
            print(f"  成功请求: {thread_success}/{self.num_requests}")
            print(f"  成功率: {thread_success / self.num_requests * 100:.1f}%")
            print(f"  相对速度: {speedup:.2f}x")
        
        speedup = sync_rps / async_rps if async_rps > 0 else 0
        print(f"\n异步方式:")
        print(f"  耗时: {async_time:.2f}秒")
        print(f"  吞吐量: {async_rps:.2f} 请求/秒")
        print(f"  成功请求: {async_success}/{self.num_requests}")
        print(f"  成功率: {async_success / self.num_requests * 100:.1f}%")
        print(f"  相对速度: {speedup:.2f}x")
        
        # 找出最快的方式
        all_results = [
            ("同步", sync_time, sync_rps, sync_success)
        ] + [
            (f"多线程({concurrent})", thread_time, thread_rps, thread_success) 
            for concurrent, thread_time, thread_rps, thread_success in thread_results
        ] + [
            ("异步", async_time, async_rps, async_success)
        ]
        
        # 按吞吐量排序
        all_results.sort(key=lambda x: x[2], reverse=True)
        
        print(f"\n" + "=" * 60)
        print("吞吐量排行")
        print("=" * 60)
        for i, (name, time_taken, rps, success) in enumerate(all_results, 1):
            speedup = rps / sync_rps if sync_rps > 0 else 0
            print(f"{i}. {name}: {rps:.2f} 请求/秒, 耗时 {time_taken:.2f}秒, 成功率 {success / self.num_requests * 100:.1f}%, 相对吞吐量 {speedup:.2f}x")
        
        print(f"\n" + "=" * 60)
        print("结论:")
        print("1. 网络IO密集型任务中，多线程和异步方式通常比同步方式快很多")
        print("2. 异步方式在高并发网络IO场景下表现最佳")
        print("3. 多线程的最佳并发数取决于系统和网络环境")
        print("4. 异步IO在处理大量并发连接时优势明显")
        print("5. 对于网络IO，异步方式通常优于多线程方式")


def main():
    """主函数，解析命令行参数并运行相应测试"""
    parser = argparse.ArgumentParser(description="IO密集型性能测试")
    parser.add_argument("--network", action="store_true", help="运行网络IO测试")
    parser.add_argument("--file", action="store_true", help="运行文件IO测试")
    parser.add_argument("--num-requests", type=int, default=1000, help="网络测试请求数")
    parser.add_argument("--num-files", type=int, default=50, help="文件测试文件数")
    parser.add_argument("--file-size", type=int, default=100, help="文件测试每个文件大小(KB)")
    
    args = parser.parse_args()
    
    # 如果没有指定测试类型，运行文件IO测试
    if not args.network and not args.file:
        args.file = True
    
    if args.file:
        # 运行文件IO测试
        file_test = IODensityPerformanceTest(
            num_files=args.num_files,
            file_size_kb=args.file_size,
            num_reads=10
        )
        file_test.run_all_tests()
    
    if args.network:
        # 运行网络IO测试
        network_test = NetworkIODensityTest(
            num_requests=args.num_requests,
            concurrent_levels=[2, 4, 8, 16, 32]
        )
        network_test.run_all_tests()


if __name__ == "__main__":
    main()