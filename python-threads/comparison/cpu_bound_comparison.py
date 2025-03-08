"""
CPU-bound task comparison between different concurrency approaches.

This module compares the performance of different concurrency approaches for CPU-bound tasks.
"""

import threading
import multiprocessing
import asyncio
import time
import random
import concurrent.futures
from typing import List, Dict, Any, Tuple, Callable
import sys
import os
import math

# Add the parent directory to the path so we can import the utilities module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utilities.timing import benchmark
from utilities.visualization import plot_execution_times, plot_speedup


# Number of calculations to perform
NUM_CALCULATIONS = 10

# Size of each calculation (higher = more CPU intensive)
CALCULATION_SIZE = 10000000


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Args:
        n: Number to check.
        
    Returns:
        True if the number is prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True


def find_primes_in_range(start: int, end: int) -> List[int]:
    """
    Find all prime numbers in a range.
    
    Args:
        start: Start of the range.
        end: End of the range.
        
    Returns:
        List of prime numbers in the range.
    """
    return [n for n in range(start, end) if is_prime(n)]


def cpu_intensive_task(task_id: int) -> Tuple[int, int]:
    """
    Perform a CPU-intensive task.
    
    Args:
        task_id: Task identifier.
        
    Returns:
        Tuple containing (task_id, number of primes found).
    """
    # Generate a range based on the task ID
    start = task_id * CALCULATION_SIZE
    end = start + CALCULATION_SIZE
    
    # Find primes in the range
    primes = find_primes_in_range(start, end)
    
    return (task_id, len(primes))


def sequential_calculation() -> List[Tuple[int, int]]:
    """
    Perform calculations sequentially.
    
    Returns:
        List of results.
    """
    print("Performing sequential calculations...")
    results = []
    
    for i in range(NUM_CALCULATIONS):
        result = cpu_intensive_task(i)
        results.append(result)
    
    return results


def threaded_calculation() -> List[Tuple[int, int]]:
    """
    Perform calculations using threads.
    
    Returns:
        List of results.
    """
    print("Performing threaded calculations...")
    results = []
    threads = []
    
    # Thread-safe list for storing results
    results_lock = threading.Lock()
    
    def worker(task_id: int) -> None:
        """Perform a task and store the result."""
        result = cpu_intensive_task(task_id)
        with results_lock:
            results.append(result)
    
    # Create and start threads
    for i in range(NUM_CALCULATIONS):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return results


def process_pool_calculation() -> List[Tuple[int, int]]:
    """
    Perform calculations using a process pool.
    
    Returns:
        List of results.
    """
    print("Performing process pool calculations...")
    
    # Use a process pool to perform calculations
    with multiprocessing.Pool() as pool:
        results = pool.map(cpu_intensive_task, range(NUM_CALCULATIONS))
    
    return results


def thread_pool_executor_calculation() -> List[Tuple[int, int]]:
    """
    Perform calculations using ThreadPoolExecutor.
    
    Returns:
        List of results.
    """
    print("Performing ThreadPoolExecutor calculations...")
    
    # Use ThreadPoolExecutor to perform calculations
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_CALCULATIONS) as executor:
        results = list(executor.map(cpu_intensive_task, range(NUM_CALCULATIONS)))
    
    return results


def process_pool_executor_calculation() -> List[Tuple[int, int]]:
    """
    Perform calculations using ProcessPoolExecutor.
    
    Returns:
        List of results.
    """
    print("Performing ProcessPoolExecutor calculations...")
    
    # Use ProcessPoolExecutor to perform calculations
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_intensive_task, range(NUM_CALCULATIONS)))
    
    return results


async def asyncio_worker(task_id: int) -> Tuple[int, int]:
    """
    Perform a CPU-intensive task asynchronously.
    
    Args:
        task_id: Task identifier.
        
    Returns:
        Result of the task.
    """
    # For CPU-bound tasks, we need to run the task in a thread or process pool
    # to avoid blocking the event loop
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, cpu_intensive_task, task_id)


async def asyncio_calculation_impl() -> List[Tuple[int, int]]:
    """
    Implementation of asyncio calculations.
    
    Returns:
        List of results.
    """
    tasks = [asyncio_worker(i) for i in range(NUM_CALCULATIONS)]
    return await asyncio.gather(*tasks)


def asyncio_calculation() -> List[Tuple[int, int]]:
    """
    Perform calculations using asyncio.
    
    Returns:
        List of results.
    """
    print("Performing asyncio calculations...")
    return asyncio.run(asyncio_calculation_impl())


async def asyncio_process_pool_worker(task_id: int) -> Tuple[int, int]:
    """
    Perform a CPU-intensive task asynchronously using a process pool.
    
    Args:
        task_id: Task identifier.
        
    Returns:
        Result of the task.
    """
    # Create a process pool executor
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        return await loop.run_in_executor(executor, cpu_intensive_task, task_id)


async def asyncio_process_pool_calculation_impl() -> List[Tuple[int, int]]:
    """
    Implementation of asyncio calculations with a process pool.
    
    Returns:
        List of results.
    """
    # Create a process pool executor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        tasks = [loop.run_in_executor(executor, cpu_intensive_task, i) for i in range(NUM_CALCULATIONS)]
        return await asyncio.gather(*tasks)


def asyncio_process_pool_calculation() -> List[Tuple[int, int]]:
    """
    Perform calculations using asyncio with a process pool.
    
    Returns:
        List of results.
    """
    print("Performing asyncio calculations with process pool...")
    return asyncio.run(asyncio_process_pool_calculation_impl())


def run_comparison() -> None:
    """Run the CPU-bound task comparison."""
    print("=== CPU-Bound Task Comparison ===")
    print(f"Performing {NUM_CALCULATIONS} CPU-intensive calculations")
    print(f"Each calculation searches for primes in a range of {CALCULATION_SIZE} numbers")
    
    # Define the approaches to compare
    approaches = {
        "Sequential": sequential_calculation,
        "Threaded": threaded_calculation,
        "ProcessPool": process_pool_calculation,
        "ThreadPoolExecutor": thread_pool_executor_calculation,
        "ProcessPoolExecutor": process_pool_executor_calculation,
        "Asyncio": asyncio_calculation,
        "AsyncioProcessPool": asyncio_process_pool_calculation
    }
    
    # Benchmark each approach
    results = {}
    for name, func in approaches.items():
        print(f"\nBenchmarking {name} approach...")
        benchmark_result = benchmark(func, iterations=3)
        results[name] = benchmark_result
        
        print(f"  Min time: {benchmark_result['min']:.2f}s")
        print(f"  Max time: {benchmark_result['max']:.2f}s")
        print(f"  Mean time: {benchmark_result['mean']:.2f}s")
        print(f"  Median time: {benchmark_result['median']:.2f}s")
    
    # Print summary
    print("\n=== Summary ===")
    print("Mean execution times:")
    for name, result in results.items():
        print(f"{name}: {result['mean']:.2f}s")
    
    # Calculate speedups relative to sequential
    baseline = "Sequential"
    baseline_time = results[baseline]["mean"]
    
    speedups = {}
    for name, result in results.items():
        if name != baseline:
            speedup = baseline_time / result["mean"]
            speedups[name] = speedup
            print(f"{name} speedup: {speedup:.2f}x")
    
    # Plot results
    try:
        # Prepare data for plotting
        execution_times = {name: [result["mean"]] for name, result in results.items()}
        
        # Plot execution times
        plot_execution_times(
            execution_times,
            title=f"CPU-Bound Task Comparison ({NUM_CALCULATIONS} Calculations)",
            ylabel="Mean Execution Time (seconds)"
        )
        
        # Plot speedups
        plot_speedup(
            baseline,
            {name: results[name]["mean"] for name in results}
        )
    except Exception as e:
        print(f"Error plotting results: {e}")
        print("Note: Plotting requires matplotlib to be installed.")


if __name__ == "__main__":
    run_comparison() 