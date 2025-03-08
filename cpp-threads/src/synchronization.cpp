/**
 * @file synchronization.cpp
 * @brief Demonstration of C++ thread synchronization mechanisms
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <chrono>
#include <atomic>
#include <shared_mutex> // For std::shared_mutex (C++17)

// Global variables
const int NUM_THREADS = 4;
const int NUM_INCREMENTS = 1000000;

// Shared counter (no protection)
int unsafe_counter = 0;

// Shared counter with mutex protection
int safe_counter = 0;
std::mutex counter_mutex;

// Shared counter with atomic protection
std::atomic<int> atomic_counter(0);

// Recursive mutex for nested locking demo
std::recursive_mutex recursive_mutex;

// Shared mutex for reader-writer pattern
std::shared_mutex shared_data_mutex;
int shared_data = 0;

// Function that increments a counter without protection (race condition)
void increment_unsafe(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        // This is unsafe - multiple threads may execute this simultaneously
        unsafe_counter++; // Race condition
    }
}

// Function that increments a counter with basic mutex protection
void increment_with_mutex(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        // Acquire the mutex before modifying the shared counter
        counter_mutex.lock();
        
        // Critical section - only one thread can execute this at a time
        safe_counter++;
        
        // Release the mutex after modifying the shared counter
        counter_mutex.unlock();
    }
}

// Function that increments a counter with RAII lock_guard
void increment_with_lock_guard(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        // RAII approach - lock_guard automatically releases mutex when it goes out of scope
        std::lock_guard<std::mutex> lock(counter_mutex);
        
        // Critical section
        safe_counter++;
        
        // The lock_guard automatically releases the mutex when it goes out of scope
    }
}

// Function that increments a counter with unique_lock
void increment_with_unique_lock(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        // Create a unique_lock without locking the mutex immediately (defer_lock)
        std::unique_lock<std::mutex> lock(counter_mutex, std::defer_lock);
        
        // Do some work before acquiring the mutex
        // ...
        
        // Now lock the mutex
        lock.lock();
        
        // Critical section
        safe_counter++;
        
        // We can explicitly unlock before the end of the scope if needed
        lock.unlock();
        
        // Do more work after releasing the mutex
        // ...
    }
}

// Function that increments an atomic counter
void increment_atomic(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        // Atomic operations don't need explicit mutex protection
        atomic_counter++; // This is thread-safe
    }
}

// Basic atomic operations demonstration
void basic_mutex_demo() {
    std::cout << "\n=== Basic Mutex Demo ===" << std::endl;
    
    // Reset counters
    unsafe_counter = 0;
    safe_counter = 0;
    atomic_counter = 0;
    
    // Start time measurement
    auto start_unsafe = std::chrono::high_resolution_clock::now();
    
    // Create threads for unsafe increment (race condition)
    std::vector<std::thread> unsafe_threads;
    for (int i = 0; i < NUM_THREADS; ++i) {
        unsafe_threads.emplace_back(increment_unsafe, NUM_INCREMENTS / NUM_THREADS);
    }
    
    // Join the unsafe threads
    for (auto& t : unsafe_threads) {
        t.join();
    }
    
    // End time measurement for unsafe
    auto end_unsafe = std::chrono::high_resolution_clock::now();
    auto unsafe_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_unsafe - start_unsafe).count();
    
    // Start time measurement for safe increment
    auto start_safe = std::chrono::high_resolution_clock::now();
    
    // Create threads for safe increment (with mutex)
    std::vector<std::thread> safe_threads;
    for (int i = 0; i < NUM_THREADS; ++i) {
        safe_threads.emplace_back(increment_with_mutex, NUM_INCREMENTS / NUM_THREADS);
    }
    
    // Join the safe threads
    for (auto& t : safe_threads) {
        t.join();
    }
    
    // End time measurement for safe
    auto end_safe = std::chrono::high_resolution_clock::now();
    auto safe_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_safe - start_safe).count();
    
    // Print results
    std::cout << "Expected final count: " << NUM_INCREMENTS << std::endl;
    std::cout << "Unsafe counter (with race condition): " << unsafe_counter 
              << " (Time: " << unsafe_duration << " ms)" << std::endl;
    std::cout << "Safe counter (with mutex): " << safe_counter 
              << " (Time: " << safe_duration << " ms)" << std::endl;
}

// Lock guard demonstration
void lock_guard_demo() {
    std::cout << "\n=== Lock Guard Demo ===" << std::endl;
    
    // Reset counter
    safe_counter = 0;
    
    // Create threads using lock_guard
    std::vector<std::thread> threads;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < NUM_THREADS; ++i) {
        threads.emplace_back(increment_with_lock_guard, NUM_INCREMENTS / NUM_THREADS);
    }
    
    // Join all threads
    for (auto& t : threads) {
        t.join();
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_time - start_time).count();
    
    // Print result
    std::cout << "Expected final count: " << NUM_INCREMENTS << std::endl;
    std::cout << "Final count with lock_guard: " << safe_counter 
              << " (Time: " << duration << " ms)" << std::endl;
    
    std::cout << "Lock guard is an RAII wrapper for mutex that automatically releases the lock when out of scope" << std::endl;
}

// Unique lock demonstration
void unique_lock_demo() {
    std::cout << "\n=== Unique Lock Demo ===" << std::endl;
    
    // Reset counter
    safe_counter = 0;
    
    // Create threads using unique_lock
    std::vector<std::thread> threads;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < NUM_THREADS; ++i) {
        threads.emplace_back(increment_with_unique_lock, NUM_INCREMENTS / NUM_THREADS);
    }
    
    // Join all threads
    for (auto& t : threads) {
        t.join();
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_time - start_time).count();
    
    // Print result
    std::cout << "Expected final count: " << NUM_INCREMENTS << std::endl;
    std::cout << "Final count with unique_lock: " << safe_counter 
              << " (Time: " << duration << " ms)" << std::endl;
    
    std::cout << "unique_lock offers more flexibility than lock_guard with defer_lock, try_lock, etc." << std::endl;
}

// Forward declare the recursive function so it can be used in lambda
void recursive_function(int depth);

// Recursive mutex demonstration
void recursive_mutex_demo() {
    std::cout << "\n=== Recursive Mutex Demo ===" << std::endl;
    
    // Call the recursive function to start
    recursive_function(3);
    
    std::cout << "Recursive mutex allows a thread to acquire the same mutex multiple times" << std::endl;
}

// Implementation of the recursive function
void recursive_function(int depth) {
    std::cout << "Recursive function at depth " << depth << std::endl;
    
    // Acquire the recursive mutex (can be locked multiple times by same thread)
    std::lock_guard<std::recursive_mutex> lock(recursive_mutex);
    
    std::cout << "Acquired recursive mutex at depth " << depth << std::endl;
    
    // Recursively call the function and acquire the lock again
    if (depth > 0) {
        recursive_function(depth - 1);
    }
    
    std::cout << "Releasing recursive mutex at depth " << depth << std::endl;
    
    // The lock is automatically released when it goes out of scope
}

// Reader-writer lock demonstration - renamed to avoid conflict with data_races.cpp
void sync_reader_writer_lock_demo() {
    std::cout << "\n=== Reader-Writer Lock Demo ===" << std::endl;
    
    // Shared data protected by a shared_mutex
    int shared_value = 0;
    std::shared_mutex rw_mutex;
    
    // Function that writes to the shared data
    auto writer_fn = [&shared_value, &rw_mutex](int iterations) {
        for (int i = 0; i < iterations; ++i) {
            // Exclusive lock for writing
            std::unique_lock<std::shared_mutex> write_lock(rw_mutex);
            shared_value = i;
            
            // Simulate some work
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
        }
    };
    
    // Function that reads from the shared data
    auto reader_fn = [&shared_value, &rw_mutex](int reader_id, int iterations) {
        int sum = 0;
        for (int i = 0; i < iterations; ++i) {
            // Shared lock for reading (multiple readers allowed)
            std::shared_lock<std::shared_mutex> read_lock(rw_mutex);
            sum += shared_value;
            
            // Simulate some work
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        }
        std::cout << "Reader " << reader_id << " sum: " << sum << std::endl;
    };
    
    // Launch one writer and multiple readers
    std::cout << "Launching writer and reader threads..." << std::endl;
    
    const int write_iterations = 100;
    const int read_iterations = 200;
    
    std::thread writer(writer_fn, write_iterations);
    
    std::vector<std::thread> readers;
    for (int i = 0; i < 3; ++i) {
        readers.emplace_back(reader_fn, i + 1, read_iterations);
    }
    
    // Wait for all threads
    writer.join();
    for (auto& reader : readers) {
        reader.join();
    }
    
    std::cout << "Reader-writer lock demo completed. Multiple readers could read simultaneously." << std::endl;
}

// Atomic operations demonstration
void atomic_demo() {
    std::cout << "\n=== Atomic Operations Demo ===" << std::endl;
    
    // Reset atomic counter
    atomic_counter = 0;
    
    // Create threads using atomic operations
    std::vector<std::thread> threads;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < NUM_THREADS; ++i) {
        threads.emplace_back(increment_atomic, NUM_INCREMENTS / NUM_THREADS);
    }
    
    // Join all threads
    for (auto& t : threads) {
        t.join();
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_time - start_time).count();
    
    // Print result
    std::cout << "Expected final count: " << NUM_INCREMENTS << std::endl;
    std::cout << "Final atomic counter: " << atomic_counter.load() 
              << " (Time: " << duration << " ms)" << std::endl;
    
    std::cout << "Atomic operations provide thread safety without explicit locks" << std::endl;
}

// Main function to run the synchronization demos
int synchronization_main() {
    std::cout << "=== Synchronization Demo ===" << std::endl;
    
    // Run the basic mutex demo
    basic_mutex_demo();
    
    // Run the lock guard demo
    lock_guard_demo();
    
    // Run the unique lock demo
    unique_lock_demo();
    
    // Run the recursive mutex demo
    recursive_mutex_demo();
    
    // Run the reader-writer lock demo
    sync_reader_writer_lock_demo();
    
    // Run the atomic operations demo
    atomic_demo();
    
    std::cout << "\nSynchronization demonstration completed" << std::endl;
    return 0;
} 