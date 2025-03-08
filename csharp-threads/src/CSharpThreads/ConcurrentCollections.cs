using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates thread-safe concurrent collections in C#
    /// </summary>
    public static class ConcurrentCollections
    {
        /// <summary>
        /// Demonstrates ConcurrentDictionary
        /// </summary>
        private static void ConcurrentDictionaryDemo()
        {
            Console.WriteLine("\n=== ConcurrentDictionary Demo ===");
            
            // Create a concurrent dictionary
            var concurrentDict = new ConcurrentDictionary<int, string>();
            
            // Add items concurrently
            Console.WriteLine("Adding items concurrently...");
            
            // Parallel operations to add items
            Parallel.For(0, 100, i =>
            {
                // TryAdd - will not throw if key already exists
                if (concurrentDict.TryAdd(i, $"Value-{i}"))
                {
                    //Console.WriteLine($"Added key {i}");
                }
                else
                {
                    Console.WriteLine($"Failed to add key {i} (already exists)");
                }
                
                // AddOrUpdate - adds if key doesn't exist, or updates if it does
                string newValue = concurrentDict.AddOrUpdate(
                    i + 100,                              // key
                    k => $"New-{k}",                      // add value factory
                    (k, oldValue) => $"Updated-{oldValue}" // update value factory
                );
                
                //Console.WriteLine($"AddOrUpdate for key {i + 100}: {newValue}");
            });
            
            Console.WriteLine($"ConcurrentDictionary contains {concurrentDict.Count} items");
            
            // GetOrAdd demonstration
            Parallel.For(0, 10, i =>
            {
                string value = concurrentDict.GetOrAdd(i * 50, k => $"GetOrAdd-{k}");
                Console.WriteLine($"GetOrAdd for key {i * 50}: {value}");
            });
            
            // Safe enumeration while other threads might modify
            Console.WriteLine("\nSafe enumeration of ConcurrentDictionary");
            foreach (var kvp in concurrentDict.Take(5))
            {
                Console.WriteLine($"Key: {kvp.Key}, Value: {kvp.Value}");
            }
            
            // Thread-safe removal
            Console.WriteLine("\nRemoving items concurrently...");
            Parallel.For(0, 20, i =>
            {
                // TryRemove - thread-safe removal
#pragma warning disable CS8600 // Converting null literal or possible null value to non-nullable type
                if (concurrentDict.TryRemove(i, out string removedValue))
                {
                    //Console.WriteLine($"Removed key {i} with value {removedValue}");
                }
#pragma warning restore CS8600
            });
            
            Console.WriteLine($"After removal, dictionary contains {concurrentDict.Count} items");
        }
        
        /// <summary>
        /// Demonstrates ConcurrentQueue
        /// </summary>
        private static void ConcurrentQueueDemo()
        {
            Console.WriteLine("\n=== ConcurrentQueue Demo ===");
            
            // Create a concurrent queue
            var concurrentQueue = new ConcurrentQueue<int>();
            
            // Producer task adds items to the queue
            Task producer = Task.Run(() =>
            {
                Console.WriteLine("Producer: Adding items to queue");
                
                for (int i = 0; i < 20; i++)
                {
                    concurrentQueue.Enqueue(i);
                    Console.WriteLine($"Producer: Enqueued {i}, queue count: {concurrentQueue.Count}");
                    Thread.Sleep(100);
                }
            });
            
            // Consumer tasks remove items from the queue
            Task[] consumers = new Task[2];
            for (int i = 0; i < consumers.Length; i++)
            {
                int consumerId = i;
                consumers[i] = Task.Run(() =>
                {
                    Console.WriteLine($"Consumer {consumerId}: Starting to dequeue items");
                    
                    int processedCount = 0;
                    
                    // Try to dequeue items until we've received enough or timeout
                    Stopwatch sw = Stopwatch.StartNew();
                    
                    while (processedCount < 10 && sw.ElapsedMilliseconds < 3000)
                    {
                        // TryDequeue is thread-safe - doesn't throw if queue is empty
                        if (concurrentQueue.TryDequeue(out int item))
                        {
                            Console.WriteLine($"Consumer {consumerId}: Dequeued {item}, remaining: {concurrentQueue.Count}");
                            processedCount++;
                            
                            // Simulate processing
                            Thread.Sleep(200);
                        }
                        else
                        {
                            // Queue is empty, wait a bit before trying again
                            Thread.Sleep(50);
                        }
                    }
                    
                    Console.WriteLine($"Consumer {consumerId}: Finished, processed {processedCount} items");
                });
            }
            
            // Wait for all tasks to complete
            Task.WaitAll(producer);
            Task.WaitAll(consumers);
            
            // Check what's left in the queue
            Console.WriteLine($"Queue finished with {concurrentQueue.Count} items remaining");
            
            // Peek demonstration
#pragma warning disable CS8600 // Converting null literal or possible null value to non-nullable type
            if (concurrentQueue.TryPeek(out int peekedItem))
            {
                Console.WriteLine($"Next item in queue is {peekedItem} (without removing it)");
            }
#pragma warning restore CS8600
            
            // Safe enumeration
            Console.WriteLine("\nRemaining items in queue:");
            foreach (int item in concurrentQueue)
            {
                Console.WriteLine($"Item: {item}");
            }
        }
        
        /// <summary>
        /// Demonstrates ConcurrentStack
        /// </summary>
        private static void ConcurrentStackDemo()
        {
            Console.WriteLine("\n=== ConcurrentStack Demo ===");
            
            // Create a concurrent stack
            var concurrentStack = new ConcurrentStack<string>();
            
            // Push items onto the stack
            Console.WriteLine("Pushing items onto the stack...");
            
            for (int i = 0; i < 5; i++)
            {
                concurrentStack.Push($"Item-{i}");
                Console.WriteLine($"Pushed: Item-{i}, Stack count: {concurrentStack.Count}");
            }
            
            // Push multiple items at once
            var itemsToPush = new[] { "Batch-0", "Batch-1", "Batch-2" };
            concurrentStack.PushRange(itemsToPush);
            Console.WriteLine($"Pushed batch of {itemsToPush.Length} items, Stack count: {concurrentStack.Count}");
            
            // Pop items from the stack
            Console.WriteLine("\nPopping items from the stack...");
            
            for (int i = 0; i < 3; i++)
            {
                // TryPop - thread-safe removal
#pragma warning disable CS8600 // Converting null literal or possible null value to non-nullable type
                if (concurrentStack.TryPop(out string poppedItem))
                {
                    Console.WriteLine($"Popped: {poppedItem}, Stack count: {concurrentStack.Count}");
                }
#pragma warning restore CS8600
            }
            
            // Pop multiple items at once
            string[] poppedItems = new string[2];
            int popped = concurrentStack.TryPopRange(poppedItems);
            Console.WriteLine($"Popped batch of {popped} items:");
            for (int i = 0; i < popped; i++)
            {
                Console.WriteLine($" - {poppedItems[i]}");
            }
            
            // Peek demonstration
#pragma warning disable CS8600 // Converting null literal or possible null value to non-nullable type
            if (concurrentStack.TryPeek(out string peekedItem))
            {
                Console.WriteLine($"\nTop item on stack is {peekedItem} (without removing it)");
            }
#pragma warning restore CS8600
            
            // Parallel operations
            Console.WriteLine("\nPerforming concurrent push/pop operations...");
            var newStack = new ConcurrentStack<int>();
            
            Parallel.For(0, 1000, i =>
            {
                newStack.Push(i);
                
                // Half the time also pop
                if (i % 2 == 0)
                {
                    newStack.TryPop(out _);
                }
            });
            
            Console.WriteLine($"After concurrent operations, stack contains {newStack.Count} items");
        }
        
        /// <summary>
        /// Demonstrates ConcurrentBag
        /// </summary>
        private static void ConcurrentBagDemo()
        {
            Console.WriteLine("\n=== ConcurrentBag Demo ===");
            
            // Create a concurrent bag
            var bag = new ConcurrentBag<int>();
            
            // Add items concurrently
            Console.WriteLine("Adding items to bag from multiple threads...");
            
            Parallel.For(0, 100, i =>
            {
                bag.Add(i);
                
                // Simulate some other operations
                Thread.Sleep(10);
            });
            
            Console.WriteLine($"Bag contains {bag.Count} items");
            
            // Take items from the bag
            Console.WriteLine("\nTaking items from bag...");
            var takenItems = new List<int>();
            
            for (int i = 0; i < 10; i++)
            {
                if (bag.TryTake(out int item))
                {
                    takenItems.Add(item);
                }
            }
            
            Console.WriteLine($"Took {takenItems.Count} items from bag: {string.Join(", ", takenItems.Take(5))}...");
            Console.WriteLine($"Bag now contains {bag.Count} items");
            
            // Peek demonstration
#pragma warning disable CS8600 // Converting null literal or possible null value to non-nullable type
            if (bag.TryPeek(out int peekedItem))
            {
                Console.WriteLine($"\nPeeked item from bag: {peekedItem} (not removed)");
            }
#pragma warning restore CS8600
            
            // Characteristics of ConcurrentBag
            Console.WriteLine("\nConcurrentBag characteristics:");
            Console.WriteLine("- Optimized for scenarios where same thread adds and removes items");
            Console.WriteLine("- No ordering guarantees (unlike Queue or Stack)");
            Console.WriteLine("- Thread-local storage optimizations for better performance");
            
            // Demonstrate thread-locality optimization
            Console.WriteLine("\nDemonstrating thread-local optimization:");
            
            var tasks = new Task<int>[Environment.ProcessorCount];
            var localBag = new ConcurrentBag<int>();
            
            for (int i = 0; i < tasks.Length; i++)
            {
                tasks[i] = Task.Run(() =>
                {
                    int threadId = Environment.CurrentManagedThreadId;
                    
                    // Add items from this thread
                    for (int j = 0; j < 1000; j++)
                    {
                        localBag.Add(threadId * 10000 + j);
                    }
                    
                    int taken = 0;
                    
                    // Take items (preferably added by same thread)
                    for (int j = 0; j < 800; j++)
                    {
                        if (localBag.TryTake(out _))
                        {
                            taken++;
                        }
                    }
                    
                    return taken;
                });
            }
            
            Task.WaitAll(tasks);
            
            Console.WriteLine($"Each thread took back most of its items efficiently");
            Console.WriteLine($"Bag contains {localBag.Count} items after operations");
        }
        
        /// <summary>
        /// Demonstrates BlockingCollection
        /// </summary>
        private static void BlockingCollectionDemo()
        {
            Console.WriteLine("\n=== BlockingCollection Demo ===");
            
            // Create a blocking collection with bounded capacity
            int capacity = 5;
            using var blockingCollection = new BlockingCollection<int>(capacity);
            
            Console.WriteLine($"Created BlockingCollection with capacity of {capacity} items");
            
            // Create a cancellation token source
            using var cts = new CancellationTokenSource();
            CancellationToken token = cts.Token;
            
            // Producer task
            Task producer = Task.Run(() =>
            {
                try
                {
                    for (int i = 0; i < 20; i++)
                    {
                        // Add with blocking behavior
                        Console.WriteLine($"Producer: Adding item {i}...");
                        
                        // This will block if collection reaches capacity
                        blockingCollection.Add(i, token);
                        
                        Console.WriteLine($"Producer: Added {i}, count: {blockingCollection.Count}");
                        Thread.Sleep(100);
                    }
                    
                    // Mark as complete
                    blockingCollection.CompleteAdding();
                    Console.WriteLine("Producer: Marked collection as complete for adding");
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("Producer: Operation was canceled");
                }
            }, token);
            
            // Consumer tasks
            Task[] consumers = new Task[2];
            for (int i = 0; i < consumers.Length; i++)
            {
                int consumerId = i;
                consumers[i] = Task.Run(() =>
                {
                    try
                    {
                        // A slightly different consumption rate for each consumer
                        int delay = 300 + (consumerId * 100);
                        
                        Console.WriteLine($"Consumer {consumerId}: Starting (delay: {delay}ms)");
                        
                        // GetConsumingEnumerable returns items until the collection is marked as complete
                        foreach (int item in blockingCollection.GetConsumingEnumerable(token))
                        {
                            Console.WriteLine($"Consumer {consumerId}: Processing item {item}, count: {blockingCollection.Count}");
                            Thread.Sleep(delay);
                        }
                        
                        Console.WriteLine($"Consumer {consumerId}: Collection completed, no more items");
                    }
                    catch (OperationCanceledException)
                    {
                        Console.WriteLine($"Consumer {consumerId}: Operation was canceled");
                    }
                }, token);
            }
            
            Console.WriteLine("Press Enter to cancel all operations...");
            Console.ReadLine();
            
            // If user pressed enter, cancel operations
            if (!blockingCollection.IsAddingCompleted)
            {
                Console.WriteLine("Canceling producer and consumer operations...");
                cts.Cancel();
            }
            
            try
            {
                Task.WaitAll(producer);
                Task.WaitAll(consumers);
            }
            catch (AggregateException)
            {
                Console.WriteLine("Some tasks were canceled");
            }
            
            Console.WriteLine("BlockingCollection demo completed");
        }
        
        /// <summary>
        /// Demonstrates how to choose the right concurrent collection
        /// </summary>
        private static void ChoosingCollectionDemo()
        {
            Console.WriteLine("\n=== Choosing the Right Concurrent Collection ===");
            
            Console.WriteLine("1. ConcurrentDictionary: Key-value pairs with fast lookups");
            Console.WriteLine("   - Use when: You need to associate keys with values with thread safety");
            Console.WriteLine("   - Unique features: Atomic GetOrAdd, AddOrUpdate operations");
            
            Console.WriteLine("\n2. ConcurrentQueue: First-in, first-out (FIFO) behavior");
            Console.WriteLine("   - Use when: You need ordered processing (first added, first processed)");
            Console.WriteLine("   - Common scenarios: Work queues, message passing between threads");
            
            Console.WriteLine("\n3. ConcurrentStack: Last-in, first-out (LIFO) behavior");
            Console.WriteLine("   - Use when: You need to process newest items first");
            Console.WriteLine("   - Unique features: PushRange, TryPopRange for batch operations");
            
            Console.WriteLine("\n4. ConcurrentBag: Unordered collection");
            Console.WriteLine("   - Use when: Order doesn't matter, same thread adds and takes items");
            Console.WriteLine("   - Unique features: Thread-local caching optimization");
            
            Console.WriteLine("\n5. BlockingCollection: Blocking behavior with bounded capacity");
            Console.WriteLine("   - Use when: You need producer-consumer patterns with flow control");
            Console.WriteLine("   - Unique features: Blocking behavior, cancellation support");
            
            Console.WriteLine("\nPerformance Considerations:");
            Console.WriteLine("- ConcurrentDictionary: Fast lookups, higher memory usage");
            Console.WriteLine("- ConcurrentQueue/Stack: Good for high throughput scenarios");
            Console.WriteLine("- ConcurrentBag: Best when same thread adds and removes");
            Console.WriteLine("- BlockingCollection: Overhead due to synchronization primitives");
        }
        
        /// <summary>
        /// Runs the concurrent collections demos
        /// </summary>
        public static void RunDemo()
        {
            Console.WriteLine("=== Concurrent Collections Demo ===");
            
            // Run the demos
            ConcurrentDictionaryDemo();
            ConcurrentQueueDemo();
            ConcurrentStackDemo();
            ConcurrentBagDemo();
            BlockingCollectionDemo();
            ChoosingCollectionDemo();
            
            Console.WriteLine("\nConcurrent collections demo completed");
        }
    }
} 