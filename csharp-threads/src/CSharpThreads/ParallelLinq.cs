using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates Parallel LINQ (PLINQ) operations
    /// </summary>
    public static class ParallelLinq
    {
        /// <summary>
        /// Helper method to generate test data
        /// </summary>
        private static IEnumerable<int> GenerateTestData(int count)
        {
            Random random = new Random(42);  // Fixed seed for reproducibility
            for (int i = 0; i < count; i++)
            {
                yield return random.Next(1, 1000);
            }
        }
        
        /// <summary>
        /// Helper method to measure execution time
        /// </summary>
        private static long MeasureExecutionTime(Action action)
        {
            Stopwatch stopwatch = Stopwatch.StartNew();
            action();
            stopwatch.Stop();
            return stopwatch.ElapsedMilliseconds;
        }
        
        /// <summary>
        /// Demonstrates basic PLINQ queries
        /// </summary>
        private static void BasicPLinqDemo()
        {
            Console.WriteLine("\n=== Basic PLINQ Demo ===");
            
            // Create a large data source
            const int dataSize = 10_000_000;
            Console.WriteLine($"Generating test data with {dataSize:N0} elements...");
            var data = GenerateTestData(dataSize).ToArray();
            
            // Compare sequential and parallel processing
            Console.WriteLine("\n1. Simple transformation and filtering");
            
            // Sequential LINQ
            long sequentialTime = MeasureExecutionTime(() =>
            {
                var sequentialResult = data
                    .Where(x => x % 2 == 0)
                    .Select(x => x * x)
                    .Take(5)
                    .ToArray();
                
                Console.WriteLine("Sequential LINQ results (first 5):");
                foreach (var item in sequentialResult)
                {
                    Console.WriteLine($"  {item}");
                }
            });
            
            // Parallel LINQ (PLINQ)
            long parallelTime = MeasureExecutionTime(() =>
            {
                var parallelResult = data
                    .AsParallel()
                    .Where(x => x % 2 == 0)
                    .Select(x => x * x)
                    .Take(5)
                    .ToArray();
                
                Console.WriteLine("Parallel LINQ results (first 5):");
                foreach (var item in parallelResult)
                {
                    Console.WriteLine($"  {item}");
                }
            });
            
            Console.WriteLine($"Sequential execution time: {sequentialTime} ms");
            Console.WriteLine($"Parallel execution time: {parallelTime} ms");
            Console.WriteLine($"Speedup: {(double)sequentialTime / parallelTime:F2}x");
            
            // Note on result ordering
            Console.WriteLine("\n2. Result ordering in PLINQ");
            
            Console.WriteLine("Sequential results are ordered by definition:");
            var sequentialOrdered = data.Take(5).ToArray();
            for (int i = 0; i < sequentialOrdered.Length; i++)
            {
                Console.WriteLine($"  Element {i}: {sequentialOrdered[i]}");
            }
            
            Console.WriteLine("Parallel results may not preserve order:");
            var parallelUnordered = data.AsParallel().Take(5).ToArray();
            for (int i = 0; i < parallelUnordered.Length; i++)
            {
                Console.WriteLine($"  Element {i}: {parallelUnordered[i]}");
            }
            
            Console.WriteLine("Use AsOrdered() to preserve original order:");
            var parallelOrdered = data.AsParallel().AsOrdered().Take(5).ToArray();
            for (int i = 0; i < parallelOrdered.Length; i++)
            {
                Console.WriteLine($"  Element {i}: {parallelOrdered[i]}");
            }
        }
        
        /// <summary>
        /// Demonstrates aggregation operations with PLINQ
        /// </summary>
        private static void AggregationDemo()
        {
            Console.WriteLine("\n=== PLINQ Aggregation Demo ===");
            
            // Generate large test data
            const int dataSize = 50_000_000;
            var data = GenerateTestData(dataSize).ToArray();
            
            // Sequential sum
            long sequentialTime = MeasureExecutionTime(() =>
            {
                int sequentialSum = data.Sum();
                Console.WriteLine($"Sequential Sum: {sequentialSum:N0}");
            });
            
            // Parallel sum
            long parallelTime = MeasureExecutionTime(() =>
            {
                int parallelSum = data.AsParallel().Sum();
                Console.WriteLine($"Parallel Sum: {parallelSum:N0}");
            });
            
            Console.WriteLine($"Sequential execution time: {sequentialTime} ms");
            Console.WriteLine($"Parallel execution time: {parallelTime} ms");
            Console.WriteLine($"Speedup: {(double)sequentialTime / parallelTime:F2}x");
            
            // Other aggregation operators
            Console.WriteLine("\nOther PLINQ Aggregation Operators:");
            
            // Count
            int evenCount = data.AsParallel().Count(x => x % 2 == 0);
            Console.WriteLine($"Count of even numbers: {evenCount:N0}");
            
            // Min/Max
            int minValue = data.AsParallel().Min();
            int maxValue = data.AsParallel().Max();
            Console.WriteLine($"Min value: {minValue}, Max value: {maxValue}");
            
            // Average
            double average = data.AsParallel().Average();
            Console.WriteLine($"Average value: {average:F2}");
            
            // Custom aggregation with Aggregate
            long sequentialAggregateTime = MeasureExecutionTime(() =>
            {
                var result = data.Aggregate(
                    new { Sum = 0, Count = 0 },
                    (acc, value) => new { Sum = acc.Sum + value, Count = acc.Count + 1 },
                    acc => (double)acc.Sum / acc.Count
                );
                
                Console.WriteLine($"Sequential custom aggregate (avg): {result:F2}");
            });
            
            // Parallel custom aggregation
            long parallelAggregateTime = MeasureExecutionTime(() =>
            {
                var result = data.AsParallel().Aggregate(
                    () => new { Sum = 0, Count = 0 },                             // Thread-local seed
                    (acc, value) => new { Sum = acc.Sum + value, Count = acc.Count + 1 }, // Thread-local update
                    (acc1, acc2) => new { Sum = acc1.Sum + acc2.Sum, Count = acc1.Count + acc2.Count },   // Merge thread-local results
                    acc => (double)acc.Sum / acc.Count                            // Final projection
                );
                
                Console.WriteLine($"Parallel custom aggregate (avg): {result:F2}");
            });
            
            Console.WriteLine($"Sequential aggregate time: {sequentialAggregateTime} ms");
            Console.WriteLine($"Parallel aggregate time: {parallelAggregateTime} ms");
            Console.WriteLine($"Speedup: {(double)sequentialAggregateTime / parallelAggregateTime:F2}x");
        }
        
        /// <summary>
        /// Demonstrates custom degree of parallelism
        /// </summary>
        private static void DegreeOfParallelismDemo()
        {
            Console.WriteLine("\n=== Degree of Parallelism Demo ===");
            
            // Get the number of logical processors
            int processorCount = Environment.ProcessorCount;
            Console.WriteLine($"Number of logical processors: {processorCount}");
            
            // Generate test data
            const int dataSize = 20_000_000;
            var data = GenerateTestData(dataSize).ToArray();
            
            // Create a CPU-intensive operation
            Func<int, int> cpuIntensiveOperation = x =>
            {
                // Simulate computation by calculating multiple square roots
                double result = 0;
                for (int i = 0; i < 100; i++)
                {
                    result += Math.Sqrt(x + i);
                }
                Thread.Sleep(1); // Add a small delay to make the effect more visible
                return (int)result;
            };
            
            // Test with different degrees of parallelism
            foreach (int degreeOfParallelism in new[] { 1, 2, processorCount, processorCount * 2 })
            {
                Console.WriteLine($"\nUsing {degreeOfParallelism} threads:");
                
                long executionTime = MeasureExecutionTime(() =>
                {
                    var result = data
                        .AsParallel()
                        .WithDegreeOfParallelism(degreeOfParallelism)
                        .Select(cpuIntensiveOperation)
                        .Average();
                    
                    Console.WriteLine($"Result: {result:F2}");
                });
                
                Console.WriteLine($"Execution time: {executionTime} ms");
            }
            
            Console.WriteLine("\nNotes on Degree of Parallelism:");
            Console.WriteLine("- Default: Usually matches the number of available processors");
            Console.WriteLine("- Set higher for I/O-bound operations");
            Console.WriteLine("- Set lower to reduce resource consumption");
            Console.WriteLine("- Too many threads can lead to overhead from context switching");
        }
        
        /// <summary>
        /// Demonstrates exception handling in PLINQ
        /// </summary>
        private static void ExceptionHandlingDemo()
        {
            Console.WriteLine("\n=== PLINQ Exception Handling Demo ===");
            
            // Create a data source
            var data = Enumerable.Range(0, 100).ToArray();
            
            // Query that might throw exceptions
            Console.WriteLine("1. Handling exceptions with try-catch:");
            try
            {
                var result = data
                    .AsParallel()
                    .Select(x => 
                    {
                        // Throw for specific values to simulate failures
                        if (x % 25 == 0 && x > 0)
                            throw new DivideByZeroException($"Simulated error at x={x}");
                            
                        return 100 / (x % 5); // Will also throw when x % 5 == 0
                    })
                    .ToArray(); // Force execution
                
                Console.WriteLine("Query completed without exceptions (shouldn't happen)");
            }
            catch (AggregateException ae)
            {
                Console.WriteLine($"Caught AggregateException with {ae.InnerExceptions.Count} inner exceptions:");
                foreach (var inner in ae.InnerExceptions)
                {
                    Console.WriteLine($"  - {inner.GetType().Name}: {inner.Message}");
                }
            }
            
            // Using a custom exception handler
            Console.WriteLine("\n2. Continue processing with exception handling:");
            
            var resultWithHandling = data
                .AsParallel()
                .Select(x => 
                {
                    try
                    {
                        if (x % 25 == 0 && x > 0)
                            throw new DivideByZeroException($"Simulated error at x={x}");
                            
                        return 100 / (x % 5); // Will also throw when x % 5 == 0
                    }
                    catch (Exception)
                    {
                        // Return a default value instead of throwing
                        return -1;
                    }
                })
                .Where(result => result >= 0) // Filter out error values
                .ToArray();
            
            Console.WriteLine($"Completed with error handling, processed {resultWithHandling.Length} items");
            Console.WriteLine($"First few results: {string.Join(", ", resultWithHandling.Take(10))}");
        }
        
        /// <summary>
        /// Demonstrates cancellation support in PLINQ
        /// </summary>
        private static void CancellationDemo()
        {
            Console.WriteLine("\n=== PLINQ Cancellation Demo ===");
            
            // Create a large data source to ensure the query takes some time
            var largeData = Enumerable.Range(1, 10_000_000).ToArray();
            
            // Create a cancellation token source
            using var cts = new CancellationTokenSource();
            
            // Start a task to cancel after a delay
            Task.Run(() =>
            {
                Thread.Sleep(100); // Wait a bit
                Console.WriteLine("Cancelling PLINQ operation...");
                cts.Cancel();
            });
            
            try
            {
                Console.WriteLine("Starting long-running PLINQ query...");
                
                // Start the PLINQ query with cancellation support
                var result = largeData
                    .AsParallel()
                    .WithCancellation(cts.Token)
                    .Select(x => 
                    {
                        // Simulate a time-consuming operation
                        Thread.Sleep(1);
                        return x * x;
                    })
                    .ToArray(); // Force execution
                
                Console.WriteLine("Query completed successfully (shouldn't happen)");
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Query was successfully canceled");
            }
            
            // Demonstrate how to implement custom cancellation check
            Console.WriteLine("\nCustom cancellation checks within operations:");
            
            using var cts2 = new CancellationTokenSource();
            cts2.CancelAfter(200); // Cancel after 200ms
            
            try
            {
                var result = largeData
                    .AsParallel()
                    .WithCancellation(cts2.Token)
                    .Select(x => 
                    {
                        // Periodically check for cancellation in long-running operations
                        if (x % 1000 == 0)
                            cts2.Token.ThrowIfCancellationRequested();
                            
                        // Simulate work
                        double sum = 0;
                        for (int i = 0; i < 1000; i++)
                        {
                            sum += Math.Sqrt(x + i);
                        }
                        
                        return sum;
                    })
                    .ToArray();
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Custom cancellation check succeeded");
            }
        }
        
        /// <summary>
        /// Demonstrates when to use PLINQ
        /// </summary>
        private static void WhenToUsePLinqDemo()
        {
            Console.WriteLine("\n=== When to Use PLINQ ===");
            
            Console.WriteLine("PLINQ works best when:");
            Console.WriteLine("1. Data source is large (millions of items)");
            Console.WriteLine("2. Operations are CPU-intensive");
            Console.WriteLine("3. Operations take roughly equal time per element");
            Console.WriteLine("4. Order of results doesn't matter (unless AsOrdered is used)");
            
            Console.WriteLine("\nPLINQ may not help or could be slower when:");
            Console.WriteLine("1. Data source is small");
            Console.WriteLine("2. Operations are I/O-bound (use async/await instead)");
            Console.WriteLine("3. Operations have large variations in execution time");
            Console.WriteLine("4. The overhead of parallelization exceeds the benefits");
            
            // Demonstrate a case where PLINQ is slower
            const int smallDataSize = 1000;
            var smallData = Enumerable.Range(1, smallDataSize).ToArray();
            
            Console.WriteLine($"\nDemonstration with small data set ({smallDataSize} items):");
            
            // Sequential LINQ
            long sequentialTime = MeasureExecutionTime(() =>
            {
                var result = smallData
                    .Where(x => x % 2 == 0)
                    .Select(x => x * x)
                    .ToArray();
            });
            
            // Parallel LINQ
            long parallelTime = MeasureExecutionTime(() =>
            {
                var result = smallData
                    .AsParallel()
                    .Where(x => x % 2 == 0)
                    .Select(x => x * x)
                    .ToArray();
            });
            
            Console.WriteLine($"Sequential execution time: {sequentialTime} ms");
            Console.WriteLine($"Parallel execution time: {parallelTime} ms");
            Console.WriteLine(parallelTime > sequentialTime 
                ? "PLINQ was slower due to parallelization overhead with small data set"
                : "PLINQ was faster despite small data set");
            
            // Demonstrate a case where PLINQ is significantly faster
            const int largeDataSize = 10_000_000;
            var largeData = Enumerable.Range(1, largeDataSize).ToArray();
            
            Console.WriteLine($"\nDemonstration with large data set ({largeDataSize:N0} items) and CPU-intensive operation:");
            
            Func<int, double> cpuIntensiveOperation = x =>
            {
                double result = 0;
                for (int i = 0; i < 20; i++)
                {
                    result += Math.Sqrt(x + i);
                }
                return result;
            };
            
            // Sequential LINQ
            sequentialTime = MeasureExecutionTime(() =>
            {
                var result = largeData
                    .Where(x => x % 2 == 0)
                    .Select(cpuIntensiveOperation)
                    .Take(5)
                    .ToArray();
            });
            
            // Parallel LINQ
            parallelTime = MeasureExecutionTime(() =>
            {
                var result = largeData
                    .AsParallel()
                    .Where(x => x % 2 == 0)
                    .Select(cpuIntensiveOperation)
                    .Take(5)
                    .ToArray();
            });
            
            Console.WriteLine($"Sequential execution time: {sequentialTime} ms");
            Console.WriteLine($"Parallel execution time: {parallelTime} ms");
            Console.WriteLine($"Speedup: {(double)sequentialTime / parallelTime:F2}x");
        }
        
        /// <summary>
        /// Demonstrates parallel query execution optimization
        /// </summary>
        private static void OptimizationDemo()
        {
            Console.WriteLine("\n=== PLINQ Optimization Techniques ===");
            
            const int dataSize = 10_000_000;
            var data = Enumerable.Range(1, dataSize).ToArray();
            
            Console.WriteLine("1. ForAll for side effects instead of foreach:");
            
            long foreachTime = MeasureExecutionTime(() =>
            {
                int count = 0;
                foreach (var item in data.AsParallel().Where(x => x % 2 == 0))
                {
                    Interlocked.Increment(ref count);
                }
                Console.WriteLine($"Counted {count:N0} even numbers using foreach");
            });
            
            long forAllTime = MeasureExecutionTime(() =>
            {
                int count = 0;
                data.AsParallel().Where(x => x % 2 == 0).ForAll(item =>
                {
                    Interlocked.Increment(ref count);
                });
                Console.WriteLine($"Counted {count:N0} even numbers using ForAll");
            });
            
            Console.WriteLine($"foreach time: {foreachTime} ms");
            Console.WriteLine($"ForAll time: {forAllTime} ms");
            Console.WriteLine($"Speedup: {(double)foreachTime / forAllTime:F2}x");
            
            Console.WriteLine("\n2. Optimizing query structure:");
            
            // Suboptimal: filtering after expensive operation
            long suboptimalTime = MeasureExecutionTime(() =>
            {
                var result = data
                    .AsParallel()
                    .Select(x => 
                    {
                        // Expensive operation done for all items
                        double sum = 0;
                        for (int i = 0; i < 50; i++)
                        {
                            sum += Math.Sqrt(x + i);
                        }
                        return sum;
                    })
                    .Where(result => result > 100) // Filter after expensive calculation
                    .Take(10)
                    .ToArray();
            });
            
            // Optimal: filter before expensive operation
            long optimalTime = MeasureExecutionTime(() =>
            {
                var result = data
                    .AsParallel()
                    .Where(x => x > 500) // Simple filter first to reduce workload
                    .Select(x => 
                    {
                        // Expensive operation done for fewer items
                        double sum = 0;
                        for (int i = 0; i < 50; i++)
                        {
                            sum += Math.Sqrt(x + i);
                        }
                        return sum;
                    })
                    .Take(10)
                    .ToArray();
            });
            
            Console.WriteLine($"Suboptimal query time: {suboptimalTime} ms");
            Console.WriteLine($"Optimized query time: {optimalTime} ms");
            Console.WriteLine($"Improvement: {(double)suboptimalTime / optimalTime:F2}x faster");
            
            Console.WriteLine("\n3. Partitioning strategies with .WithMergeOptions:");
            
            foreach (var option in Enum.GetValues(typeof(ParallelMergeOptions)))
            {
                long mergeTime = MeasureExecutionTime(() =>
                {
                    var result = data
                        .AsParallel()
                        .WithMergeOptions((ParallelMergeOptions)option)
                        .Where(x => x % 2 == 0)
                        .Select(x => Math.Sqrt(x))
                        .ToArray();
                });
                
                Console.WriteLine($"Time with {option}: {mergeTime} ms");
            }
            
            Console.WriteLine("\nKey PLINQ best practices:");
            Console.WriteLine("- Filter early to reduce workload");
            Console.WriteLine("- Use AsOrdered() only when necessary (has performance cost)");
            Console.WriteLine("- Use AsUnordered() to optimize when order doesn't matter");
            Console.WriteLine("- Use ForAll() instead of foreach for side effects");
            Console.WriteLine("- Adjust DegreeOfParallelism based on workload characteristics");
            Console.WriteLine("- Choose appropriate merge options for output handling");
        }
        
        /// <summary>
        /// Runs all the PLINQ demos
        /// </summary>
        public static void RunDemo()
        {
            Console.WriteLine("=== Parallel LINQ (PLINQ) Demo ===");
            
            BasicPLinqDemo();
            AggregationDemo();
            DegreeOfParallelismDemo();
            ExceptionHandlingDemo();
            CancellationDemo();
            WhenToUsePLinqDemo();
            OptimizationDemo();
            
            Console.WriteLine("\nParallel LINQ demo completed");
        }
    }
} 