import time
from typing import Callable, Any

def runtime(func: Callable[..., Any], *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start

    class_name = type(func.__self__).__name__
    print(f"{class_name}.{func.__name__}: {elapsed:.6f}s")
    
    return result, elapsed