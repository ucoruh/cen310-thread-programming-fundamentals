"""
Synchronization examples demonstrating thread synchronization mechanisms.

This module shows how to use various synchronization primitives in Python's threading module.
"""

import threading
import time
import random
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor


def lock_example() -> None:
    """Demonstrate using a Lock to protect shared resources."""
    print("\n=== Lock Example ===")
    
    # Shared counter
    counter = 0
    
    # Create a lock
    counter_lock = threading.Lock()
    
    def increment_counter(name: str, iterations: int) -> None:
        """
        Increment the counter with lock protection.
        
        Args:
            name: Thread name.
            iterations: Number of increments to perform.
        """
        nonlocal counter
        
        for i in range(iterations):
            # Acquire the lock
            counter_lock.acquire()
            try:
                # Critical section (protected by lock)
                current = counter
                time.sleep(0.000001)  # Simulate some work
                counter = current + 1
            finally:
                # Release the lock
                counter_lock.release()
            
            # Non-critical section
            time.sleep(0.0001)  # Simulate other work
        
        print(f"Thread {name}: finished {iterations} increments")
    
    # Create threads
    threads = []
    num_threads = 5
    iterations_per_thread = 100
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=increment_counter, 
            args=(f"{i}", iterations_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    expected_count = num_threads * iterations_per_thread
    print(f"Final counter value: {counter}")
    print(f"Expected counter value: {expected_count}")
    print(f"Counter is {'correct' if counter == expected_count else 'incorrect'}")
    
    # Demonstrate the same operation without locks (race condition)
    counter = 0
    
    def increment_counter_no_lock(name: str, iterations: int) -> None:
        """
        Increment the counter without lock protection.
        
        Args:
            name: Thread name.
            iterations: Number of increments to perform.
        """
        nonlocal counter
        
        for i in range(iterations):
            # No lock protection - race condition
            current = counter
            time.sleep(0.000001)  # Simulate some work
            counter = current + 1
            
            # Non-critical section
            time.sleep(0.0001)  # Simulate other work
        
        print(f"Thread {name}: finished {iterations} increments (no lock)")
    
    # Create threads without lock protection
    threads = []
    
    for i in range(num_threads):
        thread = threading.Thread(
            target=increment_counter_no_lock, 
            args=(f"{i}", iterations_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"Final counter value (no lock): {counter}")
    print(f"Expected counter value: {expected_count}")
    print(f"Counter is {'correct' if counter == expected_count else 'incorrect (race condition)'}")


def rlock_example() -> None:
    """Demonstrate using an RLock (reentrant lock)."""
    print("\n=== RLock Example ===")
    
    # Create a reentrant lock
    rlock = threading.RLock()
    
    def outer_function() -> None:
        """Outer function that acquires the lock and calls inner_function."""
        print("Outer function: acquiring lock")
        with rlock:
            print("Outer function: lock acquired")
            time.sleep(0.1)
            print("Outer function: calling inner function")
            inner_function()
            print("Outer function: inner function returned")
        print("Outer function: lock released")
    
    def inner_function() -> None:
        """Inner function that also acquires the lock."""
        print("Inner function: acquiring lock")
        with rlock:
            print("Inner function: lock acquired (reentrant)")
            time.sleep(0.1)
        print("Inner function: lock released")
    
    # Create a thread
    thread = threading.Thread(target=outer_function)
    thread.start()
    thread.join()
    
    # Demonstrate the same with a regular Lock (would deadlock)
    print("\nWith a regular Lock, this would deadlock:")
    regular_lock = threading.Lock()
    
    def outer_function_deadlock() -> None:
        """Outer function that would deadlock with a regular lock."""
        print("Outer function: acquiring regular lock")
        with regular_lock:
            print("Outer function: regular lock acquired")
            time.sleep(0.1)
            print("Outer function: calling inner function (would deadlock with regular lock)")
            print("Outer function: NOT calling inner_function_deadlock() to avoid actual deadlock")
            # inner_function_deadlock()  # This would deadlock
        print("Outer function: regular lock released")
    
    def inner_function_deadlock() -> None:
        """Inner function that would deadlock with a regular lock."""
        print("Inner function: trying to acquire regular lock (would deadlock)")
        with regular_lock:
            print("Inner function: regular lock acquired (never reached)")
            time.sleep(0.1)
        print("Inner function: regular lock released (never reached)")
    
    # Create a thread
    thread = threading.Thread(target=outer_function_deadlock)
    thread.start()
    thread.join()


def semaphore_example() -> None:
    """Demonstrate using a Semaphore to limit concurrent access."""
    print("\n=== Semaphore Example ===")
    
    # Create a semaphore with a limit of 3 concurrent accesses
    semaphore = threading.Semaphore(3)
    
    def worker(name: str) -> None:
        """
        Worker function that uses the semaphore.
        
        Args:
            name: Worker name.
        """
        print(f"Worker {name}: waiting to acquire semaphore")
        with semaphore:
            print(f"Worker {name}: semaphore acquired")
            # Simulate work
            time.sleep(random.uniform(0.5, 1.5))
            print(f"Worker {name}: releasing semaphore")
    
    # Create threads
    threads = []
    for i in range(10):
        thread = threading.Thread(target=worker, args=(f"{i}",))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("All workers finished")


def bounded_semaphore_example() -> None:
    """Demonstrate using a BoundedSemaphore to limit concurrent access."""
    print("\n=== BoundedSemaphore Example ===")
    
    # Create a bounded semaphore with a limit of 3 concurrent accesses
    semaphore = threading.BoundedSemaphore(3)
    
    def worker(name: str) -> None:
        """
        Worker function that uses the bounded semaphore.
        
        Args:
            name: Worker name.
        """
        print(f"Worker {name}: waiting to acquire bounded semaphore")
        with semaphore:
            print(f"Worker {name}: bounded semaphore acquired")
            # Simulate work
            time.sleep(random.uniform(0.2, 0.5))
            print(f"Worker {name}: releasing bounded semaphore")
    
    # Create threads
    threads = []
    for i in range(6):
        thread = threading.Thread(target=worker, args=(f"{i}",))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("All workers finished")
    
    # Demonstrate the difference between Semaphore and BoundedSemaphore
    print("\nDifference between Semaphore and BoundedSemaphore:")
    
    regular_semaphore = threading.Semaphore(2)
    bounded_semaphore = threading.BoundedSemaphore(2)
    
    # Release the semaphores twice (acquire them first)
    regular_semaphore.acquire()
    regular_semaphore.acquire()
    bounded_semaphore.acquire()
    bounded_semaphore.acquire()
    
    # Release them
    regular_semaphore.release()
    regular_semaphore.release()
    bounded_semaphore.release()
    bounded_semaphore.release()
    
    # Release regular semaphore one more time (allowed but incorrect)
    try:
        print("Releasing regular semaphore one more time (allowed but incorrect)")
        regular_semaphore.release()
        print("Regular semaphore released (no error)")
    except ValueError as e:
        print(f"Error: {e}")
    
    # Release bounded semaphore one more time (raises ValueError)
    try:
        print("Releasing bounded semaphore one more time (should raise ValueError)")
        bounded_semaphore.release()
        print("Bounded semaphore released (no error - this shouldn't happen)")
    except ValueError as e:
        print(f"Error: {e} (expected behavior)")


def event_example() -> None:
    """Demonstrate using an Event for thread synchronization."""
    print("\n=== Event Example ===")
    
    # Create an event
    event = threading.Event()
    
    def waiter(name: str) -> None:
        """
        Waiter function that waits for the event to be set.
        
        Args:
            name: Waiter name.
        """
        print(f"Waiter {name}: waiting for event")
        event.wait()
        print(f"Waiter {name}: event received, continuing")
    
    def setter() -> None:
        """Setter function that sets the event after a delay."""
        print("Setter: waiting before setting event")
        time.sleep(2)
        print("Setter: setting event")
        event.set()
    
    # Create threads
    waiters = []
    for i in range(5):
        waiter_thread = threading.Thread(target=waiter, args=(f"{i}",))
        waiters.append(waiter_thread)
        waiter_thread.start()
    
    setter_thread = threading.Thread(target=setter)
    setter_thread.start()
    
    # Wait for all threads to complete
    for waiter_thread in waiters:
        waiter_thread.join()
    
    setter_thread.join()
    
    # Demonstrate clearing and re-setting the event
    print("\nDemonstrating clearing and re-setting the event:")
    
    # Clear the event
    event.clear()
    
    def waiter_with_timeout(name: str, timeout: float) -> None:
        """
        Waiter function with timeout.
        
        Args:
            name: Waiter name.
            timeout: Timeout in seconds.
        """
        print(f"Waiter {name}: waiting for event with timeout {timeout}s")
        result = event.wait(timeout)
        if result:
            print(f"Waiter {name}: event received, continuing")
        else:
            print(f"Waiter {name}: timeout occurred, continuing anyway")
    
    # Create threads with timeouts
    waiters = []
    for i in range(3):
        waiter_thread = threading.Thread(
            target=waiter_with_timeout, 
            args=(f"{i}", (i + 1) * 0.5)
        )
        waiters.append(waiter_thread)
        waiter_thread.start()
    
    # Set the event after all timeouts have expired
    time.sleep(2)
    print("Main thread: setting event after timeouts")
    event.set()
    
    # Wait for all threads to complete
    for waiter_thread in waiters:
        waiter_thread.join()


def condition_example() -> None:
    """Demonstrate using a Condition for thread synchronization."""
    print("\n=== Condition Example ===")
    
    # Create a condition and a shared list
    condition = threading.Condition()
    items: List[int] = []
    
    def consumer() -> None:
        """Consumer function that waits for items and processes them."""
        with condition:
            while len(items) < 10:  # Process 10 items
                if not items:  # No items to process
                    print("Consumer: no items to process, waiting...")
                    condition.wait()  # Wait for notification
                
                # Process an item
                item = items.pop(0)
                print(f"Consumer: processing item {item}")
                time.sleep(random.uniform(0.2, 0.5))  # Simulate processing
                
                # Notify producer that an item was consumed
                condition.notify()
            
            print("Consumer: finished processing items")
    
    def producer() -> None:
        """Producer function that creates items and notifies the consumer."""
        with condition:
            for i in range(10):  # Produce 10 items
                if len(items) >= 2:  # Limit buffer size to 2
                    print("Producer: buffer full, waiting...")
                    condition.wait()  # Wait for notification
                
                # Produce an item
                item = i
                items.append(item)
                print(f"Producer: produced item {item}")
                time.sleep(random.uniform(0.1, 0.3))  # Simulate production
                
                # Notify consumer that an item is available
                condition.notify()
            
            print("Producer: finished producing items")
    
    # Create threads
    consumer_thread = threading.Thread(target=consumer)
    producer_thread = threading.Thread(target=producer)
    
    # Start threads
    consumer_thread.start()
    producer_thread.start()
    
    # Wait for threads to complete
    consumer_thread.join()
    producer_thread.join()
    
    print("Producer-consumer example completed")


def barrier_example() -> None:
    """Demonstrate using a Barrier for thread synchronization."""
    print("\n=== Barrier Example ===")
    
    # Number of threads
    num_threads = 5
    
    # Create a barrier
    barrier = threading.Barrier(num_threads)
    
    def worker(name: str) -> None:
        """
        Worker function that uses the barrier.
        
        Args:
            name: Worker name.
        """
        # Phase 1
        print(f"Worker {name}: starting phase 1")
        time.sleep(random.uniform(0.5, 1.5))  # Simulate work
        print(f"Worker {name}: phase 1 complete, waiting at barrier")
        barrier.wait()
        
        # Phase 2 (all threads have completed phase 1)
        print(f"Worker {name}: starting phase 2")
        time.sleep(random.uniform(0.5, 1.5))  # Simulate work
        print(f"Worker {name}: phase 2 complete, waiting at barrier")
        barrier.wait()
        
        # Phase 3 (all threads have completed phase 2)
        print(f"Worker {name}: starting phase 3")
        time.sleep(random.uniform(0.5, 1.5))  # Simulate work
        print(f"Worker {name}: phase 3 complete, waiting at barrier")
        barrier.wait()
        
        print(f"Worker {name}: all phases complete")
    
    # Create threads
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(f"{i}",))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("Barrier example completed")


def timer_example() -> None:
    """Demonstrate using a Timer for delayed execution."""
    print("\n=== Timer Example ===")
    
    def delayed_function(name: str) -> None:
        """
        Function to be executed after a delay.
        
        Args:
            name: Function name.
        """
        print(f"Delayed function {name} executed")
    
    # Create timers
    timer1 = threading.Timer(1.0, delayed_function, args=("Timer-1",))
    timer2 = threading.Timer(2.0, delayed_function, args=("Timer-2",))
    timer3 = threading.Timer(3.0, delayed_function, args=("Timer-3",))
    
    # Start timers
    print("Starting timers")
    timer1.start()
    timer2.start()
    timer3.start()
    
    # Wait for a bit
    time.sleep(1.5)
    
    # Cancel one timer
    print("Cancelling Timer-3")
    timer3.cancel()
    
    # Wait for timers to complete
    timer1.join()
    timer2.join()
    timer3.join()
    
    print("Timer example completed")


def run_demo() -> None:
    """Run all synchronization examples."""
    print("=== Thread Synchronization Examples ===")
    
    lock_example()
    rlock_example()
    semaphore_example()
    bounded_semaphore_example()
    event_example()
    condition_example()
    barrier_example()
    timer_example()
    
    print("\nAll synchronization examples completed")


if __name__ == "__main__":
    run_demo() 