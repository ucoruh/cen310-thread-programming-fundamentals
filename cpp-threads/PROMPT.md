Create a comprehensive C++ project demonstrating modern C++ threading fundamentals that works in Visual Studio and g++. The project should:

1. EDUCATIONAL CONTENT:
   
   - Create complete tutorial documentation on C++ thread operations:
     * std::thread basics (creation, joining, detaching)
     * Thread function arguments and lambdas
     * Thread management and lifecycle
     * Synchronization mechanisms (mutex, lock_guard, unique_lock)
     * Atomic operations and memory ordering
     * Condition variables for signaling
     * Future/Promise for asynchronous results
     * Thread pools and work queues

2. IMPLEMENTATION EXAMPLES:
   
   - Create separate implementation files using modern C++ (C++17 or newer):
     * thread_basics.cpp: Thread creation with various callable types
     * synchronization.cpp: Mutex and lock demonstrations
     * atomic_operations.cpp: Lock-free programming techniques
     * async_patterns.cpp: async, future, and promise patterns
     * parallel_algorithms.cpp: C++17 parallel algorithms
     * thread_pool.cpp: Thread pool implementation using modern C++
     * data_races.cpp: Identifying and preventing data races

3. BUILD SYSTEMS:
   
   - Create both Makefile and CMake build configurations
   - Include Windows batch files for Visual Studio compilation
   - Include shell scripts for Linux/Unix compilation

4. MODERN C++ FEATURES:
   
   - Demonstrate using structured binding with thread results
   - Show C++17 parallel algorithms usage
   - Utilize std::optional and std::variant where appropriate
   - Implement RAII patterns for thread resources

5. DOCUMENTATION:
   
   - Create README.md with:
     * C++ threading model explanation
     * Memory model and thread safety concepts
     * Performance considerations and best practices
     * Common pitfalls and solutions
   - Add detailed comments aligned with modern C++ practices

6. EXERCISES:
   
   - Include progressively challenging exercises with solutions:
     * Convert callback-based code to futures
     * Implement parallel algorithms manually
     * Build thread-safe data structures
     * Optimize for thread contention

Ensure all code follows modern C++ best practices, with proper exception safety, RAII principles, and comprehensive comments explaining each concept.
