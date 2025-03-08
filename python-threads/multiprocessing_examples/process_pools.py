"""
Process pools examples for multiprocessing.

This module demonstrates how to use process pools for parallel execution in Python.
"""

import multiprocessing as mp
import time
import random
import os
import sys
import math
from typing import List, Dict, Any, Optional, Tuple, Callable
from concurrent.futures import ProcessPoolExecutor


def basic_pool_example() -> None:
    """Demonstrate basic usage of a process pool."""
    print("\n=== Basic Process Pool Example ===")
    
    def worker_function(x: int) -> Tuple[int, int, float]:
        """
        A worker function that performs a computation.
        
        Args:
            x: Input value.
            
        Returns:
            Tuple containing (input value, process ID, result).
        """
        # Simulate some computation
        result = x * x
        
        # Simulate variable processing time
        time.sleep(random.uniform(0.1, 0.5))
        
        return (x, os.getpid(), result)
    
    # Create a pool of worker processes
    num_processes = min(4, mp.cpu_count())
    print(f"Creating a pool with {num_processes} processes")
    
    with mp.Pool(processes=num_processes) as pool:
        # Submit tasks to the pool
        inputs = list(range(1, 11))
        
        # Map the worker function to the inputs
        results = pool.map(worker_function, inputs)
        
        # Print the results
        print("\nResults:")
        for x, pid, result in results:
            print(f"Input: {x}, Process: {pid}, Result: {result}")


def pool_map_async_example() -> None:
    """Demonstrate asynchronous mapping with a process pool."""
    print("\n=== Process Pool Map Async Example ===")
    
    def worker_function(x: int) -> Tuple[int, int, float]:
        """
        A worker function that performs a computation.
        
        Args:
            x: Input value.
            
        Returns:
            Tuple containing (input value, process ID, result).
        """
        # Simulate some computation
        result = x * x * x
        
        # Simulate variable processing time
        time.sleep(random.uniform(0.1, 0.3))
        
        return (x, os.getpid(), result)
    
    # Create a pool of worker processes
    num_processes = min(4, mp.cpu_count())
    
    with mp.Pool(processes=num_processes) as pool:
        # Submit tasks to the pool asynchronously
        inputs = list(range(1, 11))
        
        # Map the worker function to the inputs asynchronously
        result_async = pool.map_async(worker_function, inputs)
        
        # Do some other work while the tasks are being processed
        print("Tasks submitted asynchronously, doing other work...")
        for i in range(5):
            print(f"Main process: doing other work... ({i+1}/5)")
            time.sleep(0.2)
        
        # Get the results (will block until all tasks are complete)
        print("\nWaiting for results...")
        results = result_async.get()
        
        # Print the results
        print("\nResults:")
        for x, pid, result in results:
            print(f"Input: {x}, Process: {pid}, Result: {result}")


def pool_apply_example() -> None:
    """Demonstrate apply and apply_async with a process pool."""
    print("\n=== Process Pool Apply Example ===")
    
    def worker_function(x: int, y: int) -> Tuple[int, int, int, float]:
        """
        A worker function that performs a computation with multiple arguments.
        
        Args:
            x: First input value.
            y: Second input value.
            
        Returns:
            Tuple containing (first input, second input, process ID, result).
        """
        # Simulate some computation
        result = x ** y
        
        # Simulate variable processing time
        time.sleep(random.uniform(0.1, 0.5))
        
        return (x, y, os.getpid(), result)
    
    # Create a pool of worker processes
    num_processes = min(4, mp.cpu_count())
    
    with mp.Pool(processes=num_processes) as pool:
        # Use apply (blocking)
        print("\nUsing apply (blocking):")
        start_time = time.time()
        
        results = []
        for i in range(1, 6):
            result = pool.apply(worker_function, args=(i, 2))
            results.append(result)
        
        end_time = time.time()
        print(f"Apply completed in {end_time - start_time:.2f} seconds")
        
        # Print the results
        print("\nResults from apply:")
        for x, y, pid, result in results:
            print(f"Input: ({x}, {y}), Process: {pid}, Result: {result}")
        
        # Use apply_async (non-blocking)
        print("\nUsing apply_async (non-blocking):")
        start_time = time.time()
        
        # Submit tasks asynchronously
        async_results = []
        for i in range(1, 6):
            async_result = pool.apply_async(worker_function, args=(i, 3))
            async_results.append(async_result)
        
        # Do some other work
        print("Tasks submitted asynchronously, doing other work...")
        time.sleep(0.5)
        
        # Get the results
        results = [async_result.get() for async_result in async_results]
        
        end_time = time.time()
        print(f"Apply async completed in {end_time - start_time:.2f} seconds")
        
        # Print the results
        print("\nResults from apply_async:")
        for x, y, pid, result in results:
            print(f"Input: ({x}, {y}), Process: {pid}, Result: {result}")


def pool_starmap_example() -> None:
    """Demonstrate starmap with a process pool."""
    print("\n=== Process Pool Starmap Example ===")
    
    def worker_function(x: int, y: int) -> Tuple[int, int, int, float]:
        """
        A worker function that performs a computation with multiple arguments.
        
        Args:
            x: First input value.
            y: Second input value.
            
        Returns:
            Tuple containing (first input, second input, process ID, result).
        """
        # Simulate some computation
        result = x ** y
        
        # Simulate variable processing time
        time.sleep(random.uniform(0.1, 0.3))
        
        return (x, y, os.getpid(), result)
    
    # Create a pool of worker processes
    num_processes = min(4, mp.cpu_count())
    
    with mp.Pool(processes=num_processes) as pool:
        # Create a list of argument tuples
        args_list = [(i, j) for i in range(1, 4) for j in range(1, 4)]
        
        # Use starmap to map the function to multiple arguments
        results = pool.starmap(worker_function, args_list)
        
        # Print the results
        print("\nResults from starmap:")
        for x, y, pid, result in results:
            print(f"Input: ({x}, {y}), Process: {pid}, Result: {result}")
        
        # Use starmap_async
        print("\nUsing starmap_async:")
        
        # Submit tasks asynchronously
        async_result = pool.starmap_async(worker_function, args_list)
        
        # Do some other work
        print("Tasks submitted asynchronously, doing other work...")
        time.sleep(0.5)
        
        # Get the results
        results = async_result.get()
        
        # Print the results
        print("\nResults from starmap_async:")
        for x, y, pid, result in results:
            print(f"Input: ({x}, {y}), Process: {pid}, Result: {result}")


def pool_callback_example() -> None:
    """Demonstrate callbacks with a process pool."""
    print("\n=== Process Pool Callback Example ===")
    
    def worker_function(x: int) -> Tuple[int, int, float]:
        """
        A worker function that performs a computation.
        
        Args:
            x: Input value.
            
        Returns:
            Tuple containing (input value, process ID, result).
        """
        # Simulate some computation
        result = x * x
        
        # Simulate variable processing time
        time.sleep(random.uniform(0.1, 0.5))
        
        return (x, os.getpid(), result)
    
    def success_callback(result: Tuple[int, int, float]) -> None:
        """
        Callback function for successful task completion.
        
        Args:
            result: Result from the worker function.
        """
        x, pid, value = result
        print(f"Success callback: Input {x}, Process {pid}, Result {value}")
    
    def error_callback(error: Exception) -> None:
        """
        Callback function for task errors.
        
        Args:
            error: Exception raised by the worker function.
        """
        print(f"Error callback: {error}")
    
    # Create a pool of worker processes
    num_processes = min(4, mp.cpu_count())
    
    with mp.Pool(processes=num_processes) as pool:
        # Submit tasks with callbacks
        for i in range(1, 6):
            pool.apply_async(
                worker_function, 
                args=(i,), 
                callback=success_callback,
                error_callback=error_callback
            )
        
        # Submit a task that will raise an error
        def error_function(x: int) -> int:
            """Function that raises an error."""
            time.sleep(0.2)
            raise ValueError(f"Deliberate error for input {x}")
        
        pool.apply_async(
            error_function, 
            args=(10,), 
            callback=success_callback,
            error_callback=error_callback
        )
        
        # Wait for all tasks to complete
        # Note: We need to explicitly wait since we're using callbacks
        print("Waiting for all tasks to complete...")
        time.sleep(2)


def process_pool_executor_example() -> None:
    """Demonstrate the concurrent.futures.ProcessPoolExecutor."""
    print("\n=== ProcessPoolExecutor Example ===")
    
    def worker_function(x: int) -> Tuple[int, int, float]:
        """
        A worker function that performs a computation.
        
        Args:
            x: Input value.
            
        Returns:
            Tuple containing (input value, process ID, result).
        """
        # Simulate some computation
        result = x * x
        
        # Simulate variable processing time
        time.sleep(random.uniform(0.1, 0.3))
        
        return (x, os.getpid(), result)
    
    # Create a process pool executor
    num_processes = min(4, mp.cpu_count())
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(worker_function, i) for i in range(1, 11)]
        
        # Process results as they complete
        from concurrent.futures import as_completed
        
        print("\nProcessing results as they complete:")
        for future in as_completed(futures):
            try:
                x, pid, result = future.result()
                print(f"Input: {x}, Process: {pid}, Result: {result}")
            except Exception as e:
                print(f"Task generated an exception: {e}")
        
        # Use map
        print("\nUsing executor.map:")
        results = list(executor.map(worker_function, range(1, 6)))
        
        for x, pid, result in results:
            print(f"Input: {x}, Process: {pid}, Result: {result}")


def cpu_bound_task_example() -> None:
    """Demonstrate process pools for CPU-bound tasks."""
    print("\n=== CPU-Bound Task Example ===")
    
    def is_prime(n: int) -> Tuple[int, bool]:
        """
        Check if a number is prime.
        
        Args:
            n: Number to check.
            
        Returns:
            Tuple containing (number, is_prime).
        """
        if n <= 1:
            return (n, False)
        if n <= 3:
            return (n, True)
        if n % 2 == 0 or n % 3 == 0:
            return (n, False)
        
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return (n, False)
            i += 6
        
        # Simulate more intensive computation
        time.sleep(0.01)
        
        return (n, True)
    
    # Generate a list of numbers to check
    numbers = list(range(1000, 2000))
    
    # Sequential execution
    print("\nSequential execution:")
    start_time = time.time()
    
    sequential_results = [is_prime(n) for n in numbers]
    sequential_primes = [n for n, is_prime_flag in sequential_results if is_prime_flag]
    
    end_time = time.time()
    sequential_time = end_time - start_time
    print(f"Sequential execution time: {sequential_time:.2f} seconds")
    print(f"Found {len(sequential_primes)} prime numbers")
    
    # Parallel execution with process pool
    print("\nParallel execution with process pool:")
    start_time = time.time()
    
    with mp.Pool() as pool:
        parallel_results = pool.map(is_prime, numbers)
    
    parallel_primes = [n for n, is_prime_flag in parallel_results if is_prime_flag]
    
    end_time = time.time()
    parallel_time = end_time - start_time
    print(f"Parallel execution time: {parallel_time:.2f} seconds")
    print(f"Found {len(parallel_primes)} prime numbers")
    
    # Calculate speedup
    speedup = sequential_time / parallel_time
    print(f"Speedup: {speedup:.2f}x")


def io_bound_task_example() -> None:
    """Demonstrate process pools for I/O-bound tasks."""
    print("\n=== I/O-Bound Task Example ===")
    
    def io_task(task_id: int) -> Tuple[int, float]:
        """
        Simulate an I/O-bound task.
        
        Args:
            task_id: Task identifier.
            
        Returns:
            Tuple containing (task_id, elapsed_time).
        """
        print(f"Task {task_id} starting (PID: {os.getpid()})")
        
        start_time = time.time()
        
        # Simulate I/O operations (e.g., network requests, file operations)
        time.sleep(random.uniform(0.5, 1.0))
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"Task {task_id} completed in {elapsed:.2f} seconds")
        
        return (task_id, elapsed)
    
    # Number of tasks
    num_tasks = 20
    
    # Sequential execution
    print("\nSequential execution:")
    start_time = time.time()
    
    sequential_results = [io_task(i) for i in range(num_tasks)]
    
    end_time = time.time()
    sequential_time = end_time - start_time
    print(f"Sequential execution time: {sequential_time:.2f} seconds")
    
    # Parallel execution with process pool
    print("\nParallel execution with process pool:")
    start_time = time.time()
    
    with mp.Pool() as pool:
        parallel_results = pool.map(io_task, range(num_tasks))
    
    end_time = time.time()
    parallel_time = end_time - start_time
    print(f"Parallel execution time: {parallel_time:.2f} seconds")
    
    # Calculate speedup
    speedup = sequential_time / parallel_time
    print(f"Speedup: {speedup:.2f}x")


def pool_initializer_example() -> None:
    """Demonstrate using an initializer function with a process pool."""
    print("\n=== Process Pool Initializer Example ===")
    
    # Global variables to be initialized in each process
    process_data = {}
    
    def initializer(init_value: int) -> None:
        """
        Initialize process-specific data.
        
        Args:
            init_value: Initial value for the process data.
        """
        # Use the global variable
        global process_data
        
        # Initialize process-specific data
        pid = os.getpid()
        process_data = {
            'pid': pid,
            'value': init_value,
            'start_time': time.time()
        }
        
        print(f"Process {pid} initialized with value {init_value}")
    
    def worker_function(x: int) -> Tuple[int, Dict[str, Any]]:
        """
        Worker function that uses the initialized data.
        
        Args:
            x: Input value.
            
        Returns:
            Tuple containing (input value, process data).
        """
        # Access the global variable
        global process_data
        
        # Update the process data
        process_data['value'] += x
        process_data['last_input'] = x
        process_data['elapsed'] = time.time() - process_data['start_time']
        
        # Simulate some work
        time.sleep(random.uniform(0.1, 0.3))
        
        return (x, process_data.copy())
    
    # Create a pool with an initializer
    with mp.Pool(
        processes=4, 
        initializer=initializer, 
        initargs=(100,)
    ) as pool:
        # Submit tasks to the pool
        results = pool.map(worker_function, range(1, 11))
        
        # Print the results
        print("\nResults:")
        for x, data in results:
            print(f"Input: {x}, Process: {data['pid']}, Value: {data['value']}, Elapsed: {data['elapsed']:.2f}s")


def run_demo() -> None:
    """Run all process pool examples."""
    print("=== Process Pool Examples ===")
    
    basic_pool_example()
    pool_map_async_example()
    pool_apply_example()
    pool_starmap_example()
    pool_callback_example()
    process_pool_executor_example()
    cpu_bound_task_example()
    io_bound_task_example()
    pool_initializer_example()
    
    print("\nAll process pool examples completed")


if __name__ == "__main__":
    run_demo() 