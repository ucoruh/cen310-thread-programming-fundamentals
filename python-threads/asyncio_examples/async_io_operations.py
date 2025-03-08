"""
Asynchronous I/O operations examples using asyncio.

This module demonstrates how to perform asynchronous I/O operations with asyncio.
"""

import asyncio
import aiofiles
import aiohttp
import time
import os
import random
import tempfile
from typing import List, Dict, Any, Optional, Tuple, BinaryIO


async def async_file_read_write_example() -> None:
    """Demonstrate asynchronous file reading and writing."""
    print("\n=== Asynchronous File Read/Write Example ===")
    
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_path = temp_file.name
    temp_file.close()
    
    print(f"Using temporary file: {temp_file_path}")
    
    # Write to the file asynchronously
    print("Writing to file asynchronously...")
    async with aiofiles.open(temp_file_path, 'w') as file:
        for i in range(10):
            line = f"Line {i+1}: This is some test data.\n"
            await file.write(line)
            # Simulate some processing between writes
            await asyncio.sleep(0.1)
    
    # Read from the file asynchronously
    print("Reading from file asynchronously...")
    async with aiofiles.open(temp_file_path, 'r') as file:
        content = await file.read()
    
    print(f"Read {len(content)} characters from file")
    print("First few lines:")
    print('\n'.join(content.splitlines()[:3]))
    
    # Clean up
    os.unlink(temp_file_path)
    print(f"Deleted temporary file: {temp_file_path}")


async def async_http_requests_example() -> None:
    """Demonstrate asynchronous HTTP requests."""
    print("\n=== Asynchronous HTTP Requests Example ===")
    
    async def fetch_url(session: aiohttp.ClientSession, url: str) -> Tuple[str, int, float]:
        """
        Fetch a URL asynchronously.
        
        Args:
            session: aiohttp client session.
            url: URL to fetch.
            
        Returns:
            Tuple containing (url, status code, elapsed time).
        """
        start_time = time.time()
        
        print(f"Fetching {url}...")
        async with session.get(url) as response:
            await response.text()
            elapsed = time.time() - start_time
            return (url, response.status, elapsed)
    
    # URLs to fetch
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/3"
    ]
    
    # Sequential fetching
    print("\nFetching URLs sequentially:")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        results = []
        for url in urls:
            result = await fetch_url(session, url)
            results.append(result)
    
    end_time = time.time()
    sequential_time = end_time - start_time
    print(f"Sequential fetching completed in {sequential_time:.2f}s")
    
    for url, status, elapsed in results:
        print(f"URL: {url}, Status: {status}, Time: {elapsed:.2f}s")
    
    # Concurrent fetching
    print("\nFetching URLs concurrently:")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    concurrent_time = end_time - start_time
    print(f"Concurrent fetching completed in {concurrent_time:.2f}s")
    
    for url, status, elapsed in results:
        print(f"URL: {url}, Status: {status}, Time: {elapsed:.2f}s")
    
    # Calculate speedup
    speedup = sequential_time / concurrent_time
    print(f"Speedup: {speedup:.2f}x")


async def async_streaming_example() -> None:
    """Demonstrate asynchronous streaming of data."""
    print("\n=== Asynchronous Streaming Example ===")
    
    # Create a temporary file for streaming
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_path = temp_file.name
    temp_file.close()
    
    print(f"Using temporary file: {temp_file_path}")
    
    # Generate some random data
    data_size = 1024 * 1024  # 1 MB
    chunk_size = 4096  # 4 KB
    
    # Write data in chunks asynchronously
    print(f"Writing {data_size / 1024:.0f} KB of data in {chunk_size / 1024:.0f} KB chunks...")
    async with aiofiles.open(temp_file_path, 'wb') as file:
        bytes_written = 0
        while bytes_written < data_size:
            # Generate a random chunk of data
            chunk_size_actual = min(chunk_size, data_size - bytes_written)
            chunk = os.urandom(chunk_size_actual)
            
            # Write the chunk
            await file.write(chunk)
            bytes_written += len(chunk)
            
            # Report progress
            if bytes_written % (chunk_size * 64) == 0 or bytes_written == data_size:
                print(f"Progress: {bytes_written / 1024:.0f} KB / {data_size / 1024:.0f} KB "
                      f"({bytes_written / data_size * 100:.1f}%)")
            
            # Simulate some processing between writes
            await asyncio.sleep(0.001)
    
    # Read data in chunks asynchronously
    print("\nReading data in chunks...")
    async with aiofiles.open(temp_file_path, 'rb') as file:
        bytes_read = 0
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            
            bytes_read += len(chunk)
            
            # Report progress
            if bytes_read % (chunk_size * 64) == 0 or bytes_read == data_size:
                print(f"Progress: {bytes_read / 1024:.0f} KB / {data_size / 1024:.0f} KB "
                      f"({bytes_read / data_size * 100:.1f}%)")
            
            # Simulate some processing between reads
            await asyncio.sleep(0.001)
    
    print(f"Read {bytes_read / 1024:.0f} KB of data")
    
    # Clean up
    os.unlink(temp_file_path)
    print(f"Deleted temporary file: {temp_file_path}")


async def async_subprocess_example() -> None:
    """Demonstrate asynchronous subprocess execution."""
    print("\n=== Asynchronous Subprocess Example ===")
    
    # Define commands to run
    if os.name == 'nt':  # Windows
        commands = [
            'dir',
            'echo Hello from subprocess!',
            'ping -n 3 127.0.0.1',
            'timeout 2'
        ]
    else:  # Unix-like
        commands = [
            'ls -la',
            'echo "Hello from subprocess!"',
            'ping -c 3 127.0.0.1',
            'sleep 2'
        ]
    
    async def run_command(cmd: str) -> Tuple[str, str, int]:
        """
        Run a command asynchronously.
        
        Args:
            cmd: Command to run.
            
        Returns:
            Tuple containing (command, output, return code).
        """
        print(f"Running command: {cmd}")
        
        # Create subprocess
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the subprocess to complete and get output
        stdout, stderr = await process.communicate()
        
        # Decode output
        stdout_str = stdout.decode('utf-8', errors='replace')
        stderr_str = stderr.decode('utf-8', errors='replace')
        
        # Combine stdout and stderr
        output = stdout_str
        if stderr_str:
            output += f"\nSTDERR:\n{stderr_str}"
        
        return (cmd, output, process.returncode)
    
    # Run commands sequentially
    print("\nRunning commands sequentially:")
    start_time = time.time()
    
    sequential_results = []
    for cmd in commands:
        result = await run_command(cmd)
        sequential_results.append(result)
    
    end_time = time.time()
    sequential_time = end_time - start_time
    print(f"Sequential execution completed in {sequential_time:.2f}s")
    
    # Run commands concurrently
    print("\nRunning commands concurrently:")
    start_time = time.time()
    
    tasks = [run_command(cmd) for cmd in commands]
    concurrent_results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    concurrent_time = end_time - start_time
    print(f"Concurrent execution completed in {concurrent_time:.2f}s")
    
    # Calculate speedup
    speedup = sequential_time / concurrent_time
    print(f"Speedup: {speedup:.2f}x")
    
    # Print results
    print("\nCommand results:")
    for cmd, output, returncode in concurrent_results:
        print(f"\nCommand: {cmd}")
        print(f"Return code: {returncode}")
        
        # Limit output to first few lines
        output_lines = output.splitlines()
        if len(output_lines) > 5:
            output = '\n'.join(output_lines[:5]) + f"\n... ({len(output_lines) - 5} more lines)"
        
        print(f"Output:\n{output}")


async def async_dns_resolution_example() -> None:
    """Demonstrate asynchronous DNS resolution."""
    print("\n=== Asynchronous DNS Resolution Example ===")
    
    # Domains to resolve
    domains = [
        "google.com",
        "github.com",
        "stackoverflow.com",
        "python.org",
        "microsoft.com",
        "apple.com",
        "amazon.com",
        "netflix.com",
        "facebook.com",
        "twitter.com"
    ]
    
    async def resolve_domain(domain: str) -> Tuple[str, List[str]]:
        """
        Resolve a domain name asynchronously.
        
        Args:
            domain: Domain name to resolve.
            
        Returns:
            Tuple containing (domain, list of IP addresses).
        """
        print(f"Resolving {domain}...")
        
        # Simulate DNS resolution with a delay
        await asyncio.sleep(random.uniform(0.2, 1.0))
        
        # Generate some fake IP addresses
        num_ips = random.randint(1, 3)
        ips = [f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}" for _ in range(num_ips)]
        
        return (domain, ips)
    
    # Resolve domains concurrently
    print("Resolving domains concurrently...")
    start_time = time.time()
    
    tasks = [resolve_domain(domain) for domain in domains]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Resolution completed in {end_time - start_time:.2f}s")
    
    # Print results
    for domain, ips in results:
        print(f"Domain: {domain}, IPs: {', '.join(ips)}")


async def run_demo() -> None:
    """Run all async I/O operations examples."""
    print("=== Asynchronous I/O Operations Examples ===")
    
    await async_file_read_write_example()
    await async_http_requests_example()
    await async_streaming_example()
    await async_subprocess_example()
    await async_dns_resolution_example()
    
    print("\nAll async I/O operations examples completed")


if __name__ == "__main__":
    asyncio.run(run_demo()) 