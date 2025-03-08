"""
Thread communication examples demonstrating various ways threads can communicate.

This module shows different mechanisms for communication between threads in Python.
"""

import threading
import queue
import time
import random
from typing import List, Dict, Any, Optional, Tuple, Set


def shared_memory_communication() -> None:
    """Demonstrate communication through shared memory."""
    print("\n=== Shared Memory Communication ===")
    
    # Shared data
    shared_data: Dict[str, Any] = {
        'counter': 0,
        'message': '',
        'is_done': False
    }
    
    # Lock to protect shared data
    data_lock = threading.Lock()
    
    def writer() -> None:
        """Writer thread that updates shared data."""
        nonlocal shared_data
        
        for i in range(5):
            # Simulate some work
            time.sleep(random.uniform(0.1, 0.3))
            
            # Update shared data
            with data_lock:
                shared_data['counter'] += 1
                shared_data['message'] = f"Message {i+1}"
                print(f"Writer: updated counter to {shared_data['counter']} and message to '{shared_data['message']}'")
        
        # Signal that we're done
        with data_lock:
            shared_data['is_done'] = True
            print("Writer: signaled completion")
    
    def reader() -> None:
        """Reader thread that reads shared data."""
        while True:
            # Read shared data
            with data_lock:
                counter = shared_data['counter']
                message = shared_data['message']
                is_done = shared_data['is_done']
            
            print(f"Reader: read counter={counter}, message='{message}'")
            
            # Check if we're done
            if is_done and counter == 5:
                print("Reader: detected completion signal")
                break
            
            # Simulate some work
            time.sleep(random.uniform(0.2, 0.5))
    
    # Create threads
    writer_thread = threading.Thread(target=writer)
    reader_thread = threading.Thread(target=reader)
    
    # Start threads
    writer_thread.start()
    reader_thread.start()
    
    # Wait for threads to complete
    writer_thread.join()
    reader_thread.join()
    
    print("Shared memory communication completed")


def queue_communication() -> None:
    """Demonstrate communication through a queue."""
    print("\n=== Queue Communication ===")
    
    # Create a queue
    message_queue: queue.Queue = queue.Queue()
    
    def producer() -> None:
        """Producer thread that puts messages in the queue."""
        for i in range(5):
            # Simulate some work
            time.sleep(random.uniform(0.1, 0.3))
            
            # Put a message in the queue
            message = f"Message {i+1}"
            message_queue.put(message)
            print(f"Producer: put '{message}' in the queue")
        
        # Signal that we're done
        message_queue.put(None)
        print("Producer: signaled completion")
    
    def consumer() -> None:
        """Consumer thread that gets messages from the queue."""
        while True:
            # Get a message from the queue (blocks until a message is available)
            message = message_queue.get()
            
            # Check if we're done
            if message is None:
                print("Consumer: received completion signal")
                message_queue.task_done()
                break
            
            print(f"Consumer: got '{message}' from the queue")
            
            # Simulate processing the message
            time.sleep(random.uniform(0.2, 0.5))
            
            # Mark the task as done
            message_queue.task_done()
    
    # Create threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    # Start threads
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for threads to complete
    producer_thread.join()
    consumer_thread.join()
    
    # Wait for the queue to be fully processed
    message_queue.join()
    
    print("Queue communication completed")


def multiple_producer_consumer() -> None:
    """Demonstrate multiple producers and consumers with a queue."""
    print("\n=== Multiple Producer-Consumer Example ===")
    
    # Create a queue
    task_queue: queue.Queue = queue.Queue()
    
    # Number of tasks, producers, and consumers
    num_tasks = 20
    num_producers = 3
    num_consumers = 2
    
    # Sentinel value to signal consumers to exit
    SENTINEL = object()
    
    # Track completed tasks
    completed_tasks: Set[int] = set()
    completed_lock = threading.Lock()
    
    def producer(producer_id: int, num_tasks_per_producer: int) -> None:
        """
        Producer thread that puts tasks in the queue.
        
        Args:
            producer_id: Producer identifier.
            num_tasks_per_producer: Number of tasks to produce.
        """
        for i in range(num_tasks_per_producer):
            # Simulate some work
            time.sleep(random.uniform(0.05, 0.2))
            
            # Create a task
            task_id = producer_id * 100 + i
            task = (task_id, random.randint(1, 10))
            
            # Put the task in the queue
            task_queue.put(task)
            print(f"Producer {producer_id}: put task {task_id} in the queue")
    
    def consumer(consumer_id: int) -> None:
        """
        Consumer thread that gets tasks from the queue.
        
        Args:
            consumer_id: Consumer identifier.
        """
        while True:
            # Get a task from the queue
            task = task_queue.get()
            
            # Check if we're done
            if task is SENTINEL:
                print(f"Consumer {consumer_id}: received sentinel, exiting")
                task_queue.task_done()
                break
            
            # Process the task
            task_id, value = task
            print(f"Consumer {consumer_id}: processing task {task_id} with value {value}")
            
            # Simulate processing
            time.sleep(value * 0.1)
            
            # Mark the task as completed
            with completed_lock:
                completed_tasks.add(task_id)
            
            print(f"Consumer {consumer_id}: completed task {task_id}")
            
            # Mark the task as done in the queue
            task_queue.task_done()
    
    # Create and start producer threads
    producer_threads = []
    tasks_per_producer = num_tasks // num_producers
    
    for i in range(num_producers):
        thread = threading.Thread(target=producer, args=(i, tasks_per_producer))
        producer_threads.append(thread)
        thread.start()
    
    # Create and start consumer threads
    consumer_threads = []
    
    for i in range(num_consumers):
        thread = threading.Thread(target=consumer, args=(i,))
        consumer_threads.append(thread)
        thread.start()
    
    # Wait for all producers to complete
    for thread in producer_threads:
        thread.join()
    
    # Wait for all tasks to be processed
    task_queue.join()
    
    # Signal consumers to exit
    for _ in range(num_consumers):
        task_queue.put(SENTINEL)
    
    # Wait for all consumers to complete
    for thread in consumer_threads:
        thread.join()
    
    # Verify all tasks were completed
    print(f"Completed {len(completed_tasks)} tasks out of {num_tasks}")
    
    print("Multiple producer-consumer example completed")


def event_based_communication() -> None:
    """Demonstrate communication using events."""
    print("\n=== Event-Based Communication ===")
    
    # Create events
    data_ready = threading.Event()
    data_processed = threading.Event()
    
    # Shared data
    shared_data: Dict[str, Any] = {'value': None}
    
    def sender() -> None:
        """Sender thread that sets data and signals it's ready."""
        for i in range(5):
            # Prepare data
            value = f"Data {i+1}"
            shared_data['value'] = value
            print(f"Sender: prepared '{value}'")
            
            # Signal that data is ready
            print("Sender: signaling data is ready")
            data_ready.set()
            
            # Wait for data to be processed
            print("Sender: waiting for data to be processed")
            data_processed.wait()
            data_processed.clear()
            
            print("Sender: data has been processed")
            
            # Simulate some work
            time.sleep(random.uniform(0.1, 0.3))
    
    def receiver() -> None:
        """Receiver thread that waits for data and processes it."""
        for i in range(5):
            # Wait for data to be ready
            print("Receiver: waiting for data")
            data_ready.wait()
            data_ready.clear()
            
            # Process data
            value = shared_data['value']
            print(f"Receiver: received '{value}'")
            
            # Simulate processing
            time.sleep(random.uniform(0.2, 0.5))
            
            # Signal that data has been processed
            print("Receiver: signaling data has been processed")
            data_processed.set()
    
    # Create threads
    sender_thread = threading.Thread(target=sender)
    receiver_thread = threading.Thread(target=receiver)
    
    # Start threads
    sender_thread.start()
    receiver_thread.start()
    
    # Wait for threads to complete
    sender_thread.join()
    receiver_thread.join()
    
    print("Event-based communication completed")


def condition_based_communication() -> None:
    """Demonstrate communication using conditions."""
    print("\n=== Condition-Based Communication ===")
    
    # Create a condition
    condition = threading.Condition()
    
    # Shared buffer
    buffer: List[str] = []
    max_buffer_size = 3
    
    def producer() -> None:
        """Producer thread that adds items to the buffer."""
        for i in range(10):
            # Acquire the condition
            with condition:
                # Wait while the buffer is full
                while len(buffer) >= max_buffer_size:
                    print("Producer: buffer full, waiting...")
                    condition.wait()
                
                # Add an item to the buffer
                item = f"Item {i+1}"
                buffer.append(item)
                print(f"Producer: added '{item}' to buffer, size now {len(buffer)}")
                
                # Notify consumers
                condition.notify()
            
            # Simulate some work
            time.sleep(random.uniform(0.1, 0.3))
    
    def consumer() -> None:
        """Consumer thread that removes items from the buffer."""
        items_consumed = 0
        
        while items_consumed < 10:
            # Acquire the condition
            with condition:
                # Wait while the buffer is empty
                while not buffer:
                    print("Consumer: buffer empty, waiting...")
                    condition.wait()
                
                # Remove an item from the buffer
                item = buffer.pop(0)
                items_consumed += 1
                print(f"Consumer: removed '{item}' from buffer, size now {len(buffer)}")
                
                # Notify producers
                condition.notify()
            
            # Simulate processing
            time.sleep(random.uniform(0.2, 0.5))
    
    # Create threads
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    # Start threads
    producer_thread.start()
    consumer_thread.start()
    
    # Wait for threads to complete
    producer_thread.join()
    consumer_thread.join()
    
    print("Condition-based communication completed")


def pipe_communication() -> None:
    """Demonstrate communication using a pipe (simulated with a queue)."""
    print("\n=== Pipe Communication ===")
    
    # Create a pipe (simulated with a queue)
    pipe_queue: queue.Queue = queue.Queue()
    
    def sender() -> None:
        """Sender thread that sends messages through the pipe."""
        for i in range(5):
            # Prepare message
            message = f"Message {i+1}"
            
            # Send message
            pipe_queue.put(message)
            print(f"Sender: sent '{message}' through the pipe")
            
            # Simulate some work
            time.sleep(random.uniform(0.1, 0.3))
        
        # Signal end of messages
        pipe_queue.put(None)
        print("Sender: sent end-of-messages signal")
    
    def receiver() -> None:
        """Receiver thread that receives messages from the pipe."""
        while True:
            # Receive message
            message = pipe_queue.get()
            
            # Check for end of messages
            if message is None:
                print("Receiver: received end-of-messages signal")
                break
            
            print(f"Receiver: received '{message}' from the pipe")
            
            # Simulate processing
            time.sleep(random.uniform(0.2, 0.5))
    
    # Create threads
    sender_thread = threading.Thread(target=sender)
    receiver_thread = threading.Thread(target=receiver)
    
    # Start threads
    sender_thread.start()
    receiver_thread.start()
    
    # Wait for threads to complete
    sender_thread.join()
    receiver_thread.join()
    
    print("Pipe communication completed")


def run_demo() -> None:
    """Run all thread communication examples."""
    print("=== Thread Communication Examples ===")
    
    shared_memory_communication()
    queue_communication()
    multiple_producer_consumer()
    event_based_communication()
    condition_based_communication()
    pipe_communication()
    
    print("\nAll thread communication examples completed")


if __name__ == "__main__":
    run_demo() 