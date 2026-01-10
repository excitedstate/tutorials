from ast import Call
import time
from tkinter import N, NO
from typing import ParamSpec, TypeVar, Callable, Any


_P = ParamSpec("_P")
_T_co = TypeVar("_T_co", covariant=True)
_D = TypeVar("_D")


def should(func: Callable[_P, _T_co], default: _D) -> Callable[_P, _T_co | _D]:
    """一个用于提供默认返回值的装饰器

    参数:
        func (Callable[_P, _T_co]): 需要装饰的函数。
        default (D): 当函数执行失败时返回的默认值。
    返回:
        Callable[_P, _T_co | D]: 装饰后的函数。
    """

    def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T_co | _D:
        try:
            return func(*args, **kwargs)
        except Exception:
            return default

    return wrapper


def timeit(
    repeat: int = 1,
    data_handler: Callable[[_T_co, int], None] | None = None,
    report_handler: Callable[[int, float], None] | None = None,
) -> Callable[[Callable[_P, _T_co]], Callable[_P, _T_co]]:
    """一个用于测量函数执行时间的装饰器

    参数:
        repeat (int): 执行函数的次数，默认为1。
        data_handler (Callable[[_T_co, int], None] | None): 可选的数据处理函数，
            接受函数返回值和执行时间作为参数。
    返回:
        Callable[_P, _T_co]: 装饰后的函数。
    """
    data_handler = data_handler or (lambda result, index: None)
    report_handler = report_handler or (
        lambda repeat, total_time: print(
            f"repeat {repeat}, total_time: {total_time:.6f}s, average_time: {total_time / repeat:.6f}s"
        )
    )

    def decorator(func: Callable[_P, _T_co]) -> Callable[_P, _T_co]:

        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T_co:
            total_time = 0.0
            result: _T_co | None = None

            for i in range(repeat):
                start_time = time.time()
                # # execute the function
                data_handler(func(*args, **kwargs), i)
                # # end timing
                end_time = time.time()
                total_time += end_time - start_time

            report_handler(repeat, total_time)

            return result  # type: ignore

        return wrapper

    return decorator
