using System;
using System.Threading;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates basic threading concepts in C# using the System.Threading.Thread class
    /// </summary>
    public static class BasicThreading
    {
        /// <summary>
        /// Simple thread function that writes a message to the console
        /// </summary>
        private static void ThreadFunction()
        {
            int threadId = Thread.CurrentThread.ManagedThreadId;
            Console.WriteLine($"Thread function running in thread ID: {threadId}");
            
            // Simulate some work
            Thread.Sleep(1000);
            
            Console.WriteLine($"Thread function finished in thread ID: {threadId}");
        }
        
        /// <summary>
        /// Thread function that accepts a parameter
        /// </summary>
        private static void ParameterizedThreadFunction(object? parameter)
        {
            string message = parameter as string ?? "No message provided";
            int threadId = Thread.CurrentThread.ManagedThreadId;
            
            Console.WriteLine($"Thread {threadId} received message: {message}");
            
            // Simulate some work
            Thread.Sleep(1000);
            
            Console.WriteLine($"Thread {threadId} finished processing");
        }
        
        /// <summary>
        /// Demonstrates creating and starting a basic thread
        /// </summary>
        private static void ThreadCreationDemo()
        {
            Console.WriteLine("\n=== Thread Creation Demo ===");
            
            // Get the main thread ID
            int mainThreadId = Thread.CurrentThread.ManagedThreadId;
            Console.WriteLine($"Main thread ID: {mainThreadId}");
            
            // Create a new thread with a ThreadStart delegate
            Thread thread = new Thread(ThreadFunction);
            
            // Start the thread
            thread.Start();
            
            // Display thread ID
            Console.WriteLine($"Created thread with ID: {thread.ManagedThreadId}");
            
            // Wait for the thread to complete
            thread.Join();
            
            Console.WriteLine("Thread has been joined");
        }
        
        /// <summary>
        /// Demonstrates passing arguments to a thread
        /// </summary>
        private static void ThreadArgumentsDemo()
        {
            Console.WriteLine("\n=== Thread Arguments Demo ===");
            
            // Create a new thread with a ParameterizedThreadStart delegate
            Thread thread = new Thread(ParameterizedThreadFunction);
            
            // Start the thread with a parameter
            thread.Start("Hello from the main thread!");
            
            // We can also choose to detach from the thread and continue execution
            Console.WriteLine("Detaching thread...");
            
            // Note that we're not calling Join() on the thread
            Console.WriteLine("Main thread continues execution...");
        }
        
        /// <summary>
        /// Demonstrates using a lambda expression to create a thread
        /// </summary>
        private static void LambdaThreadDemo()
        {
            Console.WriteLine("\n=== Lambda Thread Demo ===");
            
            // Define a lambda expression that will run in a new thread
            Thread thread = new Thread(() =>
            {
                // Lambda can capture variables from the enclosing scope
                int data = 42;
                
                Console.WriteLine($"Lambda thread received data: {data}");
                Thread.Sleep(500);
                Console.WriteLine("Lambda thread finished");
            });
            
            // Start the thread
            thread.Start();
            
            // Wait for the thread to complete
            thread.Join();
            
            Console.WriteLine("Lambda thread has been joined");
        }
        
        /// <summary>
        /// Demonstrates creating and managing multiple threads
        /// </summary>
        private static void MultipleThreadsDemo()
        {
            Console.WriteLine("\n=== Multiple Threads Demo ===");
            
            // Create an array of threads
            const int threadCount = 5;
            Thread[] threads = new Thread[threadCount];
            
            // Initialize and start all threads
            for (int i = 0; i < threadCount; i++)
            {
                int threadNumber = i; // Capture the loop variable
                
                threads[i] = new Thread(() =>
                {
                    int threadId = Thread.CurrentThread.ManagedThreadId;
                    Console.WriteLine($"Thread {threadNumber} starting with ID: {threadId}");
                    
                    // Simulate some work with varying durations
                    Thread.Sleep(threadNumber * 100 + 500);
                    
                    Console.WriteLine($"Thread {threadNumber} finished");
                });
                
                // Start each thread
                threads[i].Start();
            }
            
            Console.WriteLine($"Created {threadCount} threads");
            
            // Wait for all threads to complete
            foreach (Thread thread in threads)
            {
                thread.Join();
            }
            
            Console.WriteLine("All threads have been joined");
        }
        
        /// <summary>
        /// Demonstrates common thread properties and operations
        /// </summary>
        private static void ThreadPropertiesDemo()
        {
            Console.WriteLine("\n=== Thread Properties Demo ===");
            
            // Create a thread to demonstrate properties
            Thread thread = new Thread(() =>
            {
                Console.WriteLine($"Running thread with IsBackground={Thread.CurrentThread.IsBackground}");
                
                // Demonstrate thread states by sleeping
                Console.WriteLine("Thread going to sleep (WaitSleepJoin state)");
                Thread.Sleep(1000);
                
                Console.WriteLine("Thread woke up and is now completing");
            });
            
            // Set thread name (useful for debugging)
            thread.Name = "DemoThread";
            
            // Set as background thread (will terminate when main thread ends)
            thread.IsBackground = true;
            
            // Set thread priority
            thread.Priority = ThreadPriority.AboveNormal;
            
            // Display thread properties before starting
            Console.WriteLine($"Thread properties before start:");
            Console.WriteLine($"  Name: {thread.Name}");
            Console.WriteLine($"  IsBackground: {thread.IsBackground}");
            Console.WriteLine($"  Priority: {thread.Priority}");
            Console.WriteLine($"  ThreadState: {thread.ThreadState}");
            
            // Start the thread
            thread.Start();
            
            // Give a little time for the thread to enter the running state
            Thread.Sleep(100);
            
            // Display thread state after starting
            Console.WriteLine($"Thread state after starting: {thread.ThreadState}");
            
            // Wait for the thread to complete
            thread.Join();
            
            // Display final thread state
            Console.WriteLine($"Final thread state: {thread.ThreadState}");
        }
        
        /// <summary>
        /// Demonstrates aborting a thread - note this is not generally recommended
        /// and Thread.Abort() is not supported in .NET Core and .NET 5+
        /// </summary>
        private static void ThreadCancellationDemo()
        {
            Console.WriteLine("\n=== Thread Cancellation Demo ===");
            
            // The cooperative cancellation pattern is now recommended instead of Thread.Abort
            
            // Create a cancellation flag
            bool shouldCancel = false;
            
            // Create a thread that periodically checks the cancellation flag
            Thread thread = new Thread(() =>
            {
                Console.WriteLine("Thread started and will run until cancelled");
                
                // Continue until cancellation is requested
                while (!shouldCancel)
                {
                    Console.WriteLine("Thread working...");
                    
                    // Simulate some work
                    Thread.Sleep(500);
                    
                    // Check for cancellation
                    if (shouldCancel)
                    {
                        Console.WriteLine("Cancellation detected, cleaning up...");
                        
                        // Perform any cleanup here
                        Thread.Sleep(100);
                        
                        break;
                    }
                }
                
                Console.WriteLine("Thread exiting gracefully after cancellation");
            });
            
            // Start the thread
            thread.Start();
            
            // Let the thread run for a while
            Console.WriteLine("Main thread waiting before cancelling...");
            Thread.Sleep(2000);
            
            // Request cancellation
            Console.WriteLine("Main thread requesting cancellation...");
            shouldCancel = true;
            
            // Wait for the thread to complete
            thread.Join();
            
            Console.WriteLine("Thread has been successfully cancelled and joined");
            
            Console.WriteLine("\nNote: Thread.Abort() is not supported in .NET Core and .NET 5+");
            Console.WriteLine("Use cooperative cancellation with CancellationToken instead");
        }
        
        /// <summary>
        /// Demonstrates differences between foreground and background threads
        /// </summary>
        private static void ForegroundBackgroundDemo()
        {
            Console.WriteLine("\n=== Foreground vs Background Threads Demo ===");
            
            // Create a background thread
            Thread backgroundThread = new Thread(() =>
            {
                Console.WriteLine("Background thread started");
                
                // Simulate long-running work
                for (int i = 0; i < 10; i++)
                {
                    Console.WriteLine($"Background thread working... ({i+1}/10)");
                    Thread.Sleep(500);
                }
                
                Console.WriteLine("Background thread finished (this might not be seen)");
            });
            
            // Set as background thread
            backgroundThread.IsBackground = true;
            Console.WriteLine("Created background thread (will terminate when main thread exits)");
            
            // Create a foreground thread
            Thread foregroundThread = new Thread(() =>
            {
                Console.WriteLine("Foreground thread started");
                
                // Simulate shorter work
                for (int i = 0; i < 3; i++)
                {
                    Console.WriteLine($"Foreground thread working... ({i+1}/3)");
                    Thread.Sleep(500);
                }
                
                Console.WriteLine("Foreground thread finished");
            });
            
            // Foreground is default, but we'll set it explicitly for clarity
            foregroundThread.IsBackground = false;
            Console.WriteLine("Created foreground thread (application will wait for it to complete)");
            
            // Start both threads
            backgroundThread.Start();
            foregroundThread.Start();
            
            // Wait for the foreground thread to complete
            foregroundThread.Join();
            
            Console.WriteLine("Main thread completed. The application will exit now.");
            Console.WriteLine("Note: The background thread may not complete all its work.");
            
            // Note: We're deliberately not joining the background thread to demonstrate
            // that it will be terminated when the application exits
        }
        
        /// <summary>
        /// Demonstrates thread local storage using ThreadLocal<T>
        /// </summary>
        private static void ThreadLocalStorageDemo()
        {
            Console.WriteLine("\n=== Thread Local Storage Demo ===");
            
            // Create a thread-local variable
            ThreadLocal<int> threadLocalValue = new ThreadLocal<int>(() => 
            {
                // This initializer runs once per thread
                int threadId = Thread.CurrentThread.ManagedThreadId;
                Console.WriteLine($"Initializing thread-local value for thread {threadId}");
                return threadId * 10; // Different initial value for each thread
            });
            
            // Create several threads that use the thread-local variable
            Thread[] threads = new Thread[3];
            
            for (int i = 0; i < threads.Length; i++)
            {
                threads[i] = new Thread(() =>
                {
                    // Access the thread-local value
                    int threadId = Thread.CurrentThread.ManagedThreadId;
                    Console.WriteLine($"Thread {threadId} has initial value: {threadLocalValue.Value}");
                    
                    // Modify the thread-local value (only affects this thread)
                    threadLocalValue.Value += 5;
                    
                    Console.WriteLine($"Thread {threadId} modified value to: {threadLocalValue.Value}");
                });
                
                threads[i].Start();
            }
            
            // Wait for all threads to complete
            foreach (Thread thread in threads)
            {
                thread.Join();
            }
            
            // Access the thread-local value from the main thread
            Console.WriteLine($"Main thread value: {threadLocalValue.Value}");
            
            // Dispose when no longer needed
            threadLocalValue.Dispose();
            
            Console.WriteLine("ThreadLocal<T> provides isolation between threads");
        }
        
        /// <summary>
        /// Run all basic threading demos
        /// </summary>
        public static void RunDemo()
        {
            Console.WriteLine("=== Thread Basics Demo ===");
            
            // Run the demos
            ThreadCreationDemo();
            ThreadArgumentsDemo();
            LambdaThreadDemo();
            MultipleThreadsDemo();
            ThreadPropertiesDemo();
            ThreadCancellationDemo();
            ForegroundBackgroundDemo();
            ThreadLocalStorageDemo();
            
            Console.WriteLine("\nThread basics demonstration completed");
        }
    }
} 