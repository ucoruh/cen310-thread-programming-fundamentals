"""
Timing utilities for measuring execution time of functions.
"""

import time
import functools
from typing import Callable, TypeVar, Any, Dict, List, Tuple
import statistics

T = TypeVar('T')


def timeit(func: Callable[..., T]) -> Callable[..., Tuple[T, float]]:
    """
    Decorator to measure the execution time of a function.
    
    Args:
        func: The function to measure.
        
    Returns:
        A wrapped function that returns a tuple of (result, execution_time).
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Tuple[T, float]:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper


def benchmark(func: Callable[..., Any], iterations: int = 5, *args: Any, **kwargs: Any) -> Dict[str, float]:
    """
    Benchmark a function by running it multiple times and collecting statistics.
    
    Args:
        func: The function to benchmark.
        iterations: Number of times to run the function.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
        
    Returns:
        A dictionary containing benchmark statistics (min, max, mean, median).
    """
    times: List[float] = []
    
    for _ in range(iterations):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        times.append(end_time - start_time)
    
    return {
        'min': min(times),
        'max': max(times),
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'iterations': iterations
    }


class Timer:
    """Context manager for timing code blocks."""
    
    def __init__(self, name: str = "Timer"):
        """
        Initialize the timer.
        
        Args:
            name: A name for this timer (used in the output).
        """
        self.name = name
        self.start_time = 0.0
        self.end_time = 0.0
    
    def __enter__(self) -> 'Timer':
        """Start the timer when entering the context."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Stop the timer when exiting the context and print the elapsed time."""
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"{self.name} took {elapsed:.6f} seconds")
    
    @property
    def elapsed(self) -> float:
        """Get the elapsed time in seconds."""
        if self.end_time < self.start_time:
            return time.time() - self.start_time
        return self.end_time - self.start_time 