"""
Basic multiprocessing examples demonstrating process creation and management.

This module shows how to create and use processes in Python using the multiprocessing module.
"""

import multiprocessing as mp
import time
import random
import os
import sys
from typing import List, Dict, Any, Optional, Tuple


def process_function(name: str, sleep_time: float = 1.0) -> None:
    """
    A simple function to be executed in a process.
    
    Args:
        name: The name of the process.
        sleep_time: Time to sleep in seconds.
    """
    print(f"Process {name}: starting (PID: {os.getpid()})")
    time.sleep(sleep_time)
    print(f"Process {name}: finishing (PID: {os.getpid()})")


def basic_process_creation() -> None:
    """Demonstrate basic process creation and joining."""
    print("\n=== Basic Process Creation ===")
    
    # Print main process info
    print(f"Main process: PID = {os.getpid()}")
    
    # Create a process
    process = mp.Process(target=process_function, args=("1",))
    
    # Start the process
    print("Main process: starting process")
    process.start()
    
    # Wait for the process to complete
    print("Main process: waiting for process to finish")
    process.join()
    
    print("Main process: all done")


def daemon_process_example() -> None:
    """Demonstrate daemon processes that exit when the main program exits."""
    print("\n=== Daemon Process Example ===")
    
    # Create a daemon process
    daemon_process = mp.Process(
        target=process_function, 
        args=("Daemon", 2.0),
        daemon=True
    )
    
    # Create a non-daemon process
    non_daemon_process = mp.Process(
        target=process_function, 
        args=("Non-Daemon", 1.0),
        daemon=False
    )
    
    # Start both processes
    daemon_process.start()
    non_daemon_process.start()
    
    print("Main process: daemon process started, not waiting for it")
    print("Main process: waiting for non-daemon process")
    
    # Wait only for the non-daemon process
    non_daemon_process.join()
    
    print("Main process: non-daemon process finished")
    print("Main process: exiting (daemon process may not finish)")


def multiple_processes_example(num_processes: int = 5) -> None:
    """
    Demonstrate creating and managing multiple processes.
    
    Args:
        num_processes: Number of processes to create.
    """
    print(f"\n=== Multiple Processes Example ({num_processes} processes) ===")
    
    processes: List[mp.Process] = []
    
    # Create and start processes
    for i in range(num_processes):
        sleep_time = random.uniform(0.5, 2.0)
        process = mp.Process(
            target=process_function, 
            args=(f"{i}", sleep_time)
        )
        processes.append(process)
        print(f"Main process: created process {i}")
        process.start()
    
    # Wait for all processes to complete
    for i, process in enumerate(processes):
        print(f"Main process: waiting for process {i} to finish")
        process.join()
        print(f"Main process: process {i} finished")
    
    print("Main process: all processes finished")


def process_with_arguments() -> None:
    """Demonstrate passing arguments to processes."""
    print("\n=== Process with Arguments ===")
    
    def worker(name: str, numbers: List[int], results_dict: Dict[str, int]) -> None:
        """
        Worker function that processes a list of numbers.
        
        Args:
            name: Worker name.
            numbers: List of numbers to process.
            results_dict: Dictionary to store the result.
        """
        print(f"Worker {name}: starting (PID: {os.getpid()})")
        total = sum(numbers)
        time.sleep(random.uniform(0.5, 1.5))  # Simulate work
        results_dict[name] = total
        print(f"Worker {name}: finished, sum = {total}")
    
    # Create a manager for sharing objects between processes
    with mp.Manager() as manager:
        # Shared dictionary to store results
        results = manager.dict()
        
        # Create processes with different arguments
        process1 = mp.Process(
            target=worker, 
            args=("A", [1, 2, 3, 4, 5], results)
        )
        
        process2 = mp.Process(
            target=worker, 
            args=("B", [10, 20, 30, 40, 50], results)
        )
        
        # Start processes
        process1.start()
        process2.start()
        
        # Wait for processes to complete
        process1.join()
        process2.join()
        
        # Convert manager dict to regular dict for printing
        results_dict = dict(results)
        
        print(f"Main process: all workers finished")
        print(f"Results: {results_dict}")


def process_with_return_value() -> None:
    """Demonstrate getting return values from processes using a queue."""
    print("\n=== Process with Return Value ===")
    
    def worker(name: str, numbers: List[int], result_queue: mp.Queue) -> None:
        """
        Worker function that calculates the sum of numbers and puts the result in a queue.
        
        Args:
            name: Worker name.
            numbers: List of numbers to sum.
            result_queue: Queue to store the result.
        """
        print(f"Worker {name}: starting (PID: {os.getpid()})")
        total = sum(numbers)
        time.sleep(random.uniform(0.5, 1.5))  # Simulate work
        result_queue.put((name, total))
        print(f"Worker {name}: finished, sum = {total}")
    
    # Create a queue for results
    result_queue = mp.Queue()
    
    # Create processes
    process1 = mp.Process(
        target=worker, 
        args=("X", [1, 2, 3, 4, 5], result_queue)
    )
    
    process2 = mp.Process(
        target=worker, 
        args=("Y", [10, 20, 30, 40, 50], result_queue)
    )
    
    # Start processes
    process1.start()
    process2.start()
    
    # Wait for processes to complete
    process1.join()
    process2.join()
    
    # Get results from the queue
    results = {}
    while not result_queue.empty():
        name, total = result_queue.get()
        results[name] = total
    
    print(f"Main process: Worker X result: {results.get('X')}")
    print(f"Main process: Worker Y result: {results.get('Y')}")
    print(f"Main process: Total: {sum(results.values())}")


def process_termination_example() -> None:
    """Demonstrate terminating a process."""
    print("\n=== Process Termination Example ===")
    
    def long_running_task() -> None:
        """A long-running task that can be terminated."""
        print(f"Long-running task: starting (PID: {os.getpid()})")
        try:
            while True:
                print("Long-running task: working...")
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Long-running task: received KeyboardInterrupt")
        finally:
            print("Long-running task: cleaning up")
            print("Long-running task: exiting")
    
    # Create a process
    process = mp.Process(target=long_running_task)
    
    # Start the process
    print("Main process: starting long-running task")
    process.start()
    
    # Let it run for a bit
    time.sleep(2)
    
    # Terminate the process
    print("Main process: terminating process")
    process.terminate()
    
    # Wait for the process to terminate
    process.join()
    
    print(f"Main process: process is alive: {process.is_alive()}")
    print(f"Main process: process exit code: {process.exitcode}")


def process_communication_pipe() -> None:
    """Demonstrate communication between processes using a pipe."""
    print("\n=== Process Communication with Pipe ===")
    
    def sender(conn: mp.connection.Connection) -> None:
        """
        Sender function that sends messages through a pipe.
        
        Args:
            conn: Connection object for sending messages.
        """
        print(f"Sender: starting (PID: {os.getpid()})")
        
        for i in range(5):
            message = f"Message {i+1}"
            conn.send(message)
            print(f"Sender: sent '{message}'")
            time.sleep(random.uniform(0.1, 0.5))
        
        # Signal that we're done
        conn.send(None)
        print("Sender: sent completion signal")
        
        # Close the connection
        conn.close()
        print("Sender: closed connection")
    
    def receiver(conn: mp.connection.Connection) -> None:
        """
        Receiver function that receives messages from a pipe.
        
        Args:
            conn: Connection object for receiving messages.
        """
        print(f"Receiver: starting (PID: {os.getpid()})")
        
        while True:
            if conn.poll(timeout=1.0):  # Check if there's data to receive
                message = conn.recv()
                
                if message is None:
                    print("Receiver: received completion signal")
                    break
                
                print(f"Receiver: received '{message}'")
                time.sleep(random.uniform(0.1, 0.3))
            else:
                print("Receiver: no message received (timeout)")
        
        # Close the connection
        conn.close()
        print("Receiver: closed connection")
    
    # Create a pipe
    parent_conn, child_conn = mp.Pipe()
    
    # Create processes
    sender_process = mp.Process(target=sender, args=(parent_conn,))
    receiver_process = mp.Process(target=receiver, args=(child_conn,))
    
    # Start processes
    sender_process.start()
    receiver_process.start()
    
    # Wait for processes to complete
    sender_process.join()
    receiver_process.join()
    
    print("Process communication with pipe completed")


def process_communication_queue() -> None:
    """Demonstrate communication between processes using a queue."""
    print("\n=== Process Communication with Queue ===")
    
    def producer(queue: mp.Queue) -> None:
        """
        Producer function that puts items in the queue.
        
        Args:
            queue: Queue for sending items.
        """
        print(f"Producer: starting (PID: {os.getpid()})")
        
        for i in range(5):
            item = f"Item {i+1}"
            queue.put(item)
            print(f"Producer: put '{item}' in the queue")
            time.sleep(random.uniform(0.1, 0.5))
        
        # Signal that we're done
        queue.put(None)
        print("Producer: put completion signal in the queue")
    
    def consumer(queue: mp.Queue) -> None:
        """
        Consumer function that gets items from the queue.
        
        Args:
            queue: Queue for receiving items.
        """
        print(f"Consumer: starting (PID: {os.getpid()})")
        
        while True:
            try:
                item = queue.get(timeout=1.0)
                
                if item is None:
                    print("Consumer: received completion signal")
                    break
                
                print(f"Consumer: got '{item}' from the queue")
                time.sleep(random.uniform(0.1, 0.3))
            except mp.queues.Empty:
                print("Consumer: no item received (timeout)")
        
        print("Consumer: finished")
    
    # Create a queue
    queue = mp.Queue()
    
    # Create processes
    producer_process = mp.Process(target=producer, args=(queue,))
    consumer_process = mp.Process(target=consumer, args=(queue,))
    
    # Start processes
    producer_process.start()
    consumer_process.start()
    
    # Wait for processes to complete
    producer_process.join()
    consumer_process.join()
    
    print("Process communication with queue completed")


def process_errors_example() -> None:
    """Demonstrate handling errors in processes."""
    print("\n=== Process Errors Example ===")
    
    def process_with_error() -> None:
        """Process function that raises an error."""
        print(f"Error process: starting (PID: {os.getpid()})")
        time.sleep(0.5)
        
        # Raise an error
        raise ValueError("Deliberate error in process")
    
    # Create a process
    process = mp.Process(target=process_with_error)
    
    # Start the process
    print("Main process: starting process that will raise an error")
    process.start()
    
    # Wait for the process to complete
    process.join()
    
    # Check the exit code
    print(f"Main process: process exit code: {process.exitcode}")
    print("Note: A non-zero exit code indicates that the process terminated with an error")


def run_demo() -> None:
    """Run all multiprocessing examples."""
    print("=== Basic Multiprocessing Examples ===")
    
    # Set the start method for multiprocessing
    # Options: 'spawn', 'fork', 'forkserver'
    # 'spawn' is the default on Windows, 'fork' is the default on Unix
    if sys.platform == 'win32':
        # Windows only supports 'spawn'
        mp.set_start_method('spawn')
    else:
        # On Unix, we can choose
        try:
            mp.set_start_method('spawn')
        except RuntimeError:
            # Method may have been set already in interactive environments
            pass
    
    print(f"Multiprocessing start method: {mp.get_start_method()}")
    print(f"Number of CPU cores: {mp.cpu_count()}")
    
    basic_process_creation()
    daemon_process_example()
    multiple_processes_example()
    process_with_arguments()
    process_with_return_value()
    process_termination_example()
    process_communication_pipe()
    process_communication_queue()
    process_errors_example()
    
    print("\nAll multiprocessing examples completed")


if __name__ == "__main__":
    run_demo() 