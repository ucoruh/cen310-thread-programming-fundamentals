"""
I/O-bound task comparison between different concurrency approaches.

This module compares the performance of different concurrency approaches for I/O-bound tasks.
"""

import threading
import multiprocessing
import asyncio
import time
import random
import requests
import aiohttp
import concurrent.futures
from typing import List, Dict, Any, Tuple, Callable
import sys
import os

# Add the parent directory to the path so we can import the utilities module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utilities.timing import benchmark
from utilities.visualization import plot_execution_times, plot_speedup


# URLs for testing (these are fast and reliable)
URLS = [
    "https://httpbin.org/get",
    "https://httpbin.org/ip",
    "https://httpbin.org/user-agent",
    "https://httpbin.org/headers",
    "https://httpbin.org/uuid"
]

# Number of requests to make
NUM_REQUESTS = 50


def sequential_requests() -> List[Dict[str, Any]]:
    """
    Make HTTP requests sequentially.
    
    Returns:
        List of response data.
    """
    print("Making sequential requests...")
    results = []
    
    # Generate URLs by repeating the list
    urls = [URLS[i % len(URLS)] for i in range(NUM_REQUESTS)]
    
    for url in urls:
        response = requests.get(url)
        results.append(response.json())
    
    return results


def threaded_requests() -> List[Dict[str, Any]]:
    """
    Make HTTP requests using threads.
    
    Returns:
        List of response data.
    """
    print("Making threaded requests...")
    results = []
    threads = []
    
    # Generate URLs by repeating the list
    urls = [URLS[i % len(URLS)] for i in range(NUM_REQUESTS)]
    
    # Thread-safe list for storing results
    results_lock = threading.Lock()
    
    def fetch_url(url: str) -> None:
        """Fetch a URL and store the result."""
        response = requests.get(url)
        with results_lock:
            results.append(response.json())
    
    # Create and start threads
    for url in urls:
        thread = threading.Thread(target=fetch_url, args=(url,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return results


def process_pool_requests() -> List[Dict[str, Any]]:
    """
    Make HTTP requests using a process pool.
    
    Returns:
        List of response data.
    """
    print("Making process pool requests...")
    
    # Generate URLs by repeating the list
    urls = [URLS[i % len(URLS)] for i in range(NUM_REQUESTS)]
    
    def fetch_url(url: str) -> Dict[str, Any]:
        """Fetch a URL and return the result."""
        response = requests.get(url)
        return response.json()
    
    # Use a process pool to fetch URLs
    with multiprocessing.Pool() as pool:
        results = pool.map(fetch_url, urls)
    
    return results


def thread_pool_executor_requests() -> List[Dict[str, Any]]:
    """
    Make HTTP requests using ThreadPoolExecutor.
    
    Returns:
        List of response data.
    """
    print("Making ThreadPoolExecutor requests...")
    
    # Generate URLs by repeating the list
    urls = [URLS[i % len(URLS)] for i in range(NUM_REQUESTS)]
    
    def fetch_url(url: str) -> Dict[str, Any]:
        """Fetch a URL and return the result."""
        response = requests.get(url)
        return response.json()
    
    # Use ThreadPoolExecutor to fetch URLs
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_url, urls))
    
    return results


def process_pool_executor_requests() -> List[Dict[str, Any]]:
    """
    Make HTTP requests using ProcessPoolExecutor.
    
    Returns:
        List of response data.
    """
    print("Making ProcessPoolExecutor requests...")
    
    # Generate URLs by repeating the list
    urls = [URLS[i % len(URLS)] for i in range(NUM_REQUESTS)]
    
    def fetch_url(url: str) -> Dict[str, Any]:
        """Fetch a URL and return the result."""
        response = requests.get(url)
        return response.json()
    
    # Use ProcessPoolExecutor to fetch URLs
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(fetch_url, urls))
    
    return results


async def fetch_url_async(url: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
    """
    Fetch a URL asynchronously.
    
    Args:
        url: URL to fetch.
        session: aiohttp client session.
        
    Returns:
        Response data.
    """
    async with session.get(url) as response:
        return await response.json()


async def asyncio_requests_impl() -> List[Dict[str, Any]]:
    """
    Implementation of asyncio requests.
    
    Returns:
        List of response data.
    """
    # Generate URLs by repeating the list
    urls = [URLS[i % len(URLS)] for i in range(NUM_REQUESTS)]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url_async(url, session) for url in urls]
        results = await asyncio.gather(*tasks)
    
    return results


def asyncio_requests() -> List[Dict[str, Any]]:
    """
    Make HTTP requests using asyncio.
    
    Returns:
        List of response data.
    """
    print("Making asyncio requests...")
    return asyncio.run(asyncio_requests_impl())


def run_comparison() -> None:
    """Run the I/O-bound task comparison."""
    print("=== I/O-Bound Task Comparison ===")
    print(f"Making {NUM_REQUESTS} HTTP requests using different concurrency approaches")
    
    # Define the approaches to compare
    approaches = {
        "Sequential": sequential_requests,
        "Threaded": threaded_requests,
        "ProcessPool": process_pool_requests,
        "ThreadPoolExecutor": thread_pool_executor_requests,
        "ProcessPoolExecutor": process_pool_executor_requests,
        "Asyncio": asyncio_requests
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
            title=f"I/O-Bound Task Comparison ({NUM_REQUESTS} HTTP Requests)",
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