/**
 * @file data_races.cpp
 * @brief Demonstration of data races and thread safety issues in C++
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>
#include <string>
#include <chrono>
#include <memory>
#include <sstream>
#include <iomanip>
#include <shared_mutex>

// Declare global variables with unique names to avoid conflicts
std::mutex data_race_mutex;
std::atomic<int> data_race_atomic_counter(0);

// Thread-safe counter class
class ThreadSafeCounter {
private:
    int value = 0;
    mutable std::mutex mutex;

public:
    // Increment the counter safely
    void increment() {
        std::lock_guard<std::mutex> lock(mutex);
        ++value;
    }
    
    // Get the current value safely
    int get() const {
        std::lock_guard<std::mutex> lock(mutex);
        return value;
    }
};

// =================== DATA RACE EXAMPLES ===================

// Example 1: Basic data race
void basic_data_race_demo() {
    std::cout << "\n=== Basic Data Race Demo ===" << std::endl;
    
    int shared_counter = 0;
    const int iterations = 1000000;
    
    // Thread function that increments the counter
    auto increment_thread = [&shared_counter, iterations]() {
        for (int i = 0; i < iterations; ++i) {
            // This is a data race - multiple threads might access this simultaneously
            shared_counter++;
        }
    };
    
    // Launch multiple threads
    std::cout << "Launching threads with data race..." << std::endl;
    std::thread t1(increment_thread);
    std::thread t2(increment_thread);
    
    // Wait for threads to complete
    t1.join();
    t2.join();
    
    // Check the result - it will be less than expected due to data races
    std::cout << "Expected counter value: " << (iterations * 2) << std::endl;
    std::cout << "Actual counter value: " << shared_counter << std::endl;
    std::cout << "Lost updates due to data race: " << (iterations * 2 - shared_counter) << std::endl;
}

// Example 2: Read-write data race
void read_write_race_demo() {
    std::cout << "\n=== Read-Write Data Race Demo ===" << std::endl;
    
    // Shared data structure with potential read-write race
    struct SharedData {
        int value = 0;
        bool is_ready = false;
    } shared_data;
    
    // Writer thread
    std::thread writer([&shared_data]() {
        std::cout << "Writer thread: preparing data..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        
        // Update the value
        shared_data.value = 42;
        
        // There's a gap between setting value and is_ready flag
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        
        // Set the ready flag
        shared_data.is_ready = true;
        std::cout << "Writer thread: data is now ready" << std::endl;
    });
    
    // Reader thread - has a race condition with the writer
    std::thread reader([&shared_data]() {
        std::cout << "Reader thread: waiting for data..." << std::endl;
        
        // Busy wait for the ready flag - this has a race condition
        // We might see is_ready=true but get an old value for value
        while (!shared_data.is_ready) {
            std::this_thread::yield();
        }
        
        // Read the value - there's a race here!
        std::cout << "Reader thread: got value = " << shared_data.value << std::endl;
    });
    
    writer.join();
    reader.join();
    
    std::cout << "This demo might work correctly by chance, but there's a potential race condition." << std::endl;
    std::cout << "The reader might see is_ready=true before value=42 is visible to it." << std::endl;
}

// =================== THREAD SAFETY SOLUTIONS ===================

// Example 3: Mutex solution
void mutex_solution_demo() {
    std::cout << "\n=== Mutex Solution Demo ===" << std::endl;
    
    int shared_counter = 0;
    std::mutex demo_mutex; // Renamed to avoid conflict with global
    const int iterations = 1000000;
    
    // Thread function that increments the counter with mutex protection
    auto safe_increment_thread = [&shared_counter, &demo_mutex, iterations]() {
        for (int i = 0; i < iterations; ++i) {
            // Lock the mutex before accessing the shared counter
            std::lock_guard<std::mutex> lock(demo_mutex);
            shared_counter++;
        }
    };
    
    // Launch multiple threads
    std::cout << "Launching threads with mutex protection..." << std::endl;
    std::thread t1(safe_increment_thread);
    std::thread t2(safe_increment_thread);
    
    // Wait for threads to complete
    t1.join();
    t2.join();
    
    // Check the result - should be exactly as expected
    std::cout << "Expected counter value: " << (iterations * 2) << std::endl;
    std::cout << "Actual counter value: " << shared_counter << std::endl;
}

// Example 4: Atomic solution
void atomic_solution_demo() {
    std::cout << "\n=== Atomic Solution Demo ===" << std::endl;
    
    std::atomic<int> demo_counter(0); // Renamed to avoid conflict with global
    const int iterations = 1000000;
    
    // Thread function that increments the atomic counter
    auto atomic_increment_thread = [&demo_counter, iterations]() {
        for (int i = 0; i < iterations; ++i) {
            // Atomic operation - no mutex needed
            demo_counter++;
        }
    };
    
    // Launch multiple threads
    std::cout << "Launching threads with atomic counter..." << std::endl;
    std::thread t1(atomic_increment_thread);
    std::thread t2(atomic_increment_thread);
    
    // Wait for threads to complete
    t1.join();
    t2.join();
    
    // Check the result - should be exactly as expected
    std::cout << "Expected counter value: " << (iterations * 2) << std::endl;
    std::cout << "Actual counter value: " << demo_counter.load() << std::endl;
}

// Example 5: Thread-local storage solution
void thread_local_solution_demo() {
    std::cout << "\n=== Thread-Local Storage Demo ===" << std::endl;
    
    // Thread-local counter
    thread_local int local_counter = 0;
    
    // Shared counter for combined result
    std::atomic<int> shared_counter(0);
    const int iterations = 1000000;
    
    // Thread function that uses thread-local storage
    auto thread_local_fn = [&shared_counter, iterations](int thread_id) {
        // Each thread has its own copy of local_counter
        local_counter = 0;
        
        for (int i = 0; i < iterations; ++i) {
            // No race condition here since local_counter is thread-local
            local_counter++;
        }
        
        // Add the thread-local result to the shared counter atomically
        shared_counter += local_counter;
        
        std::cout << "Thread " << thread_id << " local counter: " << local_counter << std::endl;
    };
    
    // Launch multiple threads
    std::cout << "Launching threads with thread-local storage..." << std::endl;
    std::thread t1(thread_local_fn, 1);
    std::thread t2(thread_local_fn, 2);
    
    // Wait for threads to complete
    t1.join();
    t2.join();
    
    // Check the combined result
    std::cout << "Expected combined value: " << (iterations * 2) << std::endl;
    std::cout << "Actual combined value: " << shared_counter.load() << std::endl;
}

// =================== ADVANCED THREAD SAFETY PATTERNS ===================

// Example 6: Reader-writer lock pattern
void reader_writer_lock_demo() {
    std::cout << "\n=== Reader-Writer Lock Demo ===" << std::endl;
    
    // Shared data protected by a shared_mutex
    int shared_data = 0;
    std::shared_mutex rw_mutex;
    
    // Function that writes to the shared data
    auto writer_fn = [&shared_data, &rw_mutex](int iterations) {
        for (int i = 0; i < iterations; ++i) {
            // Exclusive lock for writing
            std::unique_lock<std::shared_mutex> write_lock(rw_mutex);
            shared_data = i;
            
            // Simulate some work
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
        }
    };
    
    // Function that reads from the shared data
    auto reader_fn = [&shared_data, &rw_mutex](int reader_id, int iterations) {
        int sum = 0;
        for (int i = 0; i < iterations; ++i) {
            // Shared lock for reading (multiple readers allowed)
            std::shared_lock<std::shared_mutex> read_lock(rw_mutex);
            sum += shared_data;
            
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

// Example 7: Double-checked locking pattern (Singleton)
// Singleton class declared outside to allow static members
class Singleton {
private:
    // Private constructor
    Singleton() {
        std::cout << "Singleton instance created" << std::endl;
        // Simulate expensive initialization
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    // Static instance pointers and mutex
    static std::mutex s_mutex;
    static std::atomic<Singleton*> s_instance;
    
public:
    // Deleted copy operations
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    
    // Thread-safe instance accessor with double-checked locking
    static Singleton* getInstance() {
        Singleton* instance = s_instance.load(std::memory_order_acquire);
        
        // First check - outside the lock
        if (instance == nullptr) {
            // Lock only if instance needs to be created
            std::lock_guard<std::mutex> lock(s_mutex);
            
            // Double-check after acquiring the lock
            instance = s_instance.load(std::memory_order_relaxed);
            if (instance == nullptr) {
                // Create the instance
                instance = new Singleton();
                s_instance.store(instance, std::memory_order_release);
            }
        }
        
        return instance;
    }
};

// Initialize static members
std::mutex Singleton::s_mutex;
std::atomic<Singleton*> Singleton::s_instance(nullptr);

void double_checked_locking_demo() {
    std::cout << "\n=== Double-Checked Locking Demo ===" << std::endl;
    
    // Function that tries to get the Singleton instance
    auto get_instance_fn = [](int thread_id) {
        std::cout << "Thread " << thread_id << " attempting to get Singleton instance..." << std::endl;
        Singleton* instance = Singleton::getInstance();
        std::cout << "Thread " << thread_id << " got instance at address: " 
                  << instance << std::endl;
    };
    
    // Launch multiple threads
    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back(get_instance_fn, i + 1);
    }
    
    // Wait for all threads
    for (auto& thread : threads) {
        thread.join();
    }
    
    std::cout << "Double-checked locking demo completed. Singleton should only be created once." << std::endl;
}

// Example 8: Lock-free queue
// LockFreeQueue class declared outside the function to allow static constants
class LockFreeQueue {
private:
    static const int MAX_SIZE = 100;
    std::atomic<int> items[MAX_SIZE];
    std::atomic<int> head{0};
    std::atomic<int> tail{0};
    
public:
    LockFreeQueue() {
        // Initialize all slots to empty (-1)
        for (int i = 0; i < MAX_SIZE; ++i) {
            items[i].store(-1, std::memory_order_relaxed);
        }
    }
    
    bool enqueue(int value) {
        int current_tail = tail.load(std::memory_order_relaxed);
        int next_tail = (current_tail + 1) % MAX_SIZE;
        
        // Check if queue is full
        if (next_tail == head.load(std::memory_order_acquire)) {
            return false;  // Queue full
        }
        
        // Add item to the queue
        items[current_tail].store(value, std::memory_order_relaxed);
        
        // Update tail with release memory ordering
        tail.store(next_tail, std::memory_order_release);
        return true;
    }
    
    bool dequeue(int& result) {
        int current_head = head.load(std::memory_order_relaxed);
        
        // Check if queue is empty
        if (current_head == tail.load(std::memory_order_acquire)) {
            return false;  // Queue empty
        }
        
        // Get the item
        result = items[current_head].load(std::memory_order_relaxed);
        
        // Mark slot as empty for debugging
        items[current_head].store(-1, std::memory_order_relaxed);
        
        // Update head with release memory ordering
        head.store((current_head + 1) % MAX_SIZE, std::memory_order_release);
        return true;
    }
};

void lock_free_queue_demo() {
    std::cout << "\n=== Lock-Free Programming Demo ===" << std::endl;
    
    // Create a shared queue
    LockFreeQueue queue;
    
    // Producer thread
    auto producer_fn = [&queue](int start_value, int count) {
        for (int i = 0; i < count; ++i) {
            int value = start_value + i;
            while (!queue.enqueue(value)) {
                // Queue is full, yield and try again
                std::this_thread::yield();
            }
        }
    };
    
    // Consumer thread
    auto consumer_fn = [&queue](int expected_count, int consumer_id) {
        int value;
        int received_count = 0;
        int sum = 0;
        
        while (received_count < expected_count) {
            if (queue.dequeue(value)) {
                sum += value;
                received_count++;
            } else {
                // Queue is empty, yield and try again
                std::this_thread::yield();
            }
        }
        
        std::cout << "Consumer " << consumer_id << " received " << received_count 
                  << " items with sum: " << sum << std::endl;
    };
    
    // Launch producer and consumer threads
    std::cout << "Launching producer and consumer threads..." << std::endl;
    
    const int items_per_producer = 1000;
    const int num_producers = 2;
    const int num_consumers = 2;
    const int items_per_consumer = (items_per_producer * num_producers) / num_consumers;
    
    std::vector<std::thread> producers;
    for (int i = 0; i < num_producers; ++i) {
        producers.emplace_back(producer_fn, i * items_per_producer, items_per_producer);
    }
    
    std::vector<std::thread> consumers;
    for (int i = 0; i < num_consumers; ++i) {
        consumers.emplace_back(consumer_fn, items_per_consumer, i + 1);
    }
    
    // Wait for all threads
    for (auto& producer : producers) {
        producer.join();
    }
    
    for (auto& consumer : consumers) {
        consumer.join();
    }
    
    std::cout << "Lock-free queue demo completed. No locks were used." << std::endl;
}

// Main function to run the data races demos
int data_races_main() {
    std::cout << "=== Data Races and Thread Safety Demo ===" << std::endl;
    
    // Run demos showing data races
    std::cout << "\n--- Part 1: Data Race Problems ---" << std::endl;
    basic_data_race_demo();
    read_write_race_demo();
    
    // Run demos showing thread safety solutions
    std::cout << "\n--- Part 2: Thread Safety Solutions ---" << std::endl;
    mutex_solution_demo();
    atomic_solution_demo();
    thread_local_solution_demo();
    
    // Run demos of advanced thread safety patterns
    std::cout << "\n--- Part 3: Advanced Thread Safety Patterns ---" << std::endl;
    reader_writer_lock_demo();
    double_checked_locking_demo();
    lock_free_queue_demo();
    
    std::cout << "\nData races and thread safety demonstration completed" << std::endl;
    return 0;
} 