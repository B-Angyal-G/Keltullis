import time
from collections.abc import Callable
from typing import Any, TypeVar

Arg = TypeVar("Arg")


def runtime(func: Callable[..., Arg], *args: Any, **kwargs: Any) -> tuple[Arg, float]:
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start

    # Ha kötött metódus, kiolvassuk az osztály nevét, egyébként üres marad:
    instance = getattr(func, "__self__", None)
    if instance is not None:
        prefix = f"{type(instance).__name__}."
    else:
        prefix = ""

    func_name = getattr(func, "__name__", str(func))
    print(f"{prefix}{func_name}: {elapsed:.6f}s")

    return result, elapsed
