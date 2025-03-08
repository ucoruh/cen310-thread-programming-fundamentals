/**
 * @file atomic_operations.cpp
 * @brief Demonstration of C++ atomic operations and memory ordering
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <chrono>
#include <mutex>

// Global variables
const int ATOMIC_NUM_THREADS = 4;
const int ATOMIC_NUM_INCREMENTS = 10000000;

// Standard non-atomic counter (for comparison)
int atomic_demo_counter = 0;
std::mutex atomic_demo_mutex;

// Atomic counter with default memory ordering
std::atomic<int> atomic_demo_atomic_counter(0);

// Atomic flags for synchronization
std::atomic<bool> ready(false);
std::atomic<bool> done(false);

// Atomic variables for memory order demonstrations
std::atomic<int> x(0);
std::atomic<int> y(0);
int r1, r2; // For storing results of memory order tests

// Function to increment non-atomic counter using mutex
void atomic_demo_increment_with_mutex(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        std::lock_guard<std::mutex> lock(atomic_demo_mutex);
        atomic_demo_counter++;
    }
}

// Function to increment atomic counter using default memory ordering
void increment_atomic_default(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        atomic_demo_atomic_counter++; // Uses memory_order_seq_cst by default
    }
}

// Function to increment atomic counter with relaxed memory ordering
void increment_atomic_relaxed(std::atomic<int>& counter, int iterations) {
    for (int i = 0; i < iterations; ++i) {
        counter.fetch_add(1, std::memory_order_relaxed);
    }
}

// Basic atomic operations demonstration
void basic_atomic_demo() {
    std::cout << "\n=== Basic Atomic Operations Demo ===" << std::endl;
    
    // Reset counters
    atomic_demo_counter = 0;
    atomic_demo_atomic_counter = 0;
    
    // Test mutex-based synchronization
    auto start_mutex = std::chrono::high_resolution_clock::now();
    
    std::vector<std::thread> mutex_threads;
    for (int i = 0; i < ATOMIC_NUM_THREADS; ++i) {
        mutex_threads.emplace_back(atomic_demo_increment_with_mutex, ATOMIC_NUM_INCREMENTS / ATOMIC_NUM_THREADS);
    }
    
    for (auto& t : mutex_threads) {
        t.join();
    }
    
    auto end_mutex = std::chrono::high_resolution_clock::now();
    auto mutex_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_mutex - start_mutex).count();
    
    // Test atomic operations
    auto start_atomic = std::chrono::high_resolution_clock::now();
    
    std::vector<std::thread> atomic_threads;
    for (int i = 0; i < ATOMIC_NUM_THREADS; ++i) {
        atomic_threads.emplace_back(increment_atomic_default, ATOMIC_NUM_INCREMENTS / ATOMIC_NUM_THREADS);
    }
    
    for (auto& t : atomic_threads) {
        t.join();
    }
    
    auto end_atomic = std::chrono::high_resolution_clock::now();
    auto atomic_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_atomic - start_atomic).count();
    
    // Show results
    std::cout << "Expected count: " << ATOMIC_NUM_INCREMENTS << std::endl;
    std::cout << "Mutex-based counter: " << atomic_demo_counter 
              << " (Time: " << mutex_duration << " ms)" << std::endl;
    std::cout << "Atomic counter: " << atomic_demo_atomic_counter.load() 
              << " (Time: " << atomic_duration << " ms)" << std::endl;
    
    std::cout << "Atomic operations are often faster than mutex for simple operations" << std::endl;
}

// Memory ordering demonstration
void memory_ordering_demo() {
    std::cout << "\n=== Memory Ordering Demo ===" << std::endl;
    
    // Sequential consistency (strongest, default)
    std::cout << "Sequential Consistency (memory_order_seq_cst):" << std::endl;
    std::cout << "- All operations follow a single total order" << std::endl;
    std::cout << "- Most intuitive but highest overhead" << std::endl;
    
    // Acquire-Release semantics
    std::cout << "\nAcquire-Release Semantics:" << std::endl;
    std::cout << "- memory_order_acquire: Synchronizes with release operations" << std::endl;
    std::cout << "- memory_order_release: Makes prior writes visible to threads doing acquire" << std::endl;
    
    // Demonstrate acquire-release ordering
    auto acquire_release_demo = []{
        x = 0;
        y = 0;
        r1 = r2 = 0;
        
        std::thread t1([]{
            x.store(1, std::memory_order_release);
        });
        
        std::thread t2([]{
            // This acquire operation synchronizes with the release in t1
            while (!x.load(std::memory_order_acquire));
            
            // After acquire, all writes from t1 are visible
            y.store(1, std::memory_order_release);
        });
        
        std::thread t3([]{
            // This acquire operation synchronizes with the release in t2
            while (!y.load(std::memory_order_acquire));
            
            // After acquire, all writes from t2 (and transitively t1) are visible
            r1 = x.load(std::memory_order_relaxed);
        });
        
        t1.join();
        t2.join();
        t3.join();
        
        std::cout << "Using acquire-release: r1 = " << r1 << " (expected 1)" << std::endl;
    };
    
    acquire_release_demo();
    
    // Relaxed ordering
    std::cout << "\nRelaxed Ordering (memory_order_relaxed):" << std::endl;
    std::cout << "- No synchronization between threads" << std::endl;
    std::cout << "- Only guarantees atomicity, not ordering between threads" << std::endl;
    std::cout << "- Lowest overhead, but hardest to reason about" << std::endl;
    
    // Demonstrate relaxed ordering
    auto relaxed_demo = []{
        std::atomic<int> relaxed_counter(0);
        
        auto start_relaxed = std::chrono::high_resolution_clock::now();
        
        std::vector<std::thread> relaxed_threads;
        for (int i = 0; i < ATOMIC_NUM_THREADS; ++i) {
            relaxed_threads.emplace_back(increment_atomic_relaxed, 
                                         std::ref(relaxed_counter), 
                                         ATOMIC_NUM_INCREMENTS / ATOMIC_NUM_THREADS);
        }
        
        for (auto& t : relaxed_threads) {
            t.join();
        }
        
        auto end_relaxed = std::chrono::high_resolution_clock::now();
        auto relaxed_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_relaxed - start_relaxed).count();
        
        std::cout << "Relaxed counter: " << relaxed_counter.load() 
                  << " (Time: " << relaxed_duration << " ms)" << std::endl;
    };
    
    relaxed_demo();
}

// Atomic flag for signaling between threads
void atomic_flag_demo() {
    std::cout << "\n=== Atomic Flag Demo ===" << std::endl;
    
    std::atomic_flag flag = ATOMIC_FLAG_INIT; // The only lock-free atomic type guaranteed across all platforms
    
    auto wait_for_flag = [&flag](int thread_id) {
        // Spin until flag is cleared
        while (flag.test_and_set(std::memory_order_acquire)) {
            // Spin - could use std::this_thread::yield() in real code
        }
        
        std::cout << "Thread " << thread_id << " acquired the flag" << std::endl;
        
        // Simulate some work
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        
        // Release the flag
        flag.clear(std::memory_order_release);
        std::cout << "Thread " << thread_id << " released the flag" << std::endl;
    };
    
    // Create multiple threads that will compete for the flag
    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back(wait_for_flag, i + 1);
    }
    
    // Join all threads
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "std::atomic_flag provides a simple spinlock mechanism" << std::endl;
}

// Compare-and-exchange operation demonstration
void compare_exchange_demo() {
    std::cout << "\n=== Compare-and-Exchange Demo ===" << std::endl;
    
    std::atomic<int> value(0);
    
    auto attempt_update = [&value](int thread_id, int new_value) {
        int expected = 0;
        
        // Try to atomically update the value if it equals expected
        bool success = value.compare_exchange_strong(expected, new_value);
        
        if (success) {
            std::cout << "Thread " << thread_id << ": Successfully updated value to " 
                      << new_value << std::endl;
        } else {
            std::cout << "Thread " << thread_id << ": Update failed, value was " 
                      << expected << ", not 0" << std::endl;
        }
    };
    
    // Create threads to compete in updating the value
    std::thread t1(attempt_update, 1, 100);
    std::thread t2(attempt_update, 2, 200);
    std::thread t3(attempt_update, 3, 300);
    
    // Join threads
    t1.join();
    t2.join();
    t3.join();
    
    std::cout << "Final value: " << value.load() << std::endl;
    std::cout << "compare_exchange operations are fundamental building blocks for lock-free algorithms" << std::endl;
}

// Atomic pointer operations
void atomic_pointer_demo() {
    std::cout << "\n=== Atomic Pointer Demo ===" << std::endl;
    
    // Create a structure to represent some shared data
    struct SharedData {
        int value;
        
        SharedData(int v) : value(v) {}
        ~SharedData() {
            std::cout << "SharedData with value " << value << " destroyed" << std::endl;
        }
    };
    
    // Create an atomic pointer
    std::atomic<SharedData*> atomic_ptr(nullptr);
    
    // Thread function to update the pointer
    auto update_pointer = [&atomic_ptr](int id) {
        // Create a new SharedData object
        SharedData* new_data = new SharedData(id * 100);
        
        // Replace the old pointer with the new one
        SharedData* old_data = atomic_ptr.exchange(new_data);
        
        // If there was a previous object, delete it
        if (old_data) {
            std::cout << "Thread " << id << " replaced SharedData with value " 
                      << old_data->value << std::endl;
            delete old_data;
        } else {
            std::cout << "Thread " << id << " set the first SharedData instance" << std::endl;
        }
    };
    
    // Run multiple threads that update the pointer
    std::vector<std::thread> threads;
    for (int i = 1; i <= 3; ++i) {
        threads.emplace_back(update_pointer, i);
    }
    
    // Join all threads
    for (auto& t : threads) {
        t.join();
    }
    
    // Clean up the final pointer
    SharedData* final_data = atomic_ptr.load();
    if (final_data) {
        std::cout << "Final SharedData value: " << final_data->value << std::endl;
        delete final_data;
    }
    
    std::cout << "Atomic pointers allow thread-safe pointer updates without locks" << std::endl;
}

// Main function to run all atomic operations demos
int atomic_operations_main() {
    std::cout << "=== Atomic Operations Demo ===" << std::endl;
    
    // Run the basic atomic operations demo
    basic_atomic_demo();
    
    // Run the memory ordering demo
    memory_ordering_demo();
    
    // Run the atomic flag demo
    atomic_flag_demo();
    
    // Run the compare-and-exchange demo
    compare_exchange_demo();
    
    // Run the atomic pointer demo
    atomic_pointer_demo();
    
    std::cout << "\nAtomic operations demonstration completed" << std::endl;
    return 0;
} 