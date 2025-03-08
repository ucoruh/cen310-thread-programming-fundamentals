using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates the Task Parallel Library (TPL) fundamentals
    /// </summary>
    public static class TaskBasics
    {
        /// <summary>
        /// Simple function that returns a result
        /// </summary>
        private static int Calculate(int a, int b)
        {
            Console.WriteLine($"Calculating {a} + {b} on thread {Environment.CurrentManagedThreadId}");
            Thread.Sleep(1000); // Simulate work
            return a + b;
        }
        
        /// <summary>
        /// Demonstrates basic Task creation and execution
        /// </summary>
        private static void BasicTaskDemo()
        {
            Console.WriteLine("\n=== Basic Task Creation and Execution ===");
            Console.WriteLine($"Main thread ID: {Environment.CurrentManagedThreadId}");
            
            // Create and start a simple Task (fire and forget)
            Console.WriteLine("\n1. Fire and forget task:");
            Task simpleTask = Task.Run(() =>
            {
                Console.WriteLine($"Simple task running on thread {Environment.CurrentManagedThreadId}");
                Thread.Sleep(500);
                Console.WriteLine("Simple task completed");
            });
            
            // Wait for the task to complete
            simpleTask.Wait();
            
            // Create a task that returns a value
            Console.WriteLine("\n2. Task with return value:");
            Task<int> resultTask = Task.Run(() => Calculate(10, 20));
            
            // Get the result (blocks until completed)
            Console.WriteLine($"Waiting for result task to complete...");
            int result = resultTask.Result;
            Console.WriteLine($"Result: {result}");
            
            // Create a task using Task.Factory.StartNew
            Console.WriteLine("\n3. Task created with Task.Factory.StartNew:");
            Task factoryTask = Task.Factory.StartNew(() =>
            {
                Console.WriteLine($"Factory task running on thread {Environment.CurrentManagedThreadId}");
                Thread.Sleep(500);
                Console.WriteLine("Factory task completed");
            });
            
            factoryTask.Wait();
        }
        
        /// <summary>
        /// Demonstrates task continuation patterns
        /// </summary>
        private static void TaskContinuationDemo()
        {
            Console.WriteLine("\n=== Task Continuation Demo ===");
            
            // Create an initial task
            Console.WriteLine("Starting initial task...");
            Task<int> initialTask = Task.Run(() =>
            {
                Console.WriteLine($"Initial task running on thread {Environment.CurrentManagedThreadId}");
                Thread.Sleep(1000);
                return 42;
            });
            
            // Add a continuation that uses the result
            Task<string> continuationTask = initialTask.ContinueWith(task =>
            {
                Console.WriteLine($"Continuation task running on thread {Environment.CurrentManagedThreadId}");
                Thread.Sleep(500);
                return $"The answer is {task.Result}";
            });
            
            // Wait for the continuation to complete and get its result
            string finalResult = continuationTask.Result;
            Console.WriteLine($"Final result: {finalResult}");
            
            // Demonstrate conditional continuations
            Console.WriteLine("\nConditional continuation examples:");
            
            // Create a task that will succeed
            Task<int> successTask = Task.Run(() => 100);
            
            // Create a task that will fail
            Task<int> failureTask = Task.Run<int>(() =>
            {
                throw new InvalidOperationException("Task failed intentionally");
#pragma warning disable CS0162 // Unreachable code detected
                return 0; // This line will never execute, but helps the compiler understand the return type
#pragma warning restore CS0162
            });
            
            // Add continuations that only run on success or failure
            successTask
                .ContinueWith(t => Console.WriteLine($"Success continuation: {t.Result}"),
                    TaskContinuationOptions.OnlyOnRanToCompletion)
                .ContinueWith(t => Console.WriteLine("This continuation always runs"));
                
            try
            {
                failureTask
                    .ContinueWith(t => Console.WriteLine("This will not run because the task failed"),
                        TaskContinuationOptions.OnlyOnRanToCompletion);
                
                failureTask
                    .ContinueWith(t => Console.WriteLine($"Failure continuation: {t.Exception?.GetBaseException().Message}"),
                        TaskContinuationOptions.OnlyOnFaulted);
                
                // Wait for all tasks to complete
                Task.WaitAll(successTask, failureTask.ContinueWith(t => { }));
            }
            catch
            {
                // Ignore the exception
            }
        }
        
        /// <summary>
        /// Demonstrates child tasks and parent-child relationships
        /// </summary>
        private static void ChildTasksDemo()
        {
            Console.WriteLine("\n=== Child Tasks Demo ===");
            
            // Create a parent task that spawns child tasks
            Task parentTask = Task.Factory.StartNew(() =>
            {
                Console.WriteLine($"Parent task started on thread {Environment.CurrentManagedThreadId}");
                
                // Create detached child tasks
                var detachedChild = Task.Run(() =>
                {
                    Console.WriteLine($"Detached child task on thread {Environment.CurrentManagedThreadId}");
                    Thread.Sleep(500);
                    Console.WriteLine("Detached child task completed");
                });
                
                // Create attached child tasks using TaskCreationOptions.AttachedToParent
                var attachedChild1 = Task.Factory.StartNew(() =>
                {
                    Console.WriteLine($"Attached child task 1 on thread {Environment.CurrentManagedThreadId}");
                    Thread.Sleep(1000);
                    Console.WriteLine("Attached child task 1 completed");
                }, TaskCreationOptions.AttachedToParent);
                
                var attachedChild2 = Task.Factory.StartNew(() =>
                {
                    Console.WriteLine($"Attached child task 2 on thread {Environment.CurrentManagedThreadId}");
                    Thread.Sleep(800);
                    Console.WriteLine("Attached child task 2 completed");
                }, TaskCreationOptions.AttachedToParent);
                
                Console.WriteLine("Parent task waiting for attached children to complete...");
                // When parent task ends, it will wait for attached children
            });
            
            // Wait for the parent task (which will wait for its attached children)
            Console.WriteLine("Main thread waiting for parent task...");
            parentTask.Wait();
            Console.WriteLine("Parent task (and all attached children) completed");
        }
        
        /// <summary>
        /// Demonstrates use of Task.WhenAll and Task.WhenAny
        /// </summary>
        private static void WaitingForTasksDemo()
        {
            Console.WriteLine("\n=== Waiting for Multiple Tasks Demo ===");
            
            // Create several tasks with different durations
            Task<int> task1 = Task.Run(() =>
            {
                Console.WriteLine("Task 1 starting");
                Thread.Sleep(1000);
                Console.WriteLine("Task 1 completing");
                return 1;
            });
            
            Task<int> task2 = Task.Run(() =>
            {
                Console.WriteLine("Task 2 starting");
                Thread.Sleep(1500);
                Console.WriteLine("Task 2 completing");
                return 2;
            });
            
            Task<int> task3 = Task.Run(() =>
            {
                Console.WriteLine("Task 3 starting");
                Thread.Sleep(800);
                Console.WriteLine("Task 3 completing");
                return 3;
            });
            
            // Demonstrate Task.WhenAny
            Console.WriteLine("\nWaiting for the first task to complete...");
            Task<Task<int>> whenAnyTask = Task.WhenAny(task1, task2, task3);
            Task<int> firstCompleted = whenAnyTask.Result;
            Console.WriteLine($"First task to complete returned: {firstCompleted.Result}");
            
            // Demonstrate Task.WhenAll
            Console.WriteLine("\nWaiting for all tasks to complete...");
            Task<int[]> whenAllTask = Task.WhenAll(task1, task2, task3);
            int[] allResults = whenAllTask.Result;
            Console.WriteLine($"All tasks completed. Results: [{string.Join(", ", allResults)}]");
        }
        
        /// <summary>
        /// Demonstrates task exception handling patterns
        /// </summary>
        private static void TaskExceptionHandlingDemo()
        {
            Console.WriteLine("\n=== Task Exception Handling Demo ===");
            
            // Create a task that throws an exception
            Console.WriteLine("Creating a task that will throw an exception");
            Task faultedTask = Task.Run(() =>
            {
                Console.WriteLine("Task starting - about to throw an exception");
                throw new InvalidOperationException("Deliberate exception for demo purposes");
            });
            
            // Handle the exception using Wait() and try-catch
            Console.WriteLine("\n1. Using try-catch around Wait():");
            try
            {
                faultedTask.Wait();
            }
            catch (AggregateException ae)
            {
                Console.WriteLine($"Caught AggregateException: {ae.InnerExceptions.Count} inner exceptions");
                foreach (var ex in ae.InnerExceptions)
                {
                    Console.WriteLine($"  - {ex.GetType().Name}: {ex.Message}");
                }
            }
            
            // Create another faulted task for the next demo
            Task anotherFaultedTask = Task.Run(() =>
            {
                Console.WriteLine("Another task throwing an exception");
                throw new ArgumentException("Another deliberate exception");
            });
            
            Console.WriteLine("\n2. Checking IsFaulted and Exception properties:");
            // Wait for the task to complete but don't throw exceptions
            anotherFaultedTask.ContinueWith(t => { }).Wait();
            
            if (anotherFaultedTask.IsFaulted)
            {
                Console.WriteLine("Task faulted!");
                if (anotherFaultedTask.Exception != null)
                {
                    var innerException = anotherFaultedTask.Exception.InnerException;
                    Console.WriteLine($"Inner exception: {innerException?.GetType().Name}: {innerException?.Message}");
                }
            }
            
            // Create multiple tasks where some throw exceptions
            Console.WriteLine("\n3. Handling exceptions from multiple tasks:");
            var task1 = Task.Run(() => { throw new InvalidOperationException("Error in task 1"); });
            var task2 = Task.Run(() => { Console.WriteLine("Task 2 runs successfully"); });
            var task3 = Task.Run(() => { throw new ArgumentException("Error in task 3"); });
            
            try
            {
                Task.WaitAll(task1, task2, task3);
            }
            catch (AggregateException ae)
            {
                ae = ae.Flatten(); // Flatten nested AggregateExceptions
                Console.WriteLine($"Caught {ae.InnerExceptions.Count} exceptions from multiple tasks:");
                foreach (var ex in ae.InnerExceptions)
                {
                    Console.WriteLine($"  - {ex.GetType().Name}: {ex.Message}");
                }
            }
        }
        
        /// <summary>
        /// Run all TPL demos
        /// </summary>
        public static void RunDemo()
        {
            Console.WriteLine("=== Task Parallel Library Demo ===");
            
            // Run individual demos
            BasicTaskDemo();
            TaskContinuationDemo();
            ChildTasksDemo();
            WaitingForTasksDemo();
            TaskExceptionHandlingDemo();
            
            Console.WriteLine("\nTask Parallel Library demo completed");
        }
    }
} 