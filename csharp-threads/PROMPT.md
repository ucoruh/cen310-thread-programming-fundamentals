Create a comprehensive C# threading tutorial project demonstrating the Task Parallel Library and other threading concepts in .NET 6 or later. The project should:

1. EDUCATIONAL CONTENT:
   
   - Create complete tutorial documentation on C# threading approaches:
     * System.Threading.Thread basics
     * Task Parallel Library (TPL) fundamentals
     * async/await patterns
     * Synchronization with lock, Monitor, and Interlocked
     * Thread pooling in .NET
     * Concurrent collections
     * Parallel LINQ (PLINQ)
     * Coordination primitives (ManualResetEvent, AutoResetEvent)
     * Thread safety in C#
     * Cancellation tokens and cooperative cancellation

2. IMPLEMENTATION EXAMPLES:
   
   - Create separate implementation files for each concept:
     * BasicThreading.cs: Thread class usage and fundamentals
     * TaskBasics.cs: TPL and task creation patterns
     * AsyncAwaitPatterns.cs: Asynchronous programming patterns
     * SynchronizationDemo.cs: Various synchronization mechanisms
     * ParallelOperations.cs: Parallel.For, Parallel.ForEach
     * ThreadPooling.cs: Working with the .NET thread pool
     * ConcurrentCollections.cs: Thread-safe collection usage
     * CoordinationPrimitives.cs: Signaling between threads
     * CancellationDemo.cs: Implementing cancellation

3. PROJECT STRUCTURE:
   
   - Create a Visual Studio solution with multiple projects:
     * Core threading examples (class library)
     * Console application for demonstrations
     * WPF application showing UI responsiveness with background threads
     * Unit tests for threading concepts

4. BUILD CONFIGURATION:
   
   - Include .NET SDK project files
   - Add GitHub Actions workflow for CI/CD
   - Include PowerShell scripts for building and running examples

5. DOCUMENTATION:
   
   - Create README.md with:
     * .NET threading model explanation
     * Task vs Thread comparison
     * Best practices for C# concurrency
     * Common pitfalls and solutions
     * Performance considerations
   - Add XML documentation for all classes and methods

6. EXERCISES:
   
   - Include progressively challenging exercises with solutions:
     * Updating UI from background threads
     * Implementing producer-consumer patterns
     * Building responsive applications with background processing
     * Parallel data processing scenarios

Ensure all code follows modern C# best practices, with proper exception handling, resource management using using statements, and comprehensive comments explaining each concept.
