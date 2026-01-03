"""多进程编程示例包"""

from .basic_processes import (
    basic_process_demo,
    process_with_args,
    process_with_return_value,
    process_daemon_demo,
    process_exit_codes,
    process_termination
)

from .process_sync import (
    process_lock_demo,
    process_semaphore_demo,
    process_event_demo,
    process_condition_demo,
    process_barrier_demo,
    process_race_condition_demo
)

from .process_pools import (
    process_pool_demo,
    process_pool_map_demo,
    process_pool_starmap_demo,
    process_pool_async_demo,
    process_pool_exception_demo,
    process_pool_performance_demo
)

from .process_patterns import (
    producer_consumer_with_queue,
    pipe_communication_demo,
    shared_memory_demo,
    manager_demo,
    reader_writer_pattern
)

__all__ = [
    # 基础进程操作
    "basic_process_demo",
    "process_with_args",
    "process_with_return_value",
    "process_daemon_demo",
    "process_exit_codes",
    "process_termination",
    
    # 进程同步机制
    "process_lock_demo",
    "process_semaphore_demo",
    "process_event_demo",
    "process_condition_demo",
    "process_barrier_demo",
    "process_race_condition_demo",
    
    # 进程池
    "process_pool_demo",
    "process_pool_map_demo",
    "process_pool_starmap_demo",
    "process_pool_async_demo",
    "process_pool_exception_demo",
    "process_pool_performance_demo",
    
    # 经典多进程模式
    "producer_consumer_with_queue",
    "pipe_communication_demo",
    "shared_memory_demo",
    "manager_demo",
    "reader_writer_pattern",
    
    # 多进程与不同类型任务
    # "multiprocess_io_tasks",
    # "multiprocess_cpu_tasks"
]