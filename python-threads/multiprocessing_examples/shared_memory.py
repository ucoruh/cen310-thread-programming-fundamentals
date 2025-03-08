"""
Shared memory examples for multiprocessing.

This module demonstrates various ways to share memory between processes in Python.
"""

import multiprocessing as mp
import time
import random
import os
import sys
import array
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from multiprocessing import shared_memory


def shared_value_example() -> None:
    """Demonstrate sharing a single value between processes using Value."""
    print("\n=== Shared Value Example ===")
    
    # Create a shared value
    counter = mp.Value('i', 0)  # 'i' is the typecode for integer
    
    def increment_counter(name: str, num_increments: int) -> None:
        """
        Increment the shared counter.
        
        Args:
            name: Process name.
            num_increments: Number of increments to perform.
        """
        print(f"Process {name}: starting (PID: {os.getpid()})")
        
        for i in range(num_increments):
            # Acquire the lock associated with the shared value
            with counter.get_lock():
                counter.value += 1
            
            # Simulate some work
            time.sleep(random.uniform(0.001, 0.005))
        
        print(f"Process {name}: finished {num_increments} increments")
    
    # Create processes
    processes = []
    num_processes = 4
    increments_per_process = 25
    
    for i in range(num_processes):
        process = mp.Process(
            target=increment_counter, 
            args=(f"{i}", increments_per_process)
        )
        processes.append(process)
        process.start()
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    # Check the final counter value
    expected_count = num_processes * increments_per_process
    print(f"Final counter value: {counter.value}")
    print(f"Expected counter value: {expected_count}")
    print(f"Counter is {'correct' if counter.value == expected_count else 'incorrect'}")


def shared_array_example() -> None:
    """Demonstrate sharing an array between processes using Array."""
    print("\n=== Shared Array Example ===")
    
    # Create a shared array
    shared_arr = mp.Array('i', 10)  # 'i' is the typecode for integer, 10 is the size
    
    def modify_array(name: str, start_idx: int, end_idx: int) -> None:
        """
        Modify a portion of the shared array.
        
        Args:
            name: Process name.
            start_idx: Starting index to modify.
            end_idx: Ending index to modify (exclusive).
        """
        print(f"Process {name}: starting (PID: {os.getpid()})")
        
        # Acquire the lock associated with the shared array
        with shared_arr.get_lock():
            for i in range(start_idx, end_idx):
                shared_arr[i] = i * 10
                time.sleep(0.01)  # Simulate some work
        
        print(f"Process {name}: finished modifying indices {start_idx}-{end_idx-1}")
    
    # Initialize the array
    for i in range(len(shared_arr)):
        shared_arr[i] = 0
    
    print(f"Initial array: {list(shared_arr)}")
    
    # Create processes to modify different parts of the array
    processes = []
    
    process1 = mp.Process(target=modify_array, args=("A", 0, 5))
    process2 = mp.Process(target=modify_array, args=("B", 5, 10))
    
    processes.append(process1)
    processes.append(process2)
    
    # Start processes
    for process in processes:
        process.start()
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    # Check the final array
    print(f"Final array: {list(shared_arr)}")


def shared_dict_list_example() -> None:
    """Demonstrate sharing dictionaries and lists between processes using Manager."""
    print("\n=== Shared Dictionary and List Example ===")
    
    # Create a manager
    with mp.Manager() as manager:
        # Create shared dictionary and list
        shared_dict = manager.dict()
        shared_list = manager.list()
        
        def update_shared_objects(name: str, start_val: int, end_val: int) -> None:
            """
            Update the shared dictionary and list.
            
            Args:
                name: Process name.
                start_val: Starting value.
                end_val: Ending value (exclusive).
            """
            print(f"Process {name}: starting (PID: {os.getpid()})")
            
            for i in range(start_val, end_val):
                # Update the shared dictionary
                key = f"key_{i}"
                shared_dict[key] = i * 10
                
                # Update the shared list
                shared_list.append(i)
                
                # Simulate some work
                time.sleep(random.uniform(0.01, 0.05))
            
            print(f"Process {name}: finished updating shared objects")
        
        # Create processes
        processes = []
        
        process1 = mp.Process(target=update_shared_objects, args=("A", 0, 5))
        process2 = mp.Process(target=update_shared_objects, args=("B", 5, 10))
        
        processes.append(process1)
        processes.append(process2)
        
        # Start processes
        for process in processes:
            process.start()
        
        # Wait for all processes to complete
        for process in processes:
            process.join()
        
        # Check the final shared objects
        print(f"Final shared dictionary: {dict(shared_dict)}")
        print(f"Final shared list: {list(shared_list)}")


def shared_memory_numpy_example() -> None:
    """Demonstrate using the shared_memory module with NumPy arrays."""
    print("\n=== Shared Memory with NumPy Example ===")
    
    # Create a NumPy array
    original_array = np.array([1, 1, 2, 3, 5, 8, 13, 21, 34, 55], dtype=np.int64)
    
    # Create a shared memory block
    shm = shared_memory.SharedMemory(create=True, size=original_array.nbytes)
    
    # Create a NumPy array that uses the shared memory
    shared_array = np.ndarray(
        original_array.shape, 
        dtype=original_array.dtype, 
        buffer=shm.buf
    )
    
    # Copy the original data into the shared array
    shared_array[:] = original_array[:]
    
    print(f"Original array: {original_array}")
    print(f"Shared array: {shared_array}")
    
    def modify_shared_array(name: str, shm_name: str, indices: List[int], multiplier: int) -> None:
        """
        Modify specific indices in the shared array.
        
        Args:
            name: Process name.
            shm_name: Name of the shared memory block.
            indices: Indices to modify.
            multiplier: Value to multiply the elements by.
        """
        print(f"Process {name}: starting (PID: {os.getpid()})")
        
        # Attach to the existing shared memory block
        existing_shm = shared_memory.SharedMemory(name=shm_name)
        
        # Create a NumPy array using the shared memory
        array = np.ndarray(
            original_array.shape, 
            dtype=original_array.dtype, 
            buffer=existing_shm.buf
        )
        
        # Modify the array
        for idx in indices:
            array[idx] *= multiplier
            time.sleep(0.05)  # Simulate some work
        
        print(f"Process {name}: modified indices {indices}")
        
        # Clean up
        existing_shm.close()
    
    # Create processes to modify different parts of the array
    processes = []
    
    process1 = mp.Process(
        target=modify_shared_array, 
        args=("A", shm.name, [0, 2, 4, 6, 8], 10)
    )
    
    process2 = mp.Process(
        target=modify_shared_array, 
        args=("B", shm.name, [1, 3, 5, 7, 9], 100)
    )
    
    processes.append(process1)
    processes.append(process2)
    
    # Start processes
    for process in processes:
        process.start()
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    # Check the modified array
    print(f"Modified shared array: {shared_array}")
    
    # Clean up
    shm.close()
    shm.unlink()  # Free and remove the shared memory block


def shared_memory_raw_example() -> None:
    """Demonstrate using the shared_memory module with raw bytes."""
    print("\n=== Shared Memory with Raw Bytes Example ===")
    
    # Create a shared memory block
    shm = shared_memory.SharedMemory(create=True, size=100)
    
    # Write some data to the shared memory
    data = b"Hello, shared memory!"
    shm.buf[:len(data)] = data
    
    print(f"Data written to shared memory: {bytes(shm.buf[:len(data)])}")
    
    def read_and_modify_memory(name: str, shm_name: str, offset: int, new_data: bytes) -> None:
        """
        Read and modify the shared memory.
        
        Args:
            name: Process name.
            shm_name: Name of the shared memory block.
            offset: Offset in the shared memory to modify.
            new_data: New data to write.
        """
        print(f"Process {name}: starting (PID: {os.getpid()})")
        
        # Attach to the existing shared memory block
        existing_shm = shared_memory.SharedMemory(name=shm_name)
        
        # Read the current data
        current_data = bytes(existing_shm.buf[:len(data)])
        print(f"Process {name}: read data: {current_data}")
        
        # Modify the data
        existing_shm.buf[offset:offset+len(new_data)] = new_data
        
        print(f"Process {name}: modified data at offset {offset}")
        
        # Clean up
        existing_shm.close()
    
    # Create processes to read and modify the shared memory
    processes = []
    
    process1 = mp.Process(
        target=read_and_modify_memory, 
        args=("A", shm.name, 7, b"wonderful")
    )
    
    processes.append(process1)
    
    # Start processes
    for process in processes:
        process.start()
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    # Check the modified data
    modified_data = bytes(shm.buf[:20])
    print(f"Modified data in shared memory: {modified_data}")
    
    # Clean up
    shm.close()
    shm.unlink()  # Free and remove the shared memory block


def shared_memory_array_example() -> None:
    """Demonstrate using the shared_memory module with array.array."""
    print("\n=== Shared Memory with array.array Example ===")
    
    # Create an array
    arr = array.array('i', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    # Create a shared memory block
    shm = shared_memory.SharedMemory(create=True, size=arr.buffer_info()[1])
    
    # Copy the array data to the shared memory
    shm.buf[:arr.buffer_info()[1]] = arr.tobytes()
    
    print(f"Original array: {arr}")
    
    def modify_array_in_shared_memory(name: str, shm_name: str, indices: List[int], value: int) -> None:
        """
        Modify specific indices in the shared array.
        
        Args:
            name: Process name.
            shm_name: Name of the shared memory block.
            indices: Indices to modify.
            value: Value to set.
        """
        print(f"Process {name}: starting (PID: {os.getpid()})")
        
        # Attach to the existing shared memory block
        existing_shm = shared_memory.SharedMemory(name=shm_name)
        
        # Create an array from the shared memory
        shared_arr = array.array('i')
        shared_arr.frombytes(existing_shm.buf[:arr.buffer_info()[1]])
        
        # Modify the array
        for idx in indices:
            shared_arr[idx] = value
            time.sleep(0.05)  # Simulate some work
        
        # Copy the modified array back to shared memory
        existing_shm.buf[:arr.buffer_info()[1]] = shared_arr.tobytes()
        
        print(f"Process {name}: modified indices {indices}")
        
        # Clean up
        existing_shm.close()
    
    # Create processes to modify different parts of the array
    processes = []
    
    process1 = mp.Process(
        target=modify_array_in_shared_memory, 
        args=("A", shm.name, [0, 2, 4, 6, 8], 100)
    )
    
    process2 = mp.Process(
        target=modify_array_in_shared_memory, 
        args=("B", shm.name, [1, 3, 5, 7, 9], 200)
    )
    
    processes.append(process1)
    processes.append(process2)
    
    # Start processes
    for process in processes:
        process.start()
    
    # Wait for all processes to complete
    for process in processes:
        process.join()
    
    # Read the modified array from shared memory
    modified_arr = array.array('i')
    modified_arr.frombytes(shm.buf[:arr.buffer_info()[1]])
    
    print(f"Modified array: {modified_arr}")
    
    # Clean up
    shm.close()
    shm.unlink()  # Free and remove the shared memory block


def run_demo() -> None:
    """Run all shared memory examples."""
    print("=== Shared Memory Examples ===")
    
    shared_value_example()
    shared_array_example()
    shared_dict_list_example()
    
    # The shared_memory module was introduced in Python 3.8
    if sys.version_info >= (3, 8):
        shared_memory_numpy_example()
        shared_memory_raw_example()
        shared_memory_array_example()
    else:
        print("\nSkipping shared_memory examples (requires Python 3.8+)")
    
    print("\nAll shared memory examples completed")


if __name__ == "__main__":
    run_demo() 