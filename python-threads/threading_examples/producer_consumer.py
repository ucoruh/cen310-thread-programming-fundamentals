"""
Producer-consumer pattern examples using threading.

This module demonstrates the producer-consumer pattern using various synchronization mechanisms.
"""

import threading
import queue
import time
import random
from typing import List, Dict, Any, Optional, Tuple, Set
import concurrent.futures


def basic_producer_consumer() -> None:
    """Demonstrate a basic producer-consumer pattern using a queue."""
    print("\n=== Basic Producer-Consumer Pattern ===")
    
    # Create a queue with a maximum size
    task_queue = queue.Queue(maxsize=5)
    
    # Number of items to produce
    num_items = 20
    
    def producer() -> None:
        """Producer function that generates items and puts them in the queue."""
        for i in range(num_items):
            # Create an item
            item = f"Item-{i}"
            
            # Put the item in the queue (blocks if queue is full)
            task_queue.put(item)
            print(f"Producer: produced {item} (queue size: {task_queue.qsize()})")
            
            # Simulate variable production time
            time.sleep(random.uniform(0.1, 0.3))
        
        # Signal that production is done
        task_queue.put(None)
        print("Producer: finished producing items")
    
    def consumer() -> None:
        """Consumer function that gets items from the queue and processes them."""
        while True:
            # Get an item from the queue (blocks if queue is empty)
            item = task_queue.get()
            
            # Check for the sentinel value
            if item is None:
                print("Consumer: received shutdown signal")
                task_queue.task_done()
                break
            
            print(f"Consumer: consumed {item} (queue size: {task_queue.qsize()})")
            
            # Simulate variable consumption time
            time.sleep(random.uniform(0.2, 0.5))
            
            # Mark the task as done
            task_queue.task_done()
        
        print("Consumer: finished consuming items")
    
    # Create and start the producer and consumer threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for both threads to complete
    producer_thread.join()
    consumer_thread.join()
    
    print("Basic producer-consumer pattern completed")


def multiple_producers_consumers() -> None:
    """Demonstrate multiple producers and consumers using a queue."""
    print("\n=== Multiple Producers and Consumers ===")
    
    # Create a queue
    task_queue = queue.Queue(maxsize=10)
    
    # Number of items to produce per producer
    items_per_producer = 10
    
    # Number of producers and consumers
    num_producers = 3
    num_consumers = 2
    
    # Total number of items to produce
    total_items = items_per_producer * num_producers
    
    # Sentinel value to signal consumers to exit
    SENTINEL = object()
    
    # Track consumed items
    consumed_items = 0
    consumed_lock = threading.Lock()
    
    def producer(producer_id: int) -> None:
        """
        Producer function that generates items and puts them in the queue.
        
        Args:
            producer_id: Producer identifier.
        """
        for i in range(items_per_producer):
            # Create an item
            item = f"P{producer_id}-Item-{i}"
            
            # Put the item in the queue (blocks if queue is full)
            task_queue.put(item)
            print(f"Producer {producer_id}: produced {item} (queue size: {task_queue.qsize()})")
            
            # Simulate variable production time
            time.sleep(random.uniform(0.05, 0.2))
        
        print(f"Producer {producer_id}: finished producing items")
    
    def consumer(consumer_id: int) -> None:
        """
        Consumer function that gets items from the queue and processes them.
        
        Args:
            consumer_id: Consumer identifier.
        """
        nonlocal consumed_items
        
        while True:
            # Get an item from the queue (blocks if queue is empty)
            item = task_queue.get()
            
            # Check for the sentinel value
            if item is SENTINEL:
                print(f"Consumer {consumer_id}: received shutdown signal")
                task_queue.task_done()
                break
            
            print(f"Consumer {consumer_id}: consumed {item} (queue size: {task_queue.qsize()})")
            
            # Simulate variable consumption time
            time.sleep(random.uniform(0.1, 0.3))
            
            # Increment the consumed items counter
            with consumed_lock:
                consumed_items += 1
            
            # Mark the task as done
            task_queue.task_done()
        
        print(f"Consumer {consumer_id}: finished consuming items")
    
    # Create and start the producer threads
    producer_threads = []
    for i in range(num_producers):
        thread = threading.Thread(target=producer, args=(i,))
        producer_threads.append(thread)
        thread.start()
    
    # Create and start the consumer threads
    consumer_threads = []
    for i in range(num_consumers):
        thread = threading.Thread(target=consumer, args=(i,))
        consumer_threads.append(thread)
        thread.start()
    
    # Wait for all producers to complete
    for thread in producer_threads:
        thread.join()
    
    # Wait for all items to be processed
    task_queue.join()
    
    # Signal all consumers to exit
    for _ in range(num_consumers):
        task_queue.put(SENTINEL)
    
    # Wait for all consumers to complete
    for thread in consumer_threads:
        thread.join()
    
    # Verify that all items were consumed
    print(f"Consumed {consumed_items} items out of {total_items}")
    
    print("Multiple producers-consumers pattern completed")


def producer_consumer_with_condition() -> None:
    """Demonstrate producer-consumer pattern using a condition variable."""
    print("\n=== Producer-Consumer with Condition Variable ===")
    
    # Create a condition variable
    condition = threading.Condition()
    
    # Shared buffer
    buffer: List[str] = []
    max_buffer_size = 5
    
    # Number of items to produce
    num_items = 20
    
    # Track consumed items
    consumed_items = 0
    
    def producer() -> None:
        """Producer function that generates items and adds them to the buffer."""
        nonlocal buffer
        
        for i in range(num_items):
            # Acquire the condition
            with condition:
                # Wait while the buffer is full
                while len(buffer) >= max_buffer_size:
                    print("Producer: buffer full, waiting...")
                    condition.wait()
                
                # Create an item and add it to the buffer
                item = f"Item-{i}"
                buffer.append(item)
                print(f"Producer: added {item} to buffer (buffer size: {len(buffer)})")
                
                # Notify consumers that an item is available
                condition.notify()
            
            # Simulate variable production time
            time.sleep(random.uniform(0.1, 0.3))
        
        # Signal that production is done by adding a sentinel value
        with condition:
            buffer.append(None)
            condition.notify()
        
        print("Producer: finished producing items")
    
    def consumer() -> None:
        """Consumer function that removes items from the buffer and processes them."""
        nonlocal buffer, consumed_items
        
        while True:
            # Acquire the condition
            with condition:
                # Wait while the buffer is empty
                while not buffer:
                    print("Consumer: buffer empty, waiting...")
                    condition.wait()
                
                # Get an item from the buffer
                item = buffer.pop(0)
                
                # Check for the sentinel value
                if item is None:
                    print("Consumer: received shutdown signal")
                    # Put the sentinel back for other consumers
                    buffer.append(None)
                    condition.notify()
                    break
                
                # Increment the consumed items counter
                consumed_items += 1
                
                print(f"Consumer: removed {item} from buffer (buffer size: {len(buffer)})")
                
                # Notify producers that space is available
                condition.notify()
            
            # Simulate variable consumption time
            time.sleep(random.uniform(0.2, 0.5))
        
        print("Consumer: finished consuming items")
    
    # Create and start the producer and consumer threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for both threads to complete
    producer_thread.join()
    consumer_thread.join()
    
    # Verify that all items were consumed
    print(f"Consumed {consumed_items} items out of {num_items}")
    
    print("Producer-consumer with condition variable completed")


def producer_consumer_with_semaphores() -> None:
    """Demonstrate producer-consumer pattern using semaphores."""
    print("\n=== Producer-Consumer with Semaphores ===")
    
    # Create semaphores
    empty_slots = threading.Semaphore(5)  # Initially 5 empty slots
    filled_slots = threading.Semaphore(0)  # Initially 0 filled slots
    
    # Mutex for buffer access
    buffer_mutex = threading.Lock()
    
    # Shared buffer
    buffer: List[str] = []
    
    # Number of items to produce
    num_items = 20
    
    # Track consumed items
    consumed_items = 0
    
    def producer() -> None:
        """Producer function that generates items and adds them to the buffer."""
        nonlocal buffer
        
        for i in range(num_items):
            # Create an item
            item = f"Item-{i}"
            
            # Wait for an empty slot
            empty_slots.acquire()
            
            # Add the item to the buffer (critical section)
            with buffer_mutex:
                buffer.append(item)
                print(f"Producer: added {item} to buffer (buffer size: {len(buffer)})")
            
            # Signal that a slot is filled
            filled_slots.release()
            
            # Simulate variable production time
            time.sleep(random.uniform(0.1, 0.3))
        
        # Signal that production is done by adding a sentinel value
        empty_slots.acquire()
        with buffer_mutex:
            buffer.append(None)
        filled_slots.release()
        
        print("Producer: finished producing items")
    
    def consumer() -> None:
        """Consumer function that removes items from the buffer and processes them."""
        nonlocal buffer, consumed_items
        
        while True:
            # Wait for a filled slot
            filled_slots.acquire()
            
            # Get an item from the buffer (critical section)
            with buffer_mutex:
                item = buffer.pop(0)
            
            # Signal that a slot is empty
            empty_slots.release()
            
            # Check for the sentinel value
            if item is None:
                print("Consumer: received shutdown signal")
                
                # Put the sentinel back for other consumers
                filled_slots.release()
                break
            
            print(f"Consumer: removed {item} from buffer")
            
            # Increment the consumed items counter
            consumed_items += 1
            
            # Simulate variable consumption time
            time.sleep(random.uniform(0.2, 0.5))
        
        print("Consumer: finished consuming items")
    
    # Create and start the producer and consumer threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for both threads to complete
    producer_thread.join()
    consumer_thread.join()
    
    # Verify that all items were consumed
    print(f"Consumed {consumed_items} items out of {num_items}")
    
    print("Producer-consumer with semaphores completed")


def producer_consumer_with_event() -> None:
    """Demonstrate producer-consumer pattern using events."""
    print("\n=== Producer-Consumer with Events ===")
    
    # Create events
    item_available = threading.Event()
    item_consumed = threading.Event()
    
    # Shared item
    shared_item: Dict[str, Any] = {'value': None, 'done': False}
    
    # Number of items to produce
    num_items = 10
    
    # Track consumed items
    consumed_items = 0
    
    def producer() -> None:
        """Producer function that generates items and signals their availability."""
        nonlocal shared_item
        
        for i in range(num_items):
            # Create an item
            item = f"Item-{i}"
            
            # Set the shared item
            shared_item['value'] = item
            print(f"Producer: produced {item}")
            
            # Signal that an item is available
            item_available.set()
            
            # Wait for the item to be consumed
            item_consumed.wait()
            item_consumed.clear()
            
            # Simulate variable production time
            time.sleep(random.uniform(0.1, 0.3))
        
        # Signal that production is done
        shared_item['done'] = True
        item_available.set()
        
        print("Producer: finished producing items")
    
    def consumer() -> None:
        """Consumer function that waits for items and processes them."""
        nonlocal shared_item, consumed_items
        
        while True:
            # Wait for an item to be available
            item_available.wait()
            item_available.clear()
            
            # Check if production is done
            if shared_item['done']:
                print("Consumer: received shutdown signal")
                break
            
            # Get the item
            item = shared_item['value']
            print(f"Consumer: consumed {item}")
            
            # Increment the consumed items counter
            consumed_items += 1
            
            # Simulate variable consumption time
            time.sleep(random.uniform(0.2, 0.5))
            
            # Signal that the item has been consumed
            item_consumed.set()
        
        print("Consumer: finished consuming items")
    
    # Create and start the producer and consumer threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for both threads to complete
    producer_thread.join()
    consumer_thread.join()
    
    # Verify that all items were consumed
    print(f"Consumed {consumed_items} items out of {num_items}")
    
    print("Producer-consumer with events completed")


def producer_consumer_with_futures() -> None:
    """Demonstrate producer-consumer pattern using concurrent.futures."""
    print("\n=== Producer-Consumer with Futures ===")
    
    # Create a queue
    task_queue = queue.Queue()
    
    # Number of items to produce
    num_items = 20
    
    # Number of consumers
    num_consumers = 3
    
    # Track consumed items
    consumed_items = 0
    consumed_lock = threading.Lock()
    
    # Flag to signal consumers to exit
    done = False
    
    def producer() -> None:
        """Producer function that generates items and puts them in the queue."""
        for i in range(num_items):
            # Create an item
            item = f"Item-{i}"
            
            # Put the item in the queue
            task_queue.put(item)
            print(f"Producer: produced {item} (queue size: {task_queue.qsize()})")
            
            # Simulate variable production time
            time.sleep(random.uniform(0.05, 0.2))
        
        print("Producer: finished producing items")
    
    def consumer() -> int:
        """
        Consumer function that gets items from the queue and processes them.
        
        Returns:
            Number of items consumed by this consumer.
        """
        items_consumed = 0
        
        while not done:
            try:
                # Try to get an item from the queue (non-blocking)
                item = task_queue.get(block=False)
                
                print(f"Consumer (Thread-{threading.current_thread().name}): consumed {item}")
                
                # Simulate variable consumption time
                time.sleep(random.uniform(0.1, 0.3))
                
                # Increment the consumed items counter
                items_consumed += 1
                
                # Mark the task as done
                task_queue.task_done()
            except queue.Empty:
                # Queue is empty, wait a bit and try again
                time.sleep(0.1)
        
        return items_consumed
    
    # Create and start the producer thread
    producer_thread = threading.Thread(target=producer)
    producer_thread.start()
    
    # Create a thread pool for consumers
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_consumers) as executor:
        # Submit consumer tasks
        future_to_consumer = {executor.submit(consumer): i for i in range(num_consumers)}
        
        # Wait for the producer to complete
        producer_thread.join()
        
        # Wait for all items to be processed
        task_queue.join()
        
        # Signal consumers to exit
        done = True
        
        # Wait for all consumers to complete and collect results
        for future in concurrent.futures.as_completed(future_to_consumer):
            consumer_id = future_to_consumer[future]
            try:
                items_consumed_by_consumer = future.result()
                consumed_items += items_consumed_by_consumer
                print(f"Consumer {consumer_id} consumed {items_consumed_by_consumer} items")
            except Exception as e:
                print(f"Consumer {consumer_id} generated an exception: {e}")
    
    # Verify that all items were consumed
    print(f"Consumed {consumed_items} items out of {num_items}")
    
    print("Producer-consumer with futures completed")


def run_demo() -> None:
    """Run all producer-consumer examples."""
    print("=== Producer-Consumer Pattern Examples ===")
    
    basic_producer_consumer()
    multiple_producers_consumers()
    producer_consumer_with_condition()
    producer_consumer_with_semaphores()
    producer_consumer_with_event()
    producer_consumer_with_futures()
    
    print("\nAll producer-consumer examples completed")


if __name__ == "__main__":
    run_demo() 