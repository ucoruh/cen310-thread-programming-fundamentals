using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates C# async/await patterns and asynchronous programming
    /// </summary>
    public static class AsyncAwaitPatterns
    {
        // HttpClient for making web requests
        private static readonly HttpClient HttpClient = new HttpClient();
        
        /// <summary>
        /// Simulates an asynchronous operation
        /// </summary>
        private static async Task<string> SimulateAsyncOperation(string operationName, int delayMs)
        {
            Console.WriteLine($"Starting operation '{operationName}' on thread {Environment.CurrentManagedThreadId}");
            
            // Asynchronously wait for the specified time
            await Task.Delay(delayMs);
            
            Console.WriteLine($"Completed operation '{operationName}' on thread {Environment.CurrentManagedThreadId}");
            return $"Result from {operationName}";
        }
        
        /// <summary>
        /// Simulates an asynchronous operation that throws an exception
        /// </summary>
        private static async Task<string> SimulateAsyncFailure(string operationName, int delayMs)
        {
            Console.WriteLine($"Starting operation '{operationName}' that will fail...");
            
            // Asynchronously wait for the specified time
            await Task.Delay(delayMs);
            
            throw new InvalidOperationException($"Operation '{operationName}' failed");
        }
        
        /// <summary>
        /// Basic demonstration of async/await pattern
        /// </summary>
        private static async Task BasicAsyncAwaitDemo()
        {
            Console.WriteLine("\n=== Basic Async/Await Demo ===");
            Console.WriteLine($"Initial thread: {Environment.CurrentManagedThreadId}");
            
            // Call asynchronous method and await result
            string result = await SimulateAsyncOperation("Basic Demo", 1000);
            Console.WriteLine($"Received result: {result}");
            
            // Demonstrate that await allows the calling thread to continue with other work
            Console.WriteLine("\nDemonstrating non-blocking behavior:");
            var asyncTask = SimulateAsyncOperation("Background Task", 2000);
            
            // Do other work while the task is running
            Console.WriteLine("Main thread is continuing with other work...");
            for (int i = 0; i < 3; i++)
            {
                Console.WriteLine($"Main thread working... {i}");
                Thread.Sleep(300); // Simulate work on main thread
            }
            
            // Now wait for the async task to complete
            Console.WriteLine("Main thread now waiting for background task...");
            string backgroundResult = await asyncTask;
            Console.WriteLine($"Background task result: {backgroundResult}");
        }
        
        /// <summary>
        /// Demonstrates async/await with error handling
        /// </summary>
        private static async Task AsyncErrorHandlingDemo()
        {
            Console.WriteLine("\n=== Async Error Handling Demo ===");
            
            // Using try/catch with await
            try
            {
                Console.WriteLine("Calling an async method that will fail...");
                string result = await SimulateAsyncFailure("Doomed Operation", 500);
                Console.WriteLine($"This line won't execute - result: {result}");
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"Caught exception: {ex.Message}");
            }
            
            // Demonstrate exception propagation through multiple awaits
            Console.WriteLine("\nDemonstrating exception propagation through multiple awaits:");
            
            async Task<string> Level3()
            {
                return await SimulateAsyncFailure("Level 3", 200);
            }
            
            async Task<string> Level2()
            {
                return await Level3();
            }
            
            async Task<string> Level1()
            {
                return await Level2();
            }
            
            try
            {
                await Level1();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Exception from nested calls: {ex.Message}");
                Console.WriteLine($"Stack trace shows async call chain:");
                Console.WriteLine(ex.StackTrace);
            }
        }
        
        /// <summary>
        /// Demonstrates composition of asynchronous operations
        /// </summary>
        private static async Task AsyncCompositionDemo()
        {
            Console.WriteLine("\n=== Async Composition Demo ===");
            
            // Sequential composition
            Console.WriteLine("\n1. Sequential execution of async operations:");
            var watch = System.Diagnostics.Stopwatch.StartNew();
            
            string result1 = await SimulateAsyncOperation("Operation 1", 500);
            string result2 = await SimulateAsyncOperation("Operation 2", 700);
            string result3 = await SimulateAsyncOperation("Operation 3", 600);
            
            watch.Stop();
            Console.WriteLine($"Sequential execution completed in {watch.ElapsedMilliseconds}ms");
            Console.WriteLine($"Results: {result1}, {result2}, {result3}");
            
            // Parallel composition
            Console.WriteLine("\n2. Parallel execution of async operations:");
            watch.Restart();
            
            Task<string> task1 = SimulateAsyncOperation("Parallel 1", 500);
            Task<string> task2 = SimulateAsyncOperation("Parallel 2", 700);
            Task<string> task3 = SimulateAsyncOperation("Parallel 3", 600);
            
            // Wait for all tasks to complete
            await Task.WhenAll(task1, task2, task3);
            
            watch.Stop();
            Console.WriteLine($"Parallel execution completed in {watch.ElapsedMilliseconds}ms");
            Console.WriteLine($"Results: {task1.Result}, {task2.Result}, {task3.Result}");
            
            // Combined patterns
            Console.WriteLine("\n3. Combined sequential and parallel patterns:");
            watch.Restart();
            
            // First operation
            string firstResult = await SimulateAsyncOperation("First Operation", 400);
            
            // Then multiple parallel operations
            var parallelTasks = new List<Task<string>>
            {
                SimulateAsyncOperation("Second Parallel 1", 500),
                SimulateAsyncOperation("Second Parallel 2", 600),
                SimulateAsyncOperation("Second Parallel 3", 450)
            };
            
            await Task.WhenAll(parallelTasks);
            
            // Then a final operation
            string finalResult = await SimulateAsyncOperation("Final Operation", 300);
            
            watch.Stop();
            Console.WriteLine($"Combined execution completed in {watch.ElapsedMilliseconds}ms");
        }
        
        /// <summary>
        /// Demonstrates async/await with I/O operations
        /// </summary>
        private static async Task AsyncIODemo()
        {
            Console.WriteLine("\n=== Async I/O Demo ===");
            
            // File I/O examples
            string tempFile = Path.GetTempFileName();
            try
            {
                Console.WriteLine("\n1. Asynchronous file operations:");
                Console.WriteLine($"Working with temp file: {tempFile}");
                
                // Write to file asynchronously
                string dataToWrite = "This is sample data written asynchronously to a file.\n" +
                                     "Async file operations are efficient for I/O-bound operations.";
                                     
                Console.WriteLine("Writing to file asynchronously...");
                await File.WriteAllTextAsync(tempFile, dataToWrite);
                
                // Read from file asynchronously
                Console.WriteLine("Reading from file asynchronously...");
                string readData = await File.ReadAllTextAsync(tempFile);
                
                Console.WriteLine($"Read {readData.Length} characters from file.");
            }
            finally
            {
                // Clean up
                if (File.Exists(tempFile))
                {
                    File.Delete(tempFile);
                }
            }
            
            // Network I/O example
            try
            {
                Console.WriteLine("\n2. Asynchronous HTTP request:");
                Console.WriteLine("Making asynchronous HTTP request to example.com...");
                
                string content = await HttpClient.GetStringAsync("http://example.com");
                
                // Display a portion of the content
                Console.WriteLine($"Received response of {content.Length} characters");
                Console.WriteLine("First 100 characters of response:");
                Console.WriteLine(content.Substring(0, Math.Min(100, content.Length)) + "...");
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine($"HTTP request failed: {ex.Message}");
            }
        }
        
        /// <summary>
        /// Demonstrates async/await with cancellation support
        /// </summary>
        private static async Task AsyncCancellationDemo()
        {
            Console.WriteLine("\n=== Async Cancellation Demo ===");
            
            // Create a cancellation token source
            using var cts = new CancellationTokenSource();
            CancellationToken token = cts.Token;
            
            // Define an async operation that supports cancellation
            async Task<string> CancellableOperation(CancellationToken cancellationToken)
            {
                Console.WriteLine("Starting long-running cancellable operation...");
                
                // Simulate work with cancellation support
                for (int i = 0; i < 10; i++)
                {
                    // Check for cancellation request
                    cancellationToken.ThrowIfCancellationRequested();
                    
                    Console.WriteLine($"Operation progress: {i * 10}%");
                    
                    try
                    {
                        // Using Task.Delay with cancellation token
                        await Task.Delay(300, cancellationToken);
                    }
                    catch (TaskCanceledException)
                    {
                        Console.WriteLine("Delay was canceled");
                        throw; // Re-throw to propagate cancellation
                    }
                }
                
                return "Operation completed successfully";
            }
            
            // Start the operation
            Task<string> task = CancellableOperation(token);
            
            // Schedule a cancellation after a timeout
            Console.WriteLine("Will request cancellation after 1 second...");
            await Task.Delay(1000);
            
            Console.WriteLine("Requesting cancellation...");
            cts.Cancel();
            
            try
            {
                string result = await task;
                Console.WriteLine($"Result: {result}");
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Operation was canceled as expected.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Unexpected exception: {ex.Message}");
            }
        }
        
        /// <summary>
        /// Demonstrates async void pattern and its issues
        /// </summary>
        private static void AsyncVoidPatternDemo()
        {
            Console.WriteLine("\n=== Async Void Pattern Demo ===");
            Console.WriteLine("WARNING: Async void methods should generally be avoided except for event handlers.");
            
            // UNSAFE: This async void method can cause the application to crash
            // COMMENTED OUT FOR EDUCATIONAL PURPOSES ONLY
            /*
            // Define an async void method - exceptions can't be caught by the caller
            async void AsyncVoidMethod()
            {
                Console.WriteLine("Async void method started");
                await Task.Delay(500);
                
                // This will crash the program unless handled at AppDomain level
                throw new InvalidOperationException("Exception from async void method");
            }
            */

            // Define a safer alternative using Task
            async Task<string> AsyncTaskMethod()
            {
                Console.WriteLine("Async Task method started");
                await Task.Delay(500);
                
                // This can be caught properly by the caller
                throw new InvalidOperationException("Exception from async Task method");
            }

            Console.WriteLine("\n1. Async void methods and exceptions - SIMULATION ONLY:");
            Console.WriteLine("When calling an async void method (commented out for safety):");
            Console.WriteLine("  - The exception CANNOT be caught by the caller's try/catch");
            Console.WriteLine("  - The exception escalates to the SynchronizationContext or thread pool");
            Console.WriteLine("  - The application may crash if there's no global exception handler");
            Console.WriteLine("\nThe unsafe method call has been commented out to prevent the application from crashing");
            Console.WriteLine("An actual call would look like this: AsyncVoidMethod();");

            try
            {
                Console.WriteLine("\n2. Async Task methods and exceptions (safe alternative):");
                Console.WriteLine("Calling AsyncTaskMethod() - exceptions can be caught properly:");
                
                // Call the async Task method and wait for it - this allows exceptions to be caught
                try
                {
                    // Use Task.Run to call and wait for the async Task method
                    Task.Run(async () => await AsyncTaskMethod()).Wait();
                }
                catch (AggregateException ae)
                {
                    // Exceptions from Task methods are properly propagated
                    Console.WriteLine($"Caught exception from async Task method: {ae.InnerException?.Message ?? "No inner exception details available"}");
                    Console.WriteLine("✓ This is the proper way to handle exceptions in async code");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Outer catch: {ex.Message}");
            }
            
            Console.WriteLine("\nConclusion: Always use async Task instead of async void when possible!");
        }
        
        /// <summary>
        /// Run all async/await demos sequentially
        /// </summary>
        private static async Task RunDemoAsync()
        {
            Console.WriteLine("=== Async/Await Patterns Demo ===");
            
            await BasicAsyncAwaitDemo();
            await AsyncErrorHandlingDemo();
            await AsyncCompositionDemo();
            await AsyncIODemo();
            await AsyncCancellationDemo();
            // AsyncVoidPatternDemo is no longer an async method, so call directly without await
            AsyncVoidPatternDemo();
            
            Console.WriteLine("\nAsync/Await Patterns demo completed");
        }
        
        /// <summary>
        /// Synchronous wrapper for RunDemoAsync
        /// </summary>
        public static void RunDemo()
        {
            // Run the async task synchronously
            RunDemoAsync().GetAwaiter().GetResult();
        }
    }
} 