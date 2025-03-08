"""
Asynchronous web requests examples using asyncio and aiohttp.

This module demonstrates how to perform asynchronous web requests with asyncio and aiohttp.
"""

import asyncio
import aiohttp
import time
import random
import json
from typing import List, Dict, Any, Optional, Tuple, Set
from urllib.parse import urljoin


async def basic_web_requests_example() -> None:
    """Demonstrate basic asynchronous web requests."""
    print("\n=== Basic Asynchronous Web Requests Example ===")
    
    # URLs to fetch
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/headers"
    ]
    
    async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """
        Fetch a URL asynchronously and parse JSON response.
        
        Args:
            session: aiohttp client session.
            url: URL to fetch.
            
        Returns:
            Parsed JSON response.
        """
        print(f"Fetching {url}...")
        async with session.get(url) as response:
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
            data = await response.json()
            return data
    
    # Create a session and fetch URLs concurrently
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    # Print results
    for i, result in enumerate(results):
        print(f"\nResult from {urls[i]}:")
        print(json.dumps(result, indent=2)[:200] + "...")  # Truncate for brevity


async def http_methods_example() -> None:
    """Demonstrate different HTTP methods with aiohttp."""
    print("\n=== HTTP Methods Example ===")
    
    # Base URL for httpbin
    base_url = "https://httpbin.org"
    
    # Define endpoints and methods
    endpoints = [
        ("/get", "GET"),
        ("/post", "POST"),
        ("/put", "PUT"),
        ("/delete", "DELETE"),
        ("/patch", "PATCH")
    ]
    
    async def make_request(
        session: aiohttp.ClientSession, 
        method: str, 
        url: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with the specified method.
        
        Args:
            session: aiohttp client session.
            method: HTTP method (GET, POST, etc.).
            url: URL to request.
            data: Optional data to send with the request.
            
        Returns:
            Parsed JSON response.
        """
        print(f"Making {method} request to {url}...")
        
        # Prepare request data
        request_data = {
            "data": data or {"message": f"This is a {method} request"}
        }
        
        # Make the request
        async with session.request(method, url, json=request_data.get("data")) as response:
            response.raise_for_status()
            result = await response.json()
            return result
    
    # Create a session and make requests
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for endpoint, method in endpoints:
            url = urljoin(base_url, endpoint)
            tasks.append(make_request(session, method, url))
        
        results = await asyncio.gather(*tasks)
    
    # Print results
    for i, result in enumerate(results):
        endpoint, method = endpoints[i]
        print(f"\nResult from {method} request to {endpoint}:")
        
        # Extract and print relevant parts of the response
        if "json" in result:
            print(f"Sent data: {result['json']}")
        if "url" in result:
            print(f"URL: {result['url']}")
        if "headers" in result:
            print(f"Headers: {json.dumps(result['headers'], indent=2)[:100]}...")


async def parallel_requests_example() -> None:
    """Demonstrate making many parallel requests with rate limiting."""
    print("\n=== Parallel Requests with Rate Limiting Example ===")
    
    # URLs to fetch (we'll fetch the same URL multiple times)
    base_url = "https://httpbin.org/delay/"
    
    # Generate URLs with different delays
    urls = [f"{base_url}{random.uniform(0.1, 0.5):.1f}" for _ in range(20)]
    
    # Create a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(5)  # Allow only 5 concurrent requests
    
    async def fetch_with_semaphore(session: aiohttp.ClientSession, url: str, idx: int) -> Tuple[int, str, float]:
        """
        Fetch a URL with a semaphore for rate limiting.
        
        Args:
            session: aiohttp client session.
            url: URL to fetch.
            idx: Request index.
            
        Returns:
            Tuple containing (index, URL, elapsed time).
        """
        async with semaphore:
            print(f"Request {idx}: Acquired semaphore, fetching {url}")
            start_time = time.time()
            
            async with session.get(url) as response:
                await response.text()
                
                elapsed = time.time() - start_time
                print(f"Request {idx}: Released semaphore, took {elapsed:.2f}s")
                return (idx, url, elapsed)
    
    # Create a session and fetch URLs concurrently with rate limiting
    print(f"Fetching {len(urls)} URLs with max concurrency of 5...")
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_semaphore(session, url, i) for i, url in enumerate(urls)]
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Print results
    print(f"\nAll requests completed in {total_time:.2f}s")
    print(f"Average time per request: {total_time / len(urls):.2f}s")
    
    # Calculate statistics
    elapsed_times = [elapsed for _, _, elapsed in results]
    print(f"Min time: {min(elapsed_times):.2f}s")
    print(f"Max time: {max(elapsed_times):.2f}s")
    print(f"Avg time: {sum(elapsed_times) / len(elapsed_times):.2f}s")


async def error_handling_example() -> None:
    """Demonstrate error handling with aiohttp requests."""
    print("\n=== Error Handling Example ===")
    
    # URLs with different response codes
    urls = [
        "https://httpbin.org/status/200",  # OK
        "https://httpbin.org/status/404",  # Not Found
        "https://httpbin.org/status/500",  # Server Error
        "https://httpbin.org/status/403",  # Forbidden
        "https://httpbin.org/status/429",  # Too Many Requests
        "https://non-existent-domain-123456789.org"  # DNS error
    ]
    
    async def fetch_with_error_handling(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """
        Fetch a URL with comprehensive error handling.
        
        Args:
            session: aiohttp client session.
            url: URL to fetch.
            
        Returns:
            Dictionary with request result or error information.
        """
        try:
            async with session.get(url, timeout=5) as response:
                if response.status >= 400:
                    return {
                        "url": url,
                        "success": False,
                        "status": response.status,
                        "reason": response.reason,
                        "error": f"HTTP Error: {response.status} {response.reason}"
                    }
                
                # For successful responses, read the content
                content = await response.text()
                return {
                    "url": url,
                    "success": True,
                    "status": response.status,
                    "content_length": len(content)
                }
        except aiohttp.ClientConnectorError as e:
            return {
                "url": url,
                "success": False,
                "error": f"Connection Error: {str(e)}",
                "error_type": "ClientConnectorError"
            }
        except aiohttp.ClientResponseError as e:
            return {
                "url": url,
                "success": False,
                "error": f"Response Error: {str(e)}",
                "error_type": "ClientResponseError"
            }
        except aiohttp.ClientError as e:
            return {
                "url": url,
                "success": False,
                "error": f"Client Error: {str(e)}",
                "error_type": "ClientError"
            }
        except asyncio.TimeoutError:
            return {
                "url": url,
                "success": False,
                "error": "Request timed out",
                "error_type": "TimeoutError"
            }
        except Exception as e:
            return {
                "url": url,
                "success": False,
                "error": f"Unexpected Error: {str(e)}",
                "error_type": type(e).__name__
            }
    
    # Create a session and fetch URLs with error handling
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_error_handling(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    
    # Print results
    for result in results:
        url = result["url"]
        if result["success"]:
            print(f"\n✅ {url}: Success (Status: {result['status']}, Content Length: {result['content_length']})")
        else:
            print(f"\n❌ {url}: Failed - {result['error']}")


async def streaming_response_example() -> None:
    """Demonstrate handling streaming responses."""
    print("\n=== Streaming Response Example ===")
    
    # URL that returns a large response
    url = "https://httpbin.org/stream/20"  # Returns 20 JSON objects
    
    async def process_streaming_response(session: aiohttp.ClientSession, url: str) -> None:
        """
        Process a streaming response line by line.
        
        Args:
            session: aiohttp client session.
            url: URL to fetch.
        """
        print(f"Fetching streaming data from {url}...")
        
        async with session.get(url) as response:
            # Process the response as it comes in
            line_count = 0
            async for line in response.content:
                if line:
                    line_str = line.decode('utf-8').strip()
                    if line_str:
                        try:
                            data = json.loads(line_str)
                            line_count += 1
                            print(f"Received object {line_count}: id={data.get('id', 'N/A')}")
                        except json.JSONDecodeError:
                            print(f"Received non-JSON line: {line_str[:50]}...")
            
            print(f"Streaming complete, received {line_count} objects")
    
    # Create a session and process the streaming response
    async with aiohttp.ClientSession() as session:
        await process_streaming_response(session, url)


async def websocket_example() -> None:
    """Demonstrate using WebSockets with aiohttp."""
    print("\n=== WebSocket Example ===")
    
    # Echo WebSocket server
    url = "wss://echo.websocket.org"
    
    async def websocket_client() -> None:
        """Connect to a WebSocket server and exchange messages."""
        print(f"Connecting to WebSocket at {url}...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(url) as ws:
                    print("Connected to WebSocket server")
                    
                    # Send messages
                    for i in range(5):
                        message = f"Hello, WebSocket! Message {i+1}"
                        print(f"Sending: {message}")
                        await ws.send_str(message)
                        
                        # Wait for response
                        response = await ws.receive()
                        if response.type == aiohttp.WSMsgType.TEXT:
                            print(f"Received: {response.data}")
                        elif response.type == aiohttp.WSMsgType.CLOSED:
                            print("WebSocket closed")
                            break
                        elif response.type == aiohttp.WSMsgType.ERROR:
                            print(f"WebSocket error: {response.data}")
                            break
                        
                        # Pause between messages
                        await asyncio.sleep(0.5)
                    
                    # Close the connection
                    await ws.close()
                    print("WebSocket connection closed")
        except Exception as e:
            print(f"WebSocket error: {str(e)}")
    
    # Run the WebSocket client
    try:
        await websocket_client()
    except Exception as e:
        print(f"Failed to connect to WebSocket: {str(e)}")
        print("Note: This example requires an internet connection and a working WebSocket echo server.")


async def run_demo() -> None:
    """Run all async web requests examples."""
    print("=== Asynchronous Web Requests Examples ===")
    
    await basic_web_requests_example()
    await http_methods_example()
    await parallel_requests_example()
    await error_handling_example()
    await streaming_response_example()
    
    # WebSocket example may fail if the echo server is down
    try:
        await websocket_example()
    except Exception as e:
        print(f"\n=== WebSocket Example ===\nSkipped due to error: {str(e)}")
    
    print("\nAll async web requests examples completed")


if __name__ == "__main__":
    asyncio.run(run_demo()) 