"""
Basic asyncio examples demonstrating asynchronous programming in Python.

This module shows how to use asyncio for asynchronous programming.
"""

import asyncio
import time
import random
from typing import List, Dict, Any, Optional, Tuple, Callable


async def simple_coroutine() -> str:
    """
    A simple coroutine that returns a string after a delay.
    
    Returns:
        A greeting string.
    """
    print("Simple coroutine: starting")
    await asyncio.sleep(1)
    print("Simple coroutine: finished")
    return "Hello from coroutine!"


async def basic_coroutine_example() -> None:
    """Demonstrate basic coroutine creation and execution."""
    print("\n=== Basic Coroutine Example ===")
    
    # Create and run a coroutine
    result = await simple_coroutine()
    print(f"Result: {result}")


async def multiple_coroutines_example() -> None:
    """Demonstrate running multiple coroutines concurrently."""
    print("\n=== Multiple Coroutines Example ===")
    
    async def task_coroutine(name: str, delay: float) -> str:
        """
        A coroutine that simulates a task with a delay.
        
        Args:
            name: Task name.
            delay: Delay in seconds.
            
        Returns:
            A string with the task result.
        """
        print(f"Task {name}: starting")
        await asyncio.sleep(delay)
        print(f"Task {name}: finished after {delay:.2f}s")
        return f"Result from task {name}"
    
    # Create tasks
    task1 = asyncio.create_task(task_coroutine("A", 2.0))
    task2 = asyncio.create_task(task_coroutine("B", 1.0))
    task3 = asyncio.create_task(task_coroutine("C", 1.5))
    
    # Wait for all tasks to complete
    print("Waiting for all tasks to complete...")
    start_time = time.time()
    
    results = await asyncio.gather(task1, task2, task3)
    
    end_time = time.time()
    print(f"All tasks completed in {end_time - start_time:.2f}s")
    
    # Print results
    for i, result in enumerate(results):
        print(f"Result {i+1}: {result}")


async def task_cancellation_example() -> None:
    """Demonstrate task cancellation."""
    print("\n=== Task Cancellation Example ===")
    
    async def long_running_task() -> None:
        """A long-running task that can be cancelled."""
        try:
            print("Long-running task: starting")
            for i in range(10):
                print(f"Long-running task: working... ({i+1}/10)")
                await asyncio.sleep(0.5)
            print("Long-running task: finished")
        except asyncio.CancelledError:
            print("Long-running task: cancelled!")
            raise  # Re-raise the exception
    
    # Create a task
    task = asyncio.create_task(long_running_task())
    
    # Let it run for a bit
    await asyncio.sleep(2)
    
    # Cancel the task
    print("Main: cancelling the task")
    task.cancel()
    
    try:
        # Wait for the task to be cancelled
        await task
    except asyncio.CancelledError:
        print("Main: task was cancelled successfully")


async def timeout_example() -> None:
    """Demonstrate using timeouts with asyncio."""
    print("\n=== Timeout Example ===")
    
    async def slow_operation() -> str:
        """A slow operation that takes longer than the timeout."""
        print("Slow operation: starting")
        await asyncio.sleep(3)
        print("Slow operation: finished")
        return "Result from slow operation"
    
    # Try to run the operation with a timeout
    print("Running slow operation with a 1-second timeout...")
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")
    
    # Try with a longer timeout
    print("\nRunning slow operation with a 5-second timeout...")
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=5.0)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")


async def shield_example() -> None:
    """Demonstrate using shield to protect a coroutine from cancellation."""
    print("\n=== Shield Example ===")
    
    async def important_operation() -> str:
        """An important operation that shouldn't be interrupted."""
        print("Important operation: starting")
        try:
            for i in range(5):
                print(f"Important operation: working... ({i+1}/5)")
                await asyncio.sleep(0.5)
            print("Important operation: finished")
            return "Result from important operation"
        except asyncio.CancelledError:
            print("Important operation: cancel request received but ignored")
            # Continue execution instead of propagating the cancellation
            for i in range(5, 10):
                print(f"Important operation: working... ({i+1}/10)")
                await asyncio.sleep(0.5)
            print("Important operation: finished after cancellation attempt")
            return "Result from important operation (completed despite cancellation)"
    
    # Create a shielded task
    shielded_task = asyncio.shield(important_operation())
    
    # Let it run for a bit
    await asyncio.sleep(1.5)
    
    # Try to cancel the operation
    print("Main: attempting to cancel the operation")
    try:
        # This will cancel the shield, but not the underlying coroutine
        shielded_task.cancel()
        await shielded_task
    except asyncio.CancelledError:
        print("Main: shield was cancelled, but the operation continues")
        # The operation is still running, we can get its result by creating a new task
        new_task = asyncio.create_task(important_operation())
        result = await new_task
        print(f"Main: operation completed with result: {result}")


async def gather_example() -> None:
    """Demonstrate using gather to run multiple coroutines concurrently."""
    print("\n=== Gather Example ===")
    
    async def fetch_data(name: str, delay: float) -> Dict[str, Any]:
        """
        Simulate fetching data from a source.
        
        Args:
            name: Data source name.
            delay: Delay in seconds.
            
        Returns:
            A dictionary with the fetched data.
        """
        print(f"Fetching data from {name}...")
        await asyncio.sleep(delay)
        return {
            "source": name,
            "timestamp": time.time(),
            "value": random.randint(1, 100)
        }
    
    # Fetch data from multiple sources concurrently
    print("Fetching data from multiple sources...")
    start_time = time.time()
    
    results = await asyncio.gather(
        fetch_data("API 1", 2.0),
        fetch_data("API 2", 1.0),
        fetch_data("API 3", 3.0),
        fetch_data("Database", 2.5)
    )
    
    end_time = time.time()
    print(f"All data fetched in {end_time - start_time:.2f}s")
    
    # Print results
    for result in results:
        print(f"Data from {result['source']}: {result['value']}")


async def wait_example() -> None:
    """Demonstrate using wait to wait for multiple coroutines with more control."""
    print("\n=== Wait Example ===")
    
    async def process_item(item: int) -> Tuple[int, int]:
        """
        Process an item asynchronously.
        
        Args:
            item: Item to process.
            
        Returns:
            Tuple containing (item, result).
        """
        delay = random.uniform(0.5, 3.0)
        print(f"Processing item {item} (will take {delay:.2f}s)...")
        await asyncio.sleep(delay)
        result = item * item
        print(f"Finished processing item {item}")
        return (item, result)
    
    # Create tasks
    tasks = [
        asyncio.create_task(process_item(i)) for i in range(1, 6)
    ]
    
    # Wait for some tasks to complete
    print("Waiting for the first 3 tasks to complete...")
    start_time = time.time()
    
    done, pending = await asyncio.wait(
        tasks, 
        return_when=asyncio.FIRST_COMPLETED,
        timeout=2.0
    )
    
    end_time = time.time()
    print(f"Wait completed in {end_time - start_time:.2f}s")
    
    # Process completed tasks
    print(f"{len(done)} tasks completed, {len(pending)} tasks pending")
    
    for task in done:
        item, result = task.result()
        print(f"Result for item {item}: {result}")
    
    # Wait for all remaining tasks
    if pending:
        print("\nWaiting for all remaining tasks...")
        done, pending = await asyncio.wait(pending)
        
        for task in done:
            item, result = task.result()
            print(f"Result for item {item}: {result}")


async def as_completed_example() -> None:
    """Demonstrate using as_completed to process results as they complete."""
    print("\n=== As Completed Example ===")
    
    async def fetch_url(url: str) -> Tuple[str, str]:
        """
        Simulate fetching a URL.
        
        Args:
            url: URL to fetch.
            
        Returns:
            Tuple containing (url, content).
        """
        delay = random.uniform(1.0, 5.0)
        print(f"Fetching {url} (will take {delay:.2f}s)...")
        await asyncio.sleep(delay)
        content = f"Content from {url}"
        return (url, content)
    
    # URLs to fetch
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5"
    ]
    
    # Create tasks
    tasks = [
        asyncio.create_task(fetch_url(url)) for url in urls
    ]
    
    # Process results as they complete
    print("Processing results as they complete...")
    
    for i, future in enumerate(asyncio.as_completed(tasks), 1):
        url, content = await future
        print(f"Result {i}: {url} -> {content}")


async def error_handling_example() -> None:
    """Demonstrate error handling in asyncio."""
    print("\n=== Error Handling Example ===")
    
    async def might_fail(name: str, should_fail: bool) -> str:
        """
        A coroutine that might fail.
        
        Args:
            name: Coroutine name.
            should_fail: Whether the coroutine should fail.
            
        Returns:
            A success message.
            
        Raises:
            ValueError: If should_fail is True.
        """
        print(f"Coroutine {name}: starting")
        await asyncio.sleep(1)
        
        if should_fail:
            print(f"Coroutine {name}: failing")
            raise ValueError(f"Deliberate error in coroutine {name}")
        
        print(f"Coroutine {name}: succeeding")
        return f"Success from coroutine {name}"
    
    # Handle errors in a single coroutine
    print("Running a coroutine that will fail...")
    try:
        result = await might_fail("A", True)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Caught error: {e}")
    
    # Handle errors with gather
    print("\nRunning multiple coroutines with gather...")
    results = await asyncio.gather(
        might_fail("B", False),
        might_fail("C", True),
        might_fail("D", False),
        return_exceptions=True  # Important: return exceptions instead of raising them
    )
    
    # Process results and exceptions
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i+1} failed with error: {result}")
        else:
            print(f"Task {i+1} succeeded with result: {result}")


async def run_demo() -> None:
    """Run all asyncio examples."""
    print("=== Basic Asyncio Examples ===")
    
    await basic_coroutine_example()
    await multiple_coroutines_example()
    await task_cancellation_example()
    await timeout_example()
    await shield_example()
    await gather_example()
    await wait_example()
    await as_completed_example()
    await error_handling_example()
    
    print("\nAll asyncio examples completed")


if __name__ == "__main__":
    asyncio.run(run_demo()) 