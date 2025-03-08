/**
 * @file thread_basics.cpp
 * @brief Demonstration of basic C++ thread operations
 */

#include <iostream>
#include <thread>
#include <chrono>
#include <vector>
#include <string>

// Simple thread function
void thread_function() {
    std::cout << "Thread function running in thread ID: " 
              << std::this_thread::get_id() << std::endl;
    
    // Simulate some work
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    
    std::cout << "Thread function finished in thread ID: " 
              << std::this_thread::get_id() << std::endl;
}

// Thread function with an argument
void thread_with_arg(int id, const std::string& message) {
    std::cout << "Thread " << id << " received message: " << message << std::endl;
    
    // Simulate some work
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    
    std::cout << "Thread " << id << " finished processing" << std::endl;
}

// Thread creation demo
void thread_creation_demo() {
    std::cout << "\n=== Thread Creation Demo ===" << std::endl;
    
    // Main thread ID
    std::cout << "Main thread ID: " << std::this_thread::get_id() << std::endl;
    
    // Create a thread with a simple function
    std::thread t1(thread_function);
    
    std::cout << "Created thread with ID: " << t1.get_id() << std::endl;
    
    // Join the thread (wait for it to finish)
    std::cout << "Main thread waiting for thread to finish..." << std::endl;
    t1.join();
    std::cout << "Thread has been joined" << std::endl;
}

// Thread with arguments demo
void thread_arguments_demo() {
    std::cout << "\n=== Thread Arguments Demo ===" << std::endl;
    
    // Create a thread with arguments
    int id = 1;
    std::string message = "Hello from the main thread!";
    
    std::thread t(thread_with_arg, id, message);
    
    // Detach the thread (let it run independently)
    std::cout << "Detaching thread..." << std::endl;
    t.detach();
    
    // Since we detached, we need to wait to see the output
    std::cout << "Main thread continues execution..." << std::endl;
    
    // Add a sleep to allow the detached thread to execute
    std::this_thread::sleep_for(std::chrono::milliseconds(2000));
}

// Lambda thread demo
void lambda_thread_demo() {
    std::cout << "\n=== Lambda Thread Demo ===" << std::endl;
    
    // Create a thread with a lambda function
    int data = 42;
    
    std::thread t([data]() {
        std::cout << "Lambda thread received data: " << data << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        std::cout << "Lambda thread finished" << std::endl;
    });
    
    // Join the thread
    t.join();
    std::cout << "Lambda thread has been joined" << std::endl;
}

// Multiple threads demo
void multiple_threads_demo() {
    std::cout << "\n=== Multiple Threads Demo ===" << std::endl;
    
    const int NUM_THREADS = 5;
    
    // Vector to store threads
    std::vector<std::thread> threads;
    
    // Create multiple threads
    for (int i = 0; i < NUM_THREADS; ++i) {
        threads.emplace_back([i]() {
            std::cout << "Thread " << i << " starting with ID: " 
                      << std::this_thread::get_id() << std::endl;
            
            // Simulate different workloads
            std::this_thread::sleep_for(std::chrono::milliseconds(200 * (i + 1)));
            
            std::cout << "Thread " << i << " finished" << std::endl;
        });
    }
    
    std::cout << "Created " << NUM_THREADS << " threads" << std::endl;
    
    // Join all threads
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "All threads have been joined" << std::endl;
}

// Main function to run thread basics demos
int thread_basics_main() {
    std::cout << "=== Thread Basics Demo ===" << std::endl;
    
    // Basic thread creation
    thread_creation_demo();
    
    // Thread with arguments
    thread_arguments_demo();
    
    // Thread with lambda function
    lambda_thread_demo();
    
    // Multiple threads
    multiple_threads_demo();
    
    std::cout << "\nThread basics demonstration completed" << std::endl;
    return 0;
} 