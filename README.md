# Python并发编程教程

本项目包含Python并发编程的各种示例和性能测试，涵盖多线程、多进程、异步编程等技术。

## 目录结构

```
tutorials/
├── src/
│   ├── async_programming/    # 异步编程示例
│   ├── multi_process/        # 多进程编程示例
│   ├── multi_thread/         # 多线程编程示例
│   ├── cpu_intensive.py      # CPU密集型任务示例
│   └── io_intensive.py       # IO密集型任务示例
├── tests/                    # 测试用例
│   ├── async_programming/    # 异步编程测试
│   ├── benchmark/            # 性能基准测试
│   ├── multi_process/        # 多进程测试
│   └── multi_thread/         # 多线程测试
├── main.py                   # IO性能测试主程序
├── pyproject.toml            # 项目配置
├── README.md                 # 项目说明
└── LICENSE                   # 许可证
```

## 主要功能

### 1. 多线程编程 (multi_thread/)
- 基本线程创建和使用
- 线程同步机制（锁、条件变量、信号量等）
- 线程池使用
- 经典线程模式

### 2. 多进程编程 (multi_process/)
- 基本进程创建和使用
- 进程间通信
- 进程池
- 进程同步机制

### 3. 异步编程 (async_programming/)
- 基本异步语法
- 异步IO操作
- 异步并发控制
- 异步设计模式
- AnyIO库示例
- 异步与同步的集成

### 4. 性能测试 (main.py)
- 文件IO性能测试（同步、多线程、异步对比）
- 网络IO性能测试（同步、多线程、异步对比）
- 支持命令行参数配置

## 安装

### 依赖项
- Python 3.7+
- 主要依赖库：
  - fastapi
  - uvicorn
  - requests
  - aiohttp

### 安装方法

```bash
# 克隆仓库
git clone https://github.com/excitedstate/tutorials.git
cd tutorials

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 1. 运行IO性能测试

```bash
# 运行文件IO测试
python3 main.py --file

# 运行网络IO测试
python3 main.py --network

# 同时运行两种测试
python3 main.py --file --network

# 自定义测试参数
python3 main.py --network --num-requests 2000
python3 main.py --file --num-files 100 --file-size 200
```

### 2. 运行示例脚本

```bash
# 运行CPU密集型任务示例
python3 src/cpu_intensive.py

# 运行IO密集型任务示例
python3 src/io_intensive.py

# 运行多线程示例
python3 src/multi_thread/basic_threads.py

# 运行多进程示例
python3 src/multi_process/basic_processes.py

# 运行异步示例
python3 src/async_programming/basic_async.py
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定模块的测试
pytest tests/multi_thread/
pytest tests/async_programming/

# 运行基准测试
pytest tests/benchmark/
```

## 性能测试结果

### 文件IO测试
- **同步方式**: 4332.10 MB/s
- **多线程(16线程)**: 1420.58 MB/s
- **异步方式**: 1056.08 MB/s

### 网络IO测试 (1000个请求)
- **同步方式**: 555.97 请求/秒
- **多线程(16线程)**: 996.34 请求/秒
- **异步方式**: 2588.09 请求/秒

## 结论

1. **CPU密集型任务**: 多进程方式通常比多线程方式表现更好
2. **IO密集型任务**: 
   - 文件IO: 同步方式可能表现最佳
   - 网络IO: 异步方式通常表现最佳
3. **异步编程**: 在高并发场景下优势明显，适合处理大量网络连接
4. **多线程**: 适合IO密集型任务，但受GIL限制
5. **多进程**: 适合CPU密集型任务，可充分利用多核CPU

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request！

## 作者

excitedstate
