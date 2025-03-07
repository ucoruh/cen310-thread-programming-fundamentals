Create a comprehensive C programming project demonstrating POSIX thread fundamentals for GCC and Visual Studio. The project should:

1. EDUCATIONAL CONTENT:
   
   - Create complete tutorial documentation on basic POSIX thread operations:
     * Thread creation and joining
     * Thread detachment
     * Basic synchronization with mutexes
     * Condition variables for signaling
     * Thread-local storage
     * Thread cancellation basics
     * Thread attributes and configuration

2. IMPLEMENTATION EXAMPLES:
   
   - Create separate implementation files for each concept:
     * thread_basics.c: Thread creation, joining, and basic operations
     * mutex_demo.c: Mutex usage patterns and deadlock avoidance
     * condition_variables.c: Thread signaling and waiting mechanisms
     * producer_consumer.c: Complete producer-consumer pattern implementation
     * thread_specific_data.c: Thread-local storage demonstration
     * thread_cancellation.c: Safe thread termination techniques
     * thread_pool.c: Basic thread pool implementation

3. BUILD SYSTEMS:
   
   - Create both Makefile and CMake build configurations
   - Include Windows batch files for Visual Studio compilation
   - Include shell scripts for Linux/Unix compilation

4. PLATFORM COMPATIBILITY:
   
   - Ensure code works on both Windows (with pthreads-win32) and POSIX systems
   - Add conditional compilation for platform-specific features
   - Include installation instructions for pthread libraries on Windows

5. DOCUMENTATION:
   
   - Create README.md with:
     * Thread basics concepts explanation
     * Examples of each thread operation
     * Common pitfalls and solutions
     * Performance considerations
   - Add detailed comments throughout code explaining each operation

6. EXERCISES:
   
   - Include progressively challenging exercises with solutions:
     * Basic thread creation and termination
     * Thread synchronization scenarios
     * Deadlock identification and prevention
     * Implementing parallel algorithms

Ensure all code follows best practices for thread safety, provides proper error handling, and includes comprehensive comments explaining each concept.
