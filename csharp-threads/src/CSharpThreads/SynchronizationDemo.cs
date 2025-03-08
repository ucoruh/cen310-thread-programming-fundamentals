using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates various synchronization mechanisms in C#
    /// </summary>
    public static class SynchronizationDemo
    {
        // Shared counter for demonstration purposes
        private static int _counter;
        
        /// <summary>
        /// Demonstrates using lock statement for synchronization
        /// </summary>
        private static void LockDemo()
        {
            Console.WriteLine("\n=== Lock Statement Demo ===");
            
            // The object to lock on
            object lockObject = new object();
            
            // Reset counter
            _counter = 0;
            
            // Create a list of tasks that will increment the counter
            List<Task> tasks = new List<Task>();
            
            for (int i = 0; i < 10; i++)
            {
                tasks.Add(Task.Run(() => 
                {
                    for (int j = 0; j < 1000; j++)
                    {
                        // The lock statement ensures only one thread can execute this block at a time
                        lock (lockObject)
                        {
                            _counter++;
                        }
                    }
                }));
            }
            
            // Wait for all tasks to complete
            Task.WaitAll(tasks.ToArray());
            
            // Check the result - should be exactly 10 * 1000 = 10000
            Console.WriteLine($"Counter value after synchronized increments: {_counter}");
            Console.WriteLine($"Expected value: {10 * 1000}");
            
            // Reset counter to demonstrate the problem without locking
            _counter = 0;
            tasks.Clear();
            
            for (int i = 0; i < 10; i++)
            {
                tasks.Add(Task.Run(() => 
                {
                    for (int j = 0; j < 1000; j++)
                    {
                        // No lock - will result in race conditions
                        _counter++;
                    }
                }));
            }
            
            // Wait for all tasks to complete
            Task.WaitAll(tasks.ToArray());
            
            // Check the result - will be less than 10000 due to race conditions
            Console.WriteLine($"Counter value after unsynchronized increments: {_counter}");
            Console.WriteLine($"Expected value: {10 * 1000}");
            Console.WriteLine("Note: Value is likely less than expected due to race conditions");
        }
        
        /// <summary>
        /// Demonstrates using Monitor class for synchronization
        /// </summary>
        private static void MonitorDemo()
        {
            Console.WriteLine("\n=== Monitor Class Demo ===");
            
            // The object to lock on
            object lockObject = new object();
            
            // Reset counter
            _counter = 0;
            
            // Create a list of tasks that will increment the counter
            List<Task> tasks = new List<Task>();
            
            for (int i = 0; i < 5; i++)
            {
                int taskId = i;
                tasks.Add(Task.Run(() => 
                {
                    for (int j = 0; j < 100; j++)
                    {
                        // Try to acquire the lock with timeout
                        bool lockTaken = false;
                        try
                        {
                            // Try to acquire the lock with 100ms timeout
                            Monitor.TryEnter(lockObject, 100, ref lockTaken);
                            
                            if (lockTaken)
                            {
                                // Critical section
                                _counter++;
                                
                                // Simulate some work inside the critical section
                                if (j % 25 == 0)
                                {
                                    Console.WriteLine($"Task {taskId} inside critical section, counter = {_counter}");
                                    Thread.Sleep(10);
                                }
                            }
                            else
                            {
                                Console.WriteLine($"Task {taskId} couldn't acquire lock, giving up for iteration {j}");
                            }
                        }
                        finally
                        {
                            // Release the lock if we acquired it
                            if (lockTaken)
                            {
                                Monitor.Exit(lockObject);
                            }
                        }
                        
                        // Do some work outside the critical section
                        Thread.Sleep(1);
                    }
                }));
            }
            
            // Wait for all tasks to complete
            Task.WaitAll(tasks.ToArray());
            
            Console.WriteLine($"Final counter value: {_counter}");
            
            // Demonstrate Monitor.Wait and Monitor.Pulse for thread coordination
            Console.WriteLine("\nDemonstrating Monitor.Wait and Monitor.Pulse:");
            
            bool isDataReady = false;
            object syncObject = new object();
            
            // Create a consumer thread that waits for data
            Task consumer = Task.Run(() => 
            {
                Console.WriteLine("Consumer: Waiting for data");
                
                lock (syncObject)
                {
                    // Wait until data is ready
                    while (!isDataReady)
                    {
                        Console.WriteLine("Consumer: No data available, waiting...");
                        // Releases the lock and blocks until pulsed
                        Monitor.Wait(syncObject);
                        Console.WriteLine("Consumer: Woke up, checking condition");
                    }
                    
                    Console.WriteLine("Consumer: Data is ready, processing");
                }
            });
            
            // Wait a bit to ensure consumer is waiting
            Thread.Sleep(500);
            
            // Create a producer thread that makes data ready
            Task producer = Task.Run(() => 
            {
                Console.WriteLine("Producer: Working on data");
                
                // Simulate work
                Thread.Sleep(1000);
                
                lock (syncObject)
                {
                    // Make data ready
                    isDataReady = true;
                    Console.WriteLine("Producer: Data is ready, signaling consumer");
                    
                    // Signal a waiting thread
                    Monitor.Pulse(syncObject);
                }
            });
            
            // Wait for both threads to complete
            Task.WaitAll(consumer, producer);
        }
        
        /// <summary>
        /// Demonstrates using Mutex for synchronization
        /// </summary>
        private static void MutexDemo()
        {
            Console.WriteLine("\n=== Mutex Demo ===");
            
            // Create a mutex (initially not owned)
            using Mutex mutex = new Mutex(false, "CSharpThreadsDemoMutex");
            
            // Create a list of tasks that will use the mutex
            List<Task> tasks = new List<Task>();
            
            for (int i = 0; i < 3; i++)
            {
                int taskId = i;
                tasks.Add(Task.Run(() => 
                {
                    for (int j = 0; j < 2; j++)
                    {
                        Console.WriteLine($"Task {taskId}: Waiting for mutex");
                        
                        // Wait for the mutex with timeout
                        bool acquired = mutex.WaitOne(1000);
                        
                        if (acquired)
                        {
                            try
                            {
                                Console.WriteLine($"Task {taskId}: Acquired mutex, working...");
                                
                                // Simulate some work
                                Thread.Sleep(500);
                            }
                            finally
                            {
                                // Release the mutex
                                Console.WriteLine($"Task {taskId}: Releasing mutex");
                                mutex.ReleaseMutex();
                            }
                        }
                        else
                        {
                            Console.WriteLine($"Task {taskId}: Timeout waiting for mutex");
                        }
                        
                        // Do some work outside the mutex
                        Thread.Sleep(200);
                    }
                }));
            }
            
            // Wait for all tasks to complete
            Task.WaitAll(tasks.ToArray());
            
            // Demonstrate a named mutex for cross-process synchronization
            Console.WriteLine("\nNamed mutexes can be used for cross-process synchronization.");
            Console.WriteLine("Try running multiple instances of this program to see the effect.");
        }
        
        /// <summary>
        /// Demonstrates using Semaphore for synchronization
        /// </summary>
        private static void SemaphoreDemo()
        {
            Console.WriteLine("\n=== Semaphore Demo ===");
            
            // Create a semaphore that allows 3 concurrent accesses
            using SemaphoreSlim semaphore = new SemaphoreSlim(3, 3);
            
            // Create a list of tasks that will use the semaphore
            List<Task> tasks = new List<Task>();
            
            for (int i = 0; i < 10; i++)
            {
                int taskId = i;
                tasks.Add(Task.Run(async () => 
                {
                    Console.WriteLine($"Task {taskId}: Waiting for semaphore");
                    
                    // Wait for the semaphore
                    await semaphore.WaitAsync();
                    
                    try
                    {
                        Console.WriteLine($"Task {taskId}: Entered semaphore, working...");
                        
                        // Simulate some work
                        await Task.Delay(1000);
                    }
                    finally
                    {
                        // Release the semaphore
                        Console.WriteLine($"Task {taskId}: Releasing semaphore");
                        semaphore.Release();
                    }
                }));
            }
            
            // Wait for all tasks to complete
            Task.WhenAll(tasks).GetAwaiter().GetResult();
            
            Console.WriteLine("All tasks completed the semaphore demo");
        }
        
        /// <summary>
        /// Demonstrates using ReaderWriterLockSlim for synchronization
        /// </summary>
        private static void ReaderWriterLockDemo()
        {
            Console.WriteLine("\n=== ReaderWriterLockSlim Demo ===");
            
            // Create a reader-writer lock
            using ReaderWriterLockSlim rwLock = new ReaderWriterLockSlim();
            
            // Shared data protected by the reader-writer lock
            int sharedData = 0;
            
            // Create reader tasks
            List<Task> tasks = new List<Task>();
            
            for (int i = 0; i < 5; i++)
            {
                int readerId = i;
                tasks.Add(Task.Run(() => 
                {
                    for (int j = 0; j < 3; j++)
                    {
                        Console.WriteLine($"Reader {readerId}: Waiting for read lock");
                        
                        // Acquire a read lock
                        rwLock.EnterReadLock();
                        
                        try
                        {
                            // Multiple readers can enter simultaneously
                            Console.WriteLine($"Reader {readerId}: Reading data = {sharedData}");
                            
                            // Simulate some reading work
                            Thread.Sleep(100);
                        }
                        finally
                        {
                            // Release the read lock
                            rwLock.ExitReadLock();
                            Console.WriteLine($"Reader {readerId}: Released read lock");
                        }
                        
                        // Wait a bit before next read
                        Thread.Sleep(200);
                    }
                }));
            }
            
            // Create writer tasks
            for (int i = 0; i < 2; i++)
            {
                int writerId = i;
                tasks.Add(Task.Run(() => 
                {
                    for (int j = 0; j < 2; j++)
                    {
                        Console.WriteLine($"Writer {writerId}: Waiting for write lock");
                        
                        // Acquire a write lock (exclusive)
                        rwLock.EnterWriteLock();
                        
                        try
                        {
                            // Only one writer can enter at a time, and no readers can enter
                            int newValue = sharedData + 100 + writerId;
                            Console.WriteLine($"Writer {writerId}: Updating data {sharedData} -> {newValue}");
                            sharedData = newValue;
                            
                            // Simulate some writing work
                            Thread.Sleep(500);
                        }
                        finally
                        {
                            // Release the write lock
                            rwLock.ExitWriteLock();
                            Console.WriteLine($"Writer {writerId}: Released write lock");
                        }
                        
                        // Wait a bit before next write
                        Thread.Sleep(1000);
                    }
                }));
            }
            
            // Wait for all tasks to complete
            Task.WaitAll(tasks.ToArray());
            
            Console.WriteLine($"Final data value: {sharedData}");
        }
        
        /// <summary>
        /// Demonstrates using Barrier for synchronization
        /// </summary>
        private static void BarrierDemo()
        {
            Console.WriteLine("\n=== Barrier Demo ===");
            
            const int participantCount = 3;
            
            // Create a barrier for 3 participants
            using Barrier barrier = new Barrier(
                participantCount, 
                (b) => Console.WriteLine($"All {b.ParticipantCount} threads reached the barrier, phase {b.CurrentPhaseNumber} completed")
            );
            
            List<Task> tasks = new List<Task>();
            
            for (int i = 0; i < participantCount; i++)
            {
                int taskId = i;
                tasks.Add(Task.Run(() => 
                {
                    for (int phase = 0; phase < 3; phase++)
                    {
                        // Simulate different workloads for each participant
                        int workTime = 200 * (taskId + 1);
                        Console.WriteLine($"Task {taskId} performing phase {phase} work ({workTime}ms)");
                        Thread.Sleep(workTime);
                        
                        Console.WriteLine($"Task {taskId} waiting at barrier in phase {phase}");
                        
                        // Wait for all participants to reach the barrier
                        barrier.SignalAndWait();
                        
                        Console.WriteLine($"Task {taskId} passed barrier for phase {phase}");
                    }
                }));
            }
            
            // Wait for all tasks to complete
            Task.WaitAll(tasks.ToArray());
            
            Console.WriteLine("All phases completed");
        }
        
        /// <summary>
        /// Demonstrates using CountdownEvent for synchronization
        /// </summary>
        private static void CountdownEventDemo()
        {
            Console.WriteLine("\n=== CountdownEvent Demo ===");
            
            const int taskCount = 5;
            
            // Create a countdown event with initial count of 5
            using CountdownEvent countdown = new CountdownEvent(taskCount);
            
            // Create a list of worker tasks
            List<Task> workers = new List<Task>();
            
            for (int i = 0; i < taskCount; i++)
            {
                int taskId = i;
                workers.Add(Task.Run(() => 
                {
                    // Simulate work with varying duration
                    int workTime = 300 + taskId * 200;
                    Console.WriteLine($"Worker {taskId} started, will work for {workTime}ms");
                    Thread.Sleep(workTime);
                    
                    // Signal completion
                    Console.WriteLine($"Worker {taskId} completed, signaling countdown event");
                    countdown.Signal();
                }));
            }
            
            // Create a waiter task that waits for all workers to complete
            Task waiter = Task.Run(() => 
            {
                Console.WriteLine("Waiter: Waiting for all workers to complete");
                
                // Wait for the countdown to reach zero
                countdown.Wait();
                
                Console.WriteLine("Waiter: All workers have completed");
            });
            
            // Wait for all tasks to complete
            Task.WaitAll(workers.Concat(new[] { waiter }).ToArray());
        }
        
        /// <summary>
        /// Demonstrates using Interlocked class for atomic operations
        /// </summary>
        private static void InterlockedDemo()
        {
            Console.WriteLine("\n=== Interlocked Demo ===");
            
            // Shared counters
            int counter = 0;
            long longCounter = 0;
            
            // Create a list of tasks
            List<Task> tasks = new List<Task>();
            
            for (int i = 0; i < 10; i++)
            {
                tasks.Add(Task.Run(() => 
                {
                    for (int j = 0; j < 1000; j++)
                    {
                        // Atomic increment
                        Interlocked.Increment(ref counter);
                        
                        // Atomic long increment
                        Interlocked.Increment(ref longCounter);
                    }
                }));
            }
            
            // Wait for all tasks to complete
            Task.WaitAll(tasks.ToArray());
            
            Console.WriteLine($"Final counter value: {counter}");
            Console.WriteLine($"Final long counter value: {longCounter}");
            
            // Demonstrate other Interlocked operations
            int original;
            
            // Atomic exchange
            original = Interlocked.Exchange(ref counter, 100);
            Console.WriteLine($"Interlocked.Exchange: original={original}, new={counter}");
            
            // Atomic compare and exchange
            original = Interlocked.CompareExchange(ref counter, 200, 100);
            Console.WriteLine($"Interlocked.CompareExchange (matching): original={original}, new={counter}");
            
            original = Interlocked.CompareExchange(ref counter, 300, 999);
            Console.WriteLine($"Interlocked.CompareExchange (non-matching): original={original}, new={counter}");
            
            // Atomic add
            original = Interlocked.Add(ref counter, 50);
            Console.WriteLine($"Interlocked.Add: original={original}, new={counter}");
        }
        
        /// <summary>
        /// Demonstrates using ManualResetEvent and AutoResetEvent for synchronization
        /// </summary>
        private static void EventDemo()
        {
            Console.WriteLine("\n=== Event Synchronization Demo ===");
            
            // Create an auto-reset event (automatically resets after each wait)
            using AutoResetEvent autoEvent = new AutoResetEvent(false);
            
            // Create a manual-reset event (stays signaled until manually reset)
            using ManualResetEvent manualEvent = new ManualResetEvent(false);
            
            // Demonstrate AutoResetEvent
            Console.WriteLine("\n1. AutoResetEvent demonstration:");
            
            Task autoSender = Task.Run(() => 
            {
                for (int i = 0; i < 3; i++)
                {
                    Console.WriteLine($"Sender: Working... ({i+1}/3)");
                    Thread.Sleep(500);
                    
                    Console.WriteLine("Sender: Signaling auto-reset event");
                    autoEvent.Set();
                }
            });
            
            Task[] autoWaiters = Enumerable.Range(0, 3).Select(id => 
                Task.Run(() => 
                {
                    Console.WriteLine($"Waiter {id}: Waiting for signal");
                    autoEvent.WaitOne();
                    Console.WriteLine($"Waiter {id}: Received signal, continuing");
                })
            ).ToArray();
            
            // Wait for all auto-event tasks to complete
            Task.WaitAll(new[] { autoSender }.Concat(autoWaiters).ToArray());
            
            // Demonstrate ManualResetEvent
            Console.WriteLine("\n2. ManualResetEvent demonstration:");
            
            Task manualSender = Task.Run(() => 
            {
                Console.WriteLine("Sender: Working...");
                Thread.Sleep(1000);
                
                Console.WriteLine("Sender: Signaling manual-reset event");
                manualEvent.Set();
                
                Thread.Sleep(1000);
                
                Console.WriteLine("Sender: Resetting manual-reset event");
                manualEvent.Reset();
            });
            
            Task[] manualWaiters = Enumerable.Range(0, 3).Select(id => 
                Task.Run(() => 
                {
                    // Add varying delays so waiters start at different times
                    Thread.Sleep(id * 400);
                    
                    Console.WriteLine($"Waiter {id}: Waiting for signal");
                    bool signaled = manualEvent.WaitOne(2000);
                    
                    if (signaled)
                    {
                        Console.WriteLine($"Waiter {id}: Received signal, continuing");
                    }
                    else
                    {
                        Console.WriteLine($"Waiter {id}: Timeout waiting for signal");
                    }
                })
            ).ToArray();
            
            // Wait for all manual-event tasks to complete
            Task.WaitAll(new[] { manualSender }.Concat(manualWaiters).ToArray());
        }
        
        /// <summary>
        /// Run all synchronization demos
        /// </summary>
        public static void RunDemo()
        {
            Console.WriteLine("=== Synchronization Mechanisms Demo ===");
            
            // Run each demo
            LockDemo();
            MonitorDemo();
            MutexDemo();
            SemaphoreDemo();
            ReaderWriterLockDemo();
            BarrierDemo();
            CountdownEventDemo();
            InterlockedDemo();
            EventDemo();
            
            Console.WriteLine("\nSynchronization mechanisms demo completed");
        }
    }
} 