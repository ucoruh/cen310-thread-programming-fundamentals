"""
Basic threading examples demonstrating thread creation and management.

This module shows how to create and use threads in Python using the threading module.
"""

import threading
import time
import random
from typing import List, Callable, Any, Optional, Dict, Union


def thread_function(name: str, sleep_time: float = 1.0) -> None:
    """
    A simple function to be executed in a thread.
    
    Args:
        name: The name of the thread.
        sleep_time: Time to sleep in seconds.
    """
    print(f"Thread {name}: starting")
    time.sleep(sleep_time)
    print(f"Thread {name}: finishing")


def basic_thread_creation() -> None:
    """Demonstrate basic thread creation and joining."""
    print("\n=== Basic Thread Creation ===")
    
    # Create a thread
    thread = threading.Thread(target=thread_function, args=("1",))
    
    # Start the thread
    print("Main thread: starting thread")
    thread.start()
    
    # Wait for the thread to complete
    print("Main thread: waiting for thread to finish")
    thread.join()
    
    print("Main thread: all done")


def daemon_thread_example() -> None:
    """Demonstrate daemon threads that exit when the main program exits."""
    print("\n=== Daemon Thread Example ===")
    
    # Create a daemon thread
    daemon_thread = threading.Thread(
        target=thread_function, 
        args=("Daemon", 2.0),
        daemon=True
    )
    
    # Create a non-daemon thread
    non_daemon_thread = threading.Thread(
        target=thread_function, 
        args=("Non-Daemon", 1.0),
        daemon=False
    )
    
    # Start both threads
    daemon_thread.start()
    non_daemon_thread.start()
    
    print("Main thread: daemon thread started, not waiting for it")
    print("Main thread: waiting for non-daemon thread")
    
    # Wait only for the non-daemon thread
    non_daemon_thread.join()
    
    print("Main thread: non-daemon thread finished")
    print("Main thread: exiting (daemon thread may not finish)")


def multiple_threads_example(num_threads: int = 5) -> None:
    """
    Demonstrate creating and managing multiple threads.
    
    Args:
        num_threads: Number of threads to create.
    """
    print(f"\n=== Multiple Threads Example ({num_threads} threads) ===")
    
    threads: List[threading.Thread] = []
    
    # Create and start threads
    for i in range(num_threads):
        sleep_time = random.uniform(0.5, 2.0)
        thread = threading.Thread(
            target=thread_function, 
            args=(f"{i}", sleep_time)
        )
        threads.append(thread)
        print(f"Main thread: created thread {i}")
        thread.start()
    
    # Wait for all threads to complete
    for i, thread in enumerate(threads):
        print(f"Main thread: waiting for thread {i} to finish")
        thread.join()
        print(f"Main thread: thread {i} finished")
    
    print("Main thread: all threads finished")


def thread_with_arguments() -> None:
    """Demonstrate passing arguments to threads."""
    print("\n=== Thread with Arguments ===")
    
    def worker(name: str, values: List[int], result_dict: Dict[str, int]) -> None:
        """
        Worker function that processes a list of values.
        
        Args:
            name: Worker name.
            values: List of values to process.
            result_dict: Dictionary to store the result.
        """
        print(f"Worker {name}: starting")
        total = sum(values)
        time.sleep(random.uniform(0.5, 1.5))  # Simulate work
        result_dict[name] = total
        print(f"Worker {name}: finished, sum = {total}")
    
    # Shared dictionary to store results
    results: Dict[str, int] = {}
    
    # Create threads with different arguments
    thread1 = threading.Thread(
        target=worker, 
        args=("A", [1, 2, 3, 4, 5], results)
    )
    
    thread2 = threading.Thread(
        target=worker, 
        args=("B", [10, 20, 30, 40, 50], results)
    )
    
    # Start threads
    thread1.start()
    thread2.start()
    
    # Wait for threads to complete
    thread1.join()
    thread2.join()
    
    print(f"Main thread: all workers finished")
    print(f"Results: {results}")


def thread_with_return_value() -> None:
    """Demonstrate getting return values from threads."""
    print("\n=== Thread with Return Value ===")
    
    class WorkerWithResult(threading.Thread):
        """Thread subclass that can return a result."""
        
        def __init__(self, name: str, values: List[int]):
            """
            Initialize the thread.
            
            Args:
                name: Thread name.
                values: List of values to process.
            """
            super().__init__(name=name)
            self.values = values
            self.result: Optional[int] = None
        
        def run(self) -> None:
            """Run the thread and calculate the sum of values."""
            print(f"Worker {self.name}: starting")
            self.result = sum(self.values)
            time.sleep(random.uniform(0.5, 1.5))  # Simulate work
            print(f"Worker {self.name}: finished, sum = {self.result}")
    
    # Create thread instances
    worker1 = WorkerWithResult("X", [1, 2, 3, 4, 5])
    worker2 = WorkerWithResult("Y", [10, 20, 30, 40, 50])
    
    # Start threads
    worker1.start()
    worker2.start()
    
    # Wait for threads to complete
    worker1.join()
    worker2.join()
    
    # Get results
    print(f"Main thread: Worker {worker1.name} result: {worker1.result}")
    print(f"Main thread: Worker {worker2.name} result: {worker2.result}")
    print(f"Main thread: Total: {(worker1.result or 0) + (worker2.result or 0)}")


def thread_local_storage_example() -> None:
    """Demonstrate thread-local storage."""
    print("\n=== Thread-Local Storage Example ===")
    
    # Create thread-local storage
    thread_local = threading.local()
    
    def worker(name: str) -> None:
        """
        Worker function that uses thread-local storage.
        
        Args:
            name: Worker name.
        """
        # Each thread has its own 'value' attribute
        thread_local.value = name
        time.sleep(random.uniform(0.2, 0.5))
        print(f"Worker {name}: thread_local.value = {thread_local.value}")
    
    # Create threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(f"Thread-{i}",))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Main thread doesn't see thread-local values from other threads
    try:
        print(f"Main thread: thread_local.value = {thread_local.value}")
    except AttributeError:
        print("Main thread: thread_local.value is not set in this thread")


def thread_exception_handling() -> None:
    """Demonstrate handling exceptions in threads."""
    print("\n=== Thread Exception Handling ===")
    
    def worker_with_exception(name: str) -> None:
        """
        Worker function that raises an exception.
        
        Args:
            name: Worker name.
        """
        print(f"Worker {name}: starting")
        time.sleep(0.5)
        
        # Raise an exception
        raise ValueError(f"Exception in worker {name}")
    
    # Create a thread
    thread = threading.Thread(target=worker_with_exception, args=("Error",))
    
    # Start the thread
    thread.start()
    
    # Wait for the thread to complete
    thread.join()
    
    print("Main thread: thread finished (exception was raised but not propagated to main thread)")
    
    # Better approach: use a wrapper function to catch exceptions
    def worker_wrapper(func: Callable, *args: Any, **kwargs: Any) -> None:
        """
        Wrapper function to catch exceptions in a thread.
        
        Args:
            func: Function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Exception caught in thread: {e}")
    
    # Create a thread with the wrapper
    safe_thread = threading.Thread(
        target=worker_wrapper, 
        args=(worker_with_exception, "SafeError")
    )
    
    # Start the thread
    safe_thread.start()
    
    # Wait for the thread to complete
    safe_thread.join()
    
    print("Main thread: safe thread finished (exception was caught in the wrapper)")


def run_demo() -> None:
    """Run all threading examples."""
    print("=== Basic Threading Examples ===")
    
    basic_thread_creation()
    daemon_thread_example()
    multiple_threads_example()
    thread_with_arguments()
    thread_with_return_value()
    thread_local_storage_example()
    thread_exception_handling()
    
    print("\nAll threading examples completed")


if __name__ == "__main__":
    run_demo() 