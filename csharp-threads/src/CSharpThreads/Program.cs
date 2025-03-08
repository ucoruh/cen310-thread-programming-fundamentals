using System;
using System.Threading;

namespace CSharpThreads
{
    /// <summary>
    /// Main program entry point for C# Threading demos
    /// </summary>
    class Program
    {
        /// <summary>
        /// Display the main menu
        /// </summary>
        static void DisplayMenu()
        {
            Console.WriteLine("\n=== C# Threading Programming Demo Menu ===");
            Console.WriteLine("1. Basic Threading (System.Threading.Thread)");
            Console.WriteLine("2. Task Parallel Library (TPL) Basics");
            Console.WriteLine("3. Async/Await Patterns");
            Console.WriteLine("4. Synchronization Mechanisms");
            Console.WriteLine("5. Thread Pooling");
            Console.WriteLine("6. Concurrent Collections");
            Console.WriteLine("7. Parallel LINQ (PLINQ)");
            Console.WriteLine("8. Cancellation and Coordination");
            Console.WriteLine("9. Exception Handling and Error Demos");
            Console.WriteLine("10. Run All Demos");
            Console.WriteLine("0. Exit");
            Console.Write("Enter your choice: ");
        }

        /// <summary>
        /// Main entry point
        /// </summary>
        static void Main(string[] args)
        {
            // Set console output and input encoding to UTF-8
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            Console.InputEncoding = System.Text.Encoding.UTF8;

            // Show basic info
            Console.WriteLine($"C# Threading Demos");
            Console.WriteLine($"Running on .NET {Environment.Version}");
            Console.WriteLine($"Process ID: {Environment.ProcessId}");
            Console.WriteLine($"Thread ID: {Environment.CurrentManagedThreadId}");
            Console.WriteLine($"Processor Count: {Environment.ProcessorCount}");
            
            bool runAll = args.Length > 0 && args[0] == "--run-all";
            
            if (runAll)
            {
                // Run all demos sequentially
                BasicThreading.RunDemo();
                TaskBasics.RunDemo();
                AsyncAwaitPatterns.RunDemo();
                SynchronizationDemo.RunDemo();
                ThreadPooling.RunDemo();
                ConcurrentCollections.RunDemo();
                ParallelLinq.RunDemo();
                CancellationDemo.RunDemo();
                
                Console.WriteLine("\nAll demos completed successfully.");
            }
            else
            {
                // Interactive mode with menu
                int choice;
                do
                {
                    DisplayMenu();
                    if (!int.TryParse(Console.ReadLine(), out choice))
                    {
                        choice = -1;
                    }
                    
                    Console.WriteLine();
                    
                    try
                    {
                        switch (choice)
                        {
                            case 0:
                                Console.WriteLine("Exiting demo program. Goodbye!");
                                break;
                            case 1:
                                BasicThreading.RunDemo();
                                break;
                            case 2:
                                TaskBasics.RunDemo();
                                break;
                            case 3:
                                AsyncAwaitPatterns.RunDemo();
                                break;
                            case 4:
                                SynchronizationDemo.RunDemo();
                                break;
                            case 5:
                                ThreadPooling.RunDemo();
                                break;
                            case 6:
                                ConcurrentCollections.RunDemo();
                                break;
                            case 7:
                                ParallelLinq.RunDemo();
                                break;
                            case 8:
                                CancellationDemo.RunDemo();
                                break;
                            case 9:
                                ExceptionDemos.RunDemo();
                                break;
                            case 10:
                                BasicThreading.RunDemo();
                                TaskBasics.RunDemo();
                                AsyncAwaitPatterns.RunDemo();
                                SynchronizationDemo.RunDemo();
                                ThreadPooling.RunDemo();
                                ConcurrentCollections.RunDemo();
                                ParallelLinq.RunDemo();
                                CancellationDemo.RunDemo();
                                break;
                            default:
                                Console.WriteLine("Invalid choice. Please try again.");
                                break;
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Error in demo: {ex.Message}");
                        Console.WriteLine(ex.StackTrace);
                    }
                    
                    if (choice != 0)
                    {
                        Console.WriteLine("\nPress Enter to continue...");
                        Console.ReadLine();
                    }
                } while (choice != 0);
            }
        }
    }
} 