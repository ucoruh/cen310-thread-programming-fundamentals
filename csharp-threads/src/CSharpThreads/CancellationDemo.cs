using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates cancellation patterns in C# using CancellationToken
    /// </summary>
    public static class CancellationDemo
    {
        /// <summary>
        /// Demonstrates basic cancellation token usage
        /// </summary>
        private static void BasicCancellationDemo()
        {
            Console.WriteLine("\n=== Basic Cancellation Demo ===");
            
            // Create a cancellation token source
            using var cts = new CancellationTokenSource();
            CancellationToken token = cts.Token;
            
            // Start a task that respects cancellation
            Task task = Task.Run(() =>
            {
                Console.WriteLine("Task started");
                
                for (int i = 0; i < 10; i++)
                {
                    // Check for cancellation
                    if (token.IsCancellationRequested)
                    {
                        Console.WriteLine("Cancellation requested, stopping work");
                        return; // Cooperative cancellation
                    }
                    
                    Console.WriteLine($"Working... {i}");
                    Thread.Sleep(500);
                }
                
                Console.WriteLine("Task completed normally");
            }, token);
            
            // Wait a bit then cancel
            Console.WriteLine("Press Enter to cancel the task...");
            Console.ReadLine();
            
            Console.WriteLine("Requesting cancellation...");
            cts.Cancel();
            
            // Wait for task to observe cancellation and complete
            try
            {
                task.Wait();
                Console.WriteLine("Task terminated gracefully after cancellation");
            }
            catch (AggregateException ae)
            {
                if (ae.InnerExceptions.Any(e => e is OperationCanceledException))
                    Console.WriteLine("Task was canceled");
                else
                    Console.WriteLine($"Task failed: {ae.InnerException?.Message}");
            }
        }
        
        /// <summary>
        /// Demonstrates cancellation token with automatic throw
        /// </summary>
        private static void ThrowingCancellationDemo()
        {
            Console.WriteLine("\n=== Throwing Cancellation Demo ===");
            
            // Create a cancellation token source with timeout
            using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(3));
            CancellationToken token = cts.Token;
            
            // Start a task that will throw when canceled
            Task task = Task.Run(() =>
            {
                Console.WriteLine("Task started, will run for 10 seconds unless canceled");
                
                for (int i = 0; i < 10; i++)
                {
                    // This will throw OperationCanceledException if cancellation is requested
                    token.ThrowIfCancellationRequested();
                    
                    Console.WriteLine($"Working... {i}");
                    Thread.Sleep(1000);
                }
                
                Console.WriteLine("Task completed normally");
            }, token);
            
            Console.WriteLine("Waiting for task (will be auto-canceled after 3 seconds)...");
            
            try
            {
                task.Wait();
                Console.WriteLine("Task completed without cancellation");
            }
            catch (AggregateException ae)
            {
                if (ae.InnerExceptions.Any(e => e is OperationCanceledException))
                    Console.WriteLine("Task was canceled as expected");
                else
                    Console.WriteLine($"Task failed: {ae.InnerException?.Message}");
            }
        }
        
        /// <summary>
        /// Demonstrates cancellation with async/await
        /// </summary>
        private static async Task AsyncCancellationDemoAsync()
        {
            Console.WriteLine("\n=== Async Cancellation Demo ===");
            
            // Create a cancellation token source
            using var cts = new CancellationTokenSource();
            CancellationToken token = cts.Token;
            
            // Cancel after 2 seconds
            cts.CancelAfter(TimeSpan.FromSeconds(2));
            
            try
            {
                Console.WriteLine("Starting async operation that should take 5 seconds...");
                
                // Asynchronously wait while checking for cancellation
                for (int i = 0; i < 5; i++)
                {
                    // Check cancellation before each delay
                    token.ThrowIfCancellationRequested();
                    
                    Console.WriteLine($"Async working... {i}");
                    await Task.Delay(1000, token); // This also respects cancellation
                }
                
                Console.WriteLine("Async operation completed normally");
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Async operation was canceled");
            }
        }
        
        /// <summary>
        /// Demonstrates cancellation propagation
        /// </summary>
        private static void CancellationPropagationDemo()
        {
            Console.WriteLine("\n=== Cancellation Propagation Demo ===");
            
            using var cts = new CancellationTokenSource();
            CancellationToken token = cts.Token;
            
            // Start a parent operation that creates child operations
            Task parentTask = Task.Run(async () =>
            {
                Console.WriteLine("Parent operation started");
                
                // Create child tasks that use the same token
                var childTasks = new List<Task>();
                
                for (int i = 0; i < 3; i++)
                {
                    int childId = i;
                    childTasks.Add(Task.Run(async () =>
                    {
                        Console.WriteLine($"Child {childId} started");
                        
                        try
                        {
                            // Each child does some work with periodic cancellation checks
                            for (int j = 0; j < 10; j++)
                            {
                                token.ThrowIfCancellationRequested();
                                
                                Console.WriteLine($"Child {childId} working... {j}");
                                await Task.Delay(500, token);
                            }
                            
                            Console.WriteLine($"Child {childId} completed normally");
                        }
                        catch (OperationCanceledException)
                        {
                            Console.WriteLine($"Child {childId} was canceled");
                            throw; // Re-throw to maintain cancellation state
                        }
                    }, token));
                }
                
                Console.WriteLine("All children started, waiting for completion or cancellation...");
                
                try
                {
                    await Task.WhenAll(childTasks);
                    Console.WriteLine("All children completed normally");
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("At least one child task was canceled");
                    throw; // Re-throw for the outer catch
                }
            });
            
            // Wait a bit then cancel all operations
            Console.WriteLine("Press Enter to cancel all operations...");
            Console.ReadLine();
            
            Console.WriteLine("Cancelling all operations...");
            cts.Cancel();
            
            try
            {
                parentTask.Wait();
                Console.WriteLine("All operations completed without cancellation (this shouldn't happen)");
            }
            catch (AggregateException ae)
            {
                if (ae.InnerExceptions.Any(e => e is OperationCanceledException))
                    Console.WriteLine("Operations were successfully canceled");
                else
                    Console.WriteLine($"Operations failed: {ae.InnerException?.Message}");
            }
        }
        
        /// <summary>
        /// Demonstrates linking cancellation token sources
        /// </summary>
        private static void LinkedCancellationDemo()
        {
            Console.WriteLine("\n=== Linked Cancellation Demo ===");
            
            // Create two independent cancellation token sources
            using var timeoutCts = new CancellationTokenSource();
            using var userCts = new CancellationTokenSource();
            
            // Create a linked token source that combines both
            using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(
                timeoutCts.Token, userCts.Token);
            
            // The linked token will be canceled if either source is canceled
            CancellationToken linkedToken = linkedCts.Token;
            
            // Set a timeout of 5 seconds
            timeoutCts.CancelAfter(TimeSpan.FromSeconds(5));
            
            // Start a task that will be canceled if either timeout occurs or user cancels
            Task task = Task.Run(() =>
            {
                Console.WriteLine("Task started, will run for 10 seconds unless canceled");
                Console.WriteLine("Will be canceled if 5 seconds timeout occurs OR user presses Enter");
                
                for (int i = 0; i < 10; i++)
                {
                    linkedToken.ThrowIfCancellationRequested();
                    
                    Console.WriteLine($"Working... {i}");
                    Thread.Sleep(1000);
                }
                
                Console.WriteLine("Task completed normally");
            }, linkedToken);
            
            // Allow user to cancel
            Console.WriteLine("Press Enter to manually cancel the task...");
            Console.ReadLine();
            
            // Check if the task is already canceled (by timeout)
            if (!task.IsCompleted)
            {
                Console.WriteLine("User requested cancellation");
                userCts.Cancel();
            }
            
            try
            {
                task.Wait();
                Console.WriteLine("Task completed without cancellation (this shouldn't happen)");
            }
            catch (AggregateException ae)
            {
                if (ae.InnerExceptions.Any(e => e is OperationCanceledException))
                {
                    if (timeoutCts.Token.IsCancellationRequested)
                        Console.WriteLine("Task was canceled due to timeout");
                    else if (userCts.Token.IsCancellationRequested)
                        Console.WriteLine("Task was canceled by user");
                    else
                        Console.WriteLine("Task was canceled (unknown source)");
                }
                else
                {
                    Console.WriteLine($"Task failed: {ae.InnerException?.Message}");
                }
            }
        }
        
        /// <summary>
        /// Runs the cancellation demos
        /// </summary>
        public static void RunDemo()
        {
            Console.WriteLine("=== Cancellation Patterns Demo ===");
            
            // Run the demos
            BasicCancellationDemo();
            ThrowingCancellationDemo();
            
            // Run the async demo synchronously
            AsyncCancellationDemoAsync().GetAwaiter().GetResult();
            
            CancellationPropagationDemo();
            LinkedCancellationDemo();
            
            Console.WriteLine("\nCancellation patterns demo completed");
        }
    }
} 