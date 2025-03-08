using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpThreads
{
    /// <summary>
    /// Demonstrates various types of exceptions and error handling in C#
    /// </summary>
    public static class ExceptionDemos
    {
        /// <summary>
        /// Demonstrates basic exceptions and how to throw them
        /// </summary>
        private static void BasicExceptionDemo()
        {
            Console.WriteLine("\n=== Basic Exceptions Demo ===");
            
            try
            {
                Console.WriteLine("1. Throwing a simple exception with a message");
                throw new Exception("This is a test exception!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Caught: {ex.GetType().Name} - {ex.Message}");
            }
            
            try
            {
                Console.WriteLine("\n2. Division by zero (ArithmeticException)");
                int zero = 0;
                int result = 10 / zero; // This line will throw DivideByZeroException
                Console.WriteLine($"Result: {result}"); // This line won't execute
            }
            catch (DivideByZeroException ex)
            {
                Console.WriteLine($"Caught: {ex.GetType().Name} - {ex.Message}");
            }
            
            try
            {
                Console.WriteLine("\n3. Null reference exception");
                string? nullString = null;
                int length = nullString!.Length; // This line will throw NullReferenceException
                Console.WriteLine($"Length: {length}"); // This line won't execute
            }
            catch (NullReferenceException ex)
            {
                Console.WriteLine($"Caught: {ex.GetType().Name} - {ex.Message}");
            }
            
            try
            {
                Console.WriteLine("\n4. Index out of range exception");
                int[] array = new int[3];
                int value = array[10]; // This line will throw IndexOutOfRangeException
                Console.WriteLine($"Value: {value}"); // This line won't execute
            }
            catch (IndexOutOfRangeException ex)
            {
                Console.WriteLine($"Caught: {ex.GetType().Name} - {ex.Message}");
            }
            
            try
            {
                Console.WriteLine("\n5. Format exception");
                string notANumber = "this is not a number";
                int number = int.Parse(notANumber); // This line will throw FormatException
                Console.WriteLine($"Number: {number}"); // This line won't execute
            }
            catch (FormatException ex)
            {
                Console.WriteLine($"Caught: {ex.GetType().Name} - {ex.Message}");
            }
        }
        
        /// <summary>
        /// Demonstrates nested exception handling and re-throwing
        /// </summary>
        private static void NestedExceptionDemo()
        {
            Console.WriteLine("\n=== Nested Exception Demo ===");
            
            try
            {
                Console.WriteLine("Outer try block");
                try
                {
                    Console.WriteLine("Inner try block - about to throw");
                    throw new InvalidOperationException("Exception thrown from inner block");
                }
                catch (InvalidOperationException ex)
                {
                    Console.WriteLine($"Inner catch: {ex.Message}");
                    
                    // Re-throw the exception with additional information
                    throw new ApplicationException("Exception caught in outer block and rethrown", ex);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Outer catch: {ex.GetType().Name} - {ex.Message}");
                
                if (ex.InnerException != null)
                {
                    Console.WriteLine($"Inner exception: {ex.InnerException.GetType().Name} - {ex.InnerException.Message}");
                }
            }
        }
        
        /// <summary>
        /// Demonstrates the finally block which always executes
        /// </summary>
        private static void FinallyBlockDemo()
        {
            Console.WriteLine("\n=== Finally Block Demo ===");
            
            try
            {
                Console.WriteLine("1. Try block with exception");
                throw new Exception("Test exception");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Catch block: {ex.Message}");
            }
            finally
            {
                Console.WriteLine("Finally block: This always executes (after exception)");
            }
            
            try
            {
                Console.WriteLine("\n2. Try block without exception");
                Console.WriteLine("Completing without exception");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Catch block: {ex.Message}");
            }
            finally
            {
                Console.WriteLine("Finally block: This always executes (no exception)");
            }
            
            // Demonstrating resource cleanup in finally
            FileStream? file = null;
            try
            {
                Console.WriteLine("\n3. Resource cleanup with finally");
                // Attempt to open a file that doesn't exist
                file = File.OpenRead("non-existent-file.txt");
                Console.WriteLine("File opened successfully (this won't execute)");
            }
            catch (FileNotFoundException ex)
            {
                Console.WriteLine($"File not found: {ex.Message}");
            }
            finally
            {
                if (file != null)
                {
                    file.Dispose();
                    Console.WriteLine("File closed in finally block");
                }
                else
                {
                    Console.WriteLine("No file to close in finally block");
                }
            }
        }
        
        /// <summary>
        /// Demonstrates exception filters (when clause) introduced in C# 6
        /// </summary>
        private static void ExceptionFiltersDemo()
        {
            Console.WriteLine("\n=== Exception Filters Demo ===");
            
            for (int i = -1; i <= 1; i++)
            {
                try
                {
                    Console.WriteLine($"\nTesting with value: {i}");
                    if (i < 0)
                        throw new ArgumentOutOfRangeException("i", "Value cannot be negative");
                    if (i == 0)
                        throw new DivideByZeroException("Division by zero error");
                    if (i > 0)
                        throw new ArgumentException("A positive value");
                }
                catch (ArgumentOutOfRangeException ex) when (ex.ParamName == "i")
                {
                    Console.WriteLine($"Caught ArgumentOutOfRangeException for parameter 'i': {ex.Message}");
                }
                catch (ArgumentException ex) when (ex.Message.Contains("pozitif"))
                {
                    Console.WriteLine($"Caught ArgumentException with 'pozitif' in message: {ex.Message}");
                }
                catch (Exception ex) when (LogException(ex))
                {
                    // This block never executes because LogException returns false
                    // But the exception will be logged
                    Console.WriteLine("This won't execute");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Caught general exception: {ex.GetType().Name} - {ex.Message}");
                }
            }
        }
        
        /// <summary>
        /// Helper method for exception filter that logs and returns false
        /// </summary>
        private static bool LogException(Exception ex)
        {
            Console.WriteLine($"Logging exception: {ex.GetType().Name} - {ex.Message}");
            return false; // Always returns false so the catch block won't execute
        }
        
        /// <summary>
        /// Demonstrates unhandled exceptions in different contexts
        /// </summary>
        private static void UnhandledExceptionDemo()
        {
            Console.WriteLine("\n=== Unhandled Exception Demo ===");
            
            Console.WriteLine("1. Unhandled exception in a Task");
            
            Task task = Task.Run(() =>
            {
                throw new InvalidOperationException("Unhandled exception in Task");
            });
            
            try
            {
                task.Wait(); // This will rethrow the exception
            }
            catch (AggregateException ae)
            {
                Console.WriteLine($"Caught AggregateException from Task: {ae.InnerExceptions.Count} inner exception(s)");
                foreach (var ex in ae.InnerExceptions)
                {
                    Console.WriteLine($"  - {ex.GetType().Name}: {ex.Message}");
                }
            }
            
            Console.WriteLine("\n2. Async void method with unhandled exception (this can crash the app)");
            
            // Warn that this might crash
            Console.WriteLine("Warning: This is a demonstration of how async void methods can be dangerous");
            Console.WriteLine("The example below has been modified to prevent crashing the application while still showing the concept");
            Console.WriteLine("Press Enter to continue...");
            Console.ReadLine();
            
            // UNSAFE METHOD - commented out for safety, but described for educational purposes
            /*
            // This method would normally crash the application when called
            AsyncVoidExceptionMethod();
            */
            
            Console.WriteLine("\nDEMONSTRATION ONLY - NOT ACTUALLY CALLING THE UNSAFE METHOD");
            Console.WriteLine("If we had called the async void method:");
            Console.WriteLine("1. It would execute asynchronously");
            Console.WriteLine("2. When it throws an exception, it would propagate to the thread pool");
            Console.WriteLine("3. Since the exception is not caught, it would crash the application");
            Console.WriteLine("4. Try/catch blocks at the caller level cannot catch these exceptions");
            
            Console.WriteLine("\nSafe alternative: Use async Task instead of async void:");
            try
            {
                // Use Task.Run to execute and wait for a safer Task-based alternative
                Task.Run(async () => 
                {
                    await Task.Delay(100);
                    throw new InvalidOperationException("Exception from async Task method (safely caught)");
                }).Wait();
            }
            catch (AggregateException ae)
            {
                Console.WriteLine($"Safely caught exception: {ae.InnerException?.Message ?? "No inner exception details available"}");
                Console.WriteLine("The application continues running normally");
            }
        }
        
        /// <summary>
        /// Async void method that throws an unhandled exception
        /// This method is not being called directly to prevent application crashes
        /// Included for educational purposes only
        /// </summary>
        private static async void AsyncVoidExceptionMethod()
        {
            await Task.Delay(100); // Short delay
            throw new InvalidOperationException("Unhandled exception in async void method!");
        }
        
        /// <summary>
        /// Demonstrates handling user input errors
        /// </summary>
        private static void UserInputErrorDemo()
        {
            Console.WriteLine("\n=== User Input Error Demo ===");
            
            while (true)
            {
                Console.WriteLine("\nPlease enter a number (enter 'q' to quit):");
                string? input = Console.ReadLine();
                
                if (input?.ToLower() == "q")
                    break;
                
                try
                {
                    int number = int.Parse(input ?? string.Empty);
                    Console.WriteLine($"Square of the entered number: {number * number}");
                }
                catch (FormatException)
                {
                    Console.WriteLine("Error: You must enter a valid number!");
                }
                catch (OverflowException)
                {
                    Console.WriteLine("Error: Number is too large or too small!");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Unexpected error: {ex.Message}");
                }
            }
        }
        
        /// <summary>
        /// Creates a method that always throws a specific exception
        /// </summary>
        public static void ThrowSpecificException(string exceptionType)
        {
            Console.WriteLine($"\n=== Throwing {exceptionType} Exception ===");
            
            switch (exceptionType.ToLower())
            {
                case "argument":
                    throw new ArgumentException("Invalid argument error!");
                case "null":
                    throw new NullReferenceException("Null reference error!");
                case "outofrange":
                    throw new IndexOutOfRangeException("Index out of range error!");
                case "divide":
                    int zero = 0;
                    int result = 10 / zero; // DivideByZeroException
                    break;
                case "overflow":
                    int maxValue = int.MaxValue;
                    int overflow = checked(maxValue + 1); // OverflowException
                    break;
                case "io":
                    throw new IOException("Input/output error!");
                case "format":
                    int.Parse("this is not a number"); // FormatException
                    break;
                case "custom":
                    throw new CustomException("A custom exception type!");
                default:
                    throw new Exception($"Unknown exception type: {exceptionType}");
            }
        }
        
        /// <summary>
        /// Custom exception class demo
        /// </summary>
        public class CustomException : Exception
        {
            public CustomException(string message) : base(message)
            {
            }
            
            public CustomException(string message, Exception innerException) : base(message, innerException)
            {
            }
        }
        
        /// <summary>
        /// Run the exception demos
        /// </summary>
        public static void RunDemo()
        {
            Console.WriteLine("=== Exception Handling Demo ===");
            
            // Run the demos
            BasicExceptionDemo();
            NestedExceptionDemo();
            FinallyBlockDemo();
            ExceptionFiltersDemo();
            UnhandledExceptionDemo(); // This one can potentially crash the app!
            
            // Skip the user input demo unless specifically requested
            // UserInputErrorDemo();
            
            Console.WriteLine("\nException handling demo completed");
        }
    }
} 