using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates ThreadPool usage in C#
    /// </summary>
    public static class ThreadPooling
    {
        /// <summary>
        /// Simulates work that will be executed on the thread pool
        /// </summary>
#pragma warning disable CS8622 // Nullability of reference types in type of parameter doesn't match target delegate
        private static void ThreadPoolWorkItem(object state)
#pragma warning restore CS8622
        {
            int workItemId = (int)state;
            Console.WriteLine($"Work item {workItemId} started on thread {Environment.CurrentManagedThreadId}");
            
            // Simulate some work
            Thread.Sleep(100 * workItemId);
            
            Console.WriteLine($"Work item {workItemId} completed on thread {Environment.CurrentManagedThreadId}");
        }
        
        /// <summary>
        /// Demonstrates basic ThreadPool usage
        /// </summary>
        private static void BasicThreadPoolDemo()
        {
            Console.WriteLine("\n=== Basic ThreadPool Demo ===");
            
            // Get the ThreadPool information
            ThreadPool.GetMinThreads(out int minWorkerThreads, out int minCompletionPortThreads);
            ThreadPool.GetMaxThreads(out int maxWorkerThreads, out int maxCompletionPortThreads);
            
            Console.WriteLine("ThreadPool Configuration:");
            Console.WriteLine($"Min Worker Threads: {minWorkerThreads}, Min Completion Port Threads: {minCompletionPortThreads}");
            Console.WriteLine($"Max Worker Threads: {maxWorkerThreads}, Max Completion Port Threads: {maxCompletionPortThreads}");
            
            // Get current thread count
            ThreadPool.GetAvailableThreads(out int availableWorkerThreads, out int availableCompletionPortThreads);
            Console.WriteLine($"Available Worker Threads: {availableWorkerThreads}, Available Completion Port Threads: {availableCompletionPortThreads}");
            
            Console.WriteLine("\nQueuing 10 work items to the ThreadPool...");
            
            // Queue multiple work items to the ThreadPool
            for (int i = 1; i <= 10; i++)
            {
                int workItemId = i; // Capture the loop variable
#pragma warning disable CS8622 // Nullability of reference types in type of parameter doesn't match target delegate
                ThreadPool.QueueUserWorkItem(ThreadPoolWorkItem, workItemId);
#pragma warning restore CS8622
            }
            
            // Wait for all work items to complete (simplified approach for demo)
            Console.WriteLine("Waiting for all work items to complete...");
            Thread.Sleep(2000);
            
            // Get updated thread count after queuing work
            ThreadPool.GetAvailableThreads(out availableWorkerThreads, out availableCompletionPortThreads);
            Console.WriteLine($"Available Worker Threads after work: {availableWorkerThreads}, Available Completion Port Threads: {availableCompletionPortThreads}");
        }
        
        /// <summary>
        /// Compares performance of ThreadPool vs creating new threads
        /// </summary>
        private static void ComparePerformanceDemo()
        {
            Console.WriteLine("\n=== ThreadPool vs New Threads Performance Comparison ===");
            
            const int workItemCount = 100;
            
            // Define the work to be done
            Action workAction = () =>
            {
                // Simple computation
                double result = 0;
                for (int i = 0; i < 100000; i++)
                {
                    result += Math.Sqrt(i);
                }
            };
            
            // Measure performance using ThreadPool
            Stopwatch stopwatch = Stopwatch.StartNew();
            
            using ManualResetEvent allDone = new ManualResetEvent(false);
            int remainingWorkItems = workItemCount;
            
            for (int i = 0; i < workItemCount; i++)
            {
                ThreadPool.QueueUserWorkItem(_ =>
                {
                    try
                    {
                        workAction();
                    }
                    finally
                    {
                        if (Interlocked.Decrement(ref remainingWorkItems) == 0)
                        {
                            allDone.Set();
                        }
                    }
                });
            }
            
            // Wait for all ThreadPool work items to complete
            allDone.WaitOne();
            
            stopwatch.Stop();
            long threadPoolTime = stopwatch.ElapsedMilliseconds;
            Console.WriteLine($"ThreadPool execution time for {workItemCount} work items: {threadPoolTime} ms");
            
            // Reset for the next test
            remainingWorkItems = workItemCount;
            allDone.Reset();
            
            // Measure performance using new threads
            stopwatch.Restart();
            
            Thread[] threads = new Thread[workItemCount];
            for (int i = 0; i < workItemCount; i++)
            {
                threads[i] = new Thread(_ =>
                {
                    try
                    {
                        workAction();
                    }
                    finally
                    {
                        if (Interlocked.Decrement(ref remainingWorkItems) == 0)
                        {
                            allDone.Set();
                        }
                    }
                });
                threads[i].Start();
            }
            
            // Wait for all threads to complete
            allDone.WaitOne();
            
            stopwatch.Stop();
            long newThreadsTime = stopwatch.ElapsedMilliseconds;
            Console.WriteLine($"New Threads execution time for {workItemCount} work items: {newThreadsTime} ms");
            
            // Calculate the performance difference
            double speedupFactor = (double)newThreadsTime / threadPoolTime;
            Console.WriteLine($"ThreadPool is approximately {speedupFactor:F2}x faster than creating new threads");
        }
        
        /// <summary>
        /// Demonstrates how to configure and adjust the ThreadPool
        /// </summary>
        private static void ThreadPoolConfigurationDemo()
        {
            Console.WriteLine("\n=== ThreadPool Configuration Demo ===");
            
            // Get the current ThreadPool configuration
            ThreadPool.GetMinThreads(out int originalMinWorkerThreads, out int originalMinCompletionPortThreads);
            
            Console.WriteLine("Original ThreadPool Configuration:");
            Console.WriteLine($"Min Worker Threads: {originalMinWorkerThreads}, Min Completion Port Threads: {originalMinCompletionPortThreads}");
            
            // Set new minimum thread count
            int newMinWorkerThreads = Environment.ProcessorCount * 4;
            int newMinCompletionPortThreads = originalMinCompletionPortThreads;
            
            Console.WriteLine($"\nSetting new minimum worker threads to {newMinWorkerThreads}...");
            bool success = ThreadPool.SetMinThreads(newMinWorkerThreads, newMinCompletionPortThreads);
            
            if (success)
            {
                Console.WriteLine("Successfully changed ThreadPool configuration");
                
                // Verify the new configuration
                ThreadPool.GetMinThreads(out int updatedMinWorkerThreads, out int updatedMinCompletionPortThreads);
                Console.WriteLine($"Updated Min Worker Threads: {updatedMinWorkerThreads}, Min Completion Port Threads: {updatedMinCompletionPortThreads}");
            }
            else
            {
                Console.WriteLine("Failed to change ThreadPool configuration");
            }
            
            // Restore original configuration
            ThreadPool.SetMinThreads(originalMinWorkerThreads, originalMinCompletionPortThreads);
            Console.WriteLine("\nRestored original ThreadPool configuration");
        }
        
        /// <summary>
        /// Demonstrates the relationship between ThreadPool and Task
        /// </summary>
        private static void TaskAndThreadPoolDemo()
        {
            Console.WriteLine("\n=== Task and ThreadPool Relationship Demo ===");
            
            Console.WriteLine("Tasks created with Task.Run() typically use ThreadPool threads:");
            
            // Check ThreadPool before creating tasks
            ThreadPool.GetAvailableThreads(out int availableWorkerBefore, out int availableIoBefore);
            Console.WriteLine($"Available worker threads before tasks: {availableWorkerBefore}");
            
            // Create and start multiple tasks
            const int taskCount = 10;
            Task[] tasks = new Task[taskCount];
            
            for (int i = 0; i < taskCount; i++)
            {
                int taskId = i;
                tasks[i] = Task.Run(() =>
                {
                    Console.WriteLine($"Task {taskId} running on thread {Environment.CurrentManagedThreadId} (ThreadPool thread)");
                    Thread.Sleep(500); // Simulate work
                });
            }
            
            // Wait for some time to allow tasks to start
            Thread.Sleep(100);
            
            // Check ThreadPool during task execution
            ThreadPool.GetAvailableThreads(out int availableWorkerDuring, out int availableIoDuring);
            Console.WriteLine($"Available worker threads during tasks: {availableWorkerDuring}");
            Console.WriteLine($"ThreadPool threads being used: {availableWorkerBefore - availableWorkerDuring}");
            
            // Wait for all tasks to complete
            Task.WaitAll(tasks);
            
            // Check ThreadPool after tasks complete
            ThreadPool.GetAvailableThreads(out int availableWorkerAfter, out int availableIoAfter);
            Console.WriteLine($"Available worker threads after tasks: {availableWorkerAfter}");
            Console.WriteLine("\nThreadPool threads are returned to the pool after tasks complete");
        }
        
        /// <summary>
        /// Demonstrates how to handle I/O-bound vs CPU-bound operations
        /// </summary>
        private static async Task IOvsCPUBoundDemoAsync()
        {
            Console.WriteLine("\n=== I/O-bound vs CPU-bound Operations ===");
            
            Console.WriteLine("\nI/O-bound operations (e.g., network requests, file access):");
            Console.WriteLine("- Use async/await to avoid blocking ThreadPool threads");
            Console.WriteLine("- Free up threads during I/O wait");
            
            // Simulate I/O-bound operation
            Stopwatch stopwatch = Stopwatch.StartNew();
            Console.WriteLine("Starting I/O-bound operation with async/await...");
            
            await Task.Delay(1000); // Simulate I/O delay
            
            stopwatch.Stop();
            Console.WriteLine($"I/O-bound operation completed in {stopwatch.ElapsedMilliseconds} ms");
            Console.WriteLine("During I/O wait, ThreadPool thread was freed for other work");
            
            Console.WriteLine("\nCPU-bound operations (e.g., computation, data processing):");
            Console.WriteLine("- Use Task.Run() to offload to ThreadPool");
            Console.WriteLine("- Consider limiting parallel tasks to avoid ThreadPool saturation");
            
            // Simulate CPU-bound operation
            stopwatch.Restart();
            Console.WriteLine("Starting CPU-bound operation with Task.Run()...");
            
            await Task.Run(() =>
            {
                double result = 0;
                // Simulate CPU-intensive work
                for (int i = 0; i < 10_000_000; i++)
                {
                    result += Math.Sqrt(i);
                }
                return result;
            });
            
            stopwatch.Stop();
            Console.WriteLine($"CPU-bound operation completed in {stopwatch.ElapsedMilliseconds} ms");
            Console.WriteLine("CPU-bound work occupied a ThreadPool thread for the entire duration");
        }
        
        /// <summary>
        /// Runs the ThreadPool demos
        /// </summary>
        public static void RunDemo()
        {
            Console.WriteLine("=== ThreadPool Demo ===");
            
            // Run the demos
            BasicThreadPoolDemo();
            ComparePerformanceDemo();
            ThreadPoolConfigurationDemo();
            TaskAndThreadPoolDemo();
            
            // Run the async demo synchronously
            IOvsCPUBoundDemoAsync().GetAwaiter().GetResult();
            
            Console.WriteLine("\nThreadPool demo completed");
        }
    }
} 