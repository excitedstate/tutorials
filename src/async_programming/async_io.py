"""异步IO操作示例"""

import asyncio
import aiofiles
import aiohttp
from typing import List, Dict, Any


async def async_file_operations():
    """异步文件操作示例"""
    
    async def write_file():
        """异步写入文件"""
        async with aiofiles.open('async_file.txt', 'w') as f:
            await f.write('Hello, async world!\n')
            await f.write('This is line 2\n')
            await f.write('This is line 3\n')
        print("文件写入完成")
    
    async def read_file():
        """异步读取文件"""
        async with aiofiles.open('async_file.txt', 'r') as f:
            content = await f.read()
        print("文件内容:")
        print(content)
        return content
    
    async def append_file():
        """异步追加文件"""
        async with aiofiles.open('async_file.txt', 'a') as f:
            await f.write('This is appended line\n')
        print("文件追加完成")
    
    print("=== 异步文件操作示例 ===")
    
    # 执行异步文件操作
    await write_file()
    await read_file()
    await append_file()
    await read_file()


async def async_http_requests():
    """异步HTTP请求示例"""
    
    async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """异步获取URL内容"""
        async with session.get(url) as response:
            return {
                'url': url,
                'status': response.status,
                'content_length': response.content_length,
                'encoding': response.charset,
                'text': await response.text()[:100]  # 只获取前100个字符
            }
    
    print("\n=== 异步HTTP请求示例 ===")
    
    # 要请求的URL列表
    urls = [
        'https://httpbin.org/get',
        'https://httpbin.org/delay/1',  # 延迟1秒的请求
        'https://httpbin.org/status/200',
        'https://httpbin.org/headers'
    ]
    
    # 创建aiohttp会话并执行多个异步请求
    async with aiohttp.ClientSession() as session:
        # 使用asyncio.gather并发执行多个请求
        results = await asyncio.gather(
            *[fetch_url(session, url) for url in urls]
        )
        
        # 打印结果
        for result in results:
            print(f"\nURL: {result['url']}")
            print(f"状态码: {result['status']}")
            print(f"内容长度: {result['content_length']}")
            print(f"编码: {result['encoding']}")
            print(f"内容前100字符: {result['text']}")


async def async_tcp_client():
    """异步TCP客户端示例"""
    
    print("\n=== 异步TCP客户端示例 ===")
    
    try:
        # 连接到echo服务器
        reader, writer = await asyncio.open_connection('echo.websocket.org', 80)
        
        # 发送数据
        message = 'Hello, TCP echo server!\r\n'
        print(f"发送: {message.strip()}")
        writer.write(message.encode())
        await writer.drain()
        
        # 接收响应
        data = await reader.read(100)
        print(f"接收: {data.decode().strip()}")
        
        # 关闭连接
        print("关闭连接")
        writer.close()
        await writer.wait_closed()
        
    except ConnectionRefusedError:
        print("连接被拒绝，可能是服务器不可用")
    except Exception as e:
        print(f"发生错误: {e}")


async def async_tcp_server():
    """异步TCP服务器示例"""
    
    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """处理客户端连接"""
        addr = writer.get_extra_info('peername')
        print(f"客户端 {addr} 连接")
        
        try:
            while True:
                # 读取客户端数据
                data = await reader.read(100)
                if not data:
                    break
                
                message = data.decode().strip()
                print(f"从 {addr} 接收: {message}")
                
                # 发送响应
                response = f"服务器收到: {message}\r\n"
                writer.write(response.encode())
                await writer.drain()
                
                # 如果客户端发送'quit'，关闭连接
                if message.lower() == 'quit':
                    break
                    
        finally:
            print(f"客户端 {addr} 断开连接")
            writer.close()
            await writer.wait_closed()
    
    print("\n=== 异步TCP服务器示例 ===")
    print("注意: 这个示例会启动一个服务器，监听在127.0.0.1:8888")
    print("你可以使用telnet或其他TCP客户端连接测试")
    print("输入'quit'可以关闭连接")
    print("按Ctrl+C停止服务器")
    
    # 创建并启动服务器
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888
    )
    
    addr = server.sockets[0].getsockname()
    print(f"服务器启动，监听在 {addr}")
    
    # 运行服务器5秒后自动关闭
    try:
        async with server:
            await asyncio.wait_for(server.serve_forever(), timeout=5.0)
    except asyncio.TimeoutError:
        print("服务器运行5秒后自动关闭")


async def async_dns_resolution():
    """异步DNS解析示例"""
    
    print("\n=== 异步DNS解析示例 ===")
    
    # 要解析的域名列表
    domains = [
        'www.google.com',
        'www.baidu.com',
        'www.github.com',
        'www.python.org'
    ]
    
    # 使用asyncio的getaddrinfo进行异步DNS解析
    for domain in domains:
        try:
            print(f"解析域名: {domain}")
            result = await asyncio.getaddrinfo(domain, 80)
            print(f"解析结果: {result[0][4][0]}")  # 只打印第一个IP地址
        except Exception as e:
            print(f"解析失败: {e}")


async def async_stream_copy():
    """异步流复制示例"""
    
    async def copy_file(source: str, destination: str):
        """异步复制文件"""
        async with aiofiles.open(source, 'rb') as src:
            async with aiofiles.open(destination, 'wb') as dst:
                # 分块复制文件
                while True:
                    chunk = await src.read(1024)  # 1KB块
                    if not chunk:
                        break
                    await dst.write(chunk)
        print(f"文件复制完成: {source} -> {destination}")
    
    print("\n=== 异步流复制示例 ===")
    
    # 首先创建一个测试文件
    test_file = 'test_source.txt'
    async with aiofiles.open(test_file, 'w') as f:
        for i in range(1000):
            await f.write(f'This is line {i + 1}\n')
    
    print(f"创建测试文件: {test_file}")
    
    # 异步复制文件
    await copy_file(test_file, 'test_destination.txt')
    
    # 验证复制结果
    async with aiofiles.open(test_file, 'r') as src:
        src_content = await src.read()
    
    async with aiofiles.open('test_destination.txt', 'r') as dst:
        dst_content = await dst.read()
    
    print(f"文件复制验证: {'成功' if src_content == dst_content else '失败'}")
