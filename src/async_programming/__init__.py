"""异步编程示例包"""

from .basic_async import (
    basic_async_demo,
    async_with_return_value,
    async_await_demo,
    async_function_chaining,
    async_sleep_vs_time_sleep,
    asyncio_run_example
)

from .async_io import (
    async_file_operations,
    async_http_requests,
    async_tcp_client,
    async_tcp_server,
    async_dns_resolution,
    async_stream_copy
)

from .async_concurrency import (
    async_concurrency_with_gather,
    async_concurrency_with_wait,
    async_concurrency_with_as_completed,
    async_limits_with_semaphore,
    async_error_handling,
    async_task_group_demo,
    async_timeout_demo,
    async_cancellation_demo,
    async_performance_comparison
)

from .async_patterns import (
    async_producer_consumer,
    async_event_loop_demo,
    async_context_manager,
    async_iterators,
    async_state_machine,
    async_future_demo,
    async_cooperative_cancellation,
    async_main_entry
)

from .anyio_demo import (
    anyio_basic_demo,
    anyio_concurrency_demo,
    anyio_file_operations,
    anyio_sync_primitives,
    anyio_task_groups,
    anyio_asyncio_compatibility,
    anyio_stream_demo,
    anyio_main_demo
)

from .asyncio_sync_integration import (
    run_sync_in_async_context,
    run_async_in_sync_context,
    run_async_in_sync_with_executor,
    performance_comparison,
    advanced_integration_techniques,
    main as asyncio_sync_main
)

__all__ = [
    # 基础异步操作
    "basic_async_demo",
    "async_with_return_value",
    "async_await_demo",
    "async_function_chaining",
    "async_sleep_vs_time_sleep",
    "asyncio_run_example",
    
    # 异步IO操作
    "async_file_operations",
    "async_http_requests",
    "async_tcp_client",
    "async_tcp_server",
    "async_dns_resolution",
    "async_stream_copy",
    
    # 异步并发
    "async_concurrency_with_gather",
    "async_concurrency_with_wait",
    "async_concurrency_with_as_completed",
    "async_limits_with_semaphore",
    "async_error_handling",
    "async_task_group_demo",
    "async_timeout_demo",
    "async_cancellation_demo",
    "async_performance_comparison",
    
    # 异步设计模式
    "async_producer_consumer",
    "async_event_loop_demo",
    "async_context_manager",
    "async_iterators",
    "async_state_machine",
    "async_future_demo",
    "async_cooperative_cancellation",
    "async_main_entry",
    
    # AnyIO示例
    "anyio_basic_demo",
    "anyio_concurrency_demo",
    "anyio_file_operations",
    "anyio_sync_primitives",
    "anyio_task_groups",
    "anyio_asyncio_compatibility",
    "anyio_stream_demo",
    "anyio_main_demo",
    
    # asyncio与同步函数集成
    "run_sync_in_async_context",
    "run_async_in_sync_context",
    "run_async_in_sync_with_executor",
    "performance_comparison",
    "advanced_integration_techniques",
    "asyncio_sync_main"
]