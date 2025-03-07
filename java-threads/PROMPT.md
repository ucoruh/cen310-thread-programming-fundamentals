Create a comprehensive Java threading tutorial project demonstrating fundamental to advanced concepts compatible with Java 11+. The project should:

1. EDUCATIONAL CONTENT:
   
   - Create complete tutorial documentation on Java threading approaches:
     * Classical Thread class usage
     * Runnable interface implementation
     * Synchronization with synchronized keyword
     * java.util.concurrent framework
     * Executor Service and thread pools
     * Future and CompletableFuture for async operations
     * Locks, Semaphores, and CountDownLatch
     * Atomic variables and concurrent collections
     * ThreadLocal implementation
     * Parallel Streams with fork/join framework

2. IMPLEMENTATION EXAMPLES:
   
   - Create separate classes for each concept:
     * BasicThreads.java: Thread creation and basic operations
     * SynchronizationDemo.java: Synchronized methods and blocks
     * ExecutorDemo.java: Thread pools and executor services
     * AsyncPatterns.java: CompletableFuture examples
     * ConcurrentCollections.java: Thread-safe collections
     * ParallelStreamDemo.java: Parallel stream processing
     * ThreadSafetyPatterns.java: Common thread-safety patterns

3. BUILD SYSTEMS:
   
   - Include Maven pom.xml and Gradle build.gradle configurations
   - Create scripts for building and running examples
   - Add JUnit tests demonstrating thread behavior

4. DOCUMENTATION:
   
   - Create README.md with:
     * Java threading model explanation
     * JVM memory model overview
     * Thread lifecycle and states
     * Best practices for Java concurrency
     * Common concurrency issues and solutions
   - Add comprehensive Javadoc documentation

5. JAVA SPECIFIC FEATURES:
   
   - Demonstrate thread dump analysis
   - Show JVM thread monitoring tools
   - Include examples of Java Flight Recorder for thread analysis
   - Explain garbage collection implications

6. EXERCISES:
   
   - Include progressively challenging exercises with solutions:
     * Refactoring sequential code to parallel
     * Debugging threading issues
     * Implementing reactive patterns
     * Building custom thread pools

Ensure all code follows Java best practices, with proper exception handling, resource management, and comprehensive comments explaining each concept.
