/**
 * @file async_patterns.cpp
 * @brief Demonstration of async patterns in C++ using future, promise, and async
 */

#include <iostream>
#include <future>
#include <thread>
#include <chrono>
#include <vector>
#include <random>
#include <exception>
#include <functional>

// Simple function to be executed asynchronously
int compute_sum(int a, int b) {
    std::cout << "Computing sum of " << a << " and " << b 
              << " in thread " << std::this_thread::get_id() << std::endl;
    
    // Simulate some work
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    
    return a + b;
}

// Function that might throw an exception
double compute_division(double a, double b) {
    std::cout << "Computing division " << a << " / " << b 
              << " in thread " << std::this_thread::get_id() << std::endl;
    
    // Simulate some work
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    
    if (b == 0) {
        throw std::runtime_error("Division by zero");
    }
    
    return a / b;
}

// Function for promise-future example
void perform_work(std::promise<int>&& promise, int value) {
    try {
        std::cout << "Worker thread " << std::this_thread::get_id() 
                  << " started, computing value..." << std::endl;
        
        // Simulate complex calculation
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        
        // Set the result
        int result = value * value;
        promise.set_value(result);
        
        std::cout << "Worker thread completed, result: " << result << std::endl;
    }
    catch (...) {
        // Set the exception if something goes wrong
        promise.set_exception(std::current_exception());
    }
}

// Function for async demonstration
void async_demo() {
    std::cout << "\n=== std::async Demo ===" << std::endl;
    std::cout << "Main thread ID: " << std::this_thread::get_id() << std::endl;
    
    // Launch async task with default launch policy
    std::cout << "\n1. Default launch policy (implementation-defined):" << std::endl;
    std::future<int> result1 = std::async(compute_sum, 10, 20);
    
    // Do some work in parallel
    std::cout << "Main thread doing other work while async task runs..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
    // Get the result (will wait if not ready)
    std::cout << "Result: " << result1.get() << std::endl;
    
    // Launch async task with deferred execution (lazy evaluation)
    std::cout << "\n2. Deferred execution:" << std::endl;
    std::future<int> result2 = std::async(std::launch::deferred, compute_sum, 15, 25);
    
    std::cout << "Task is deferred, not yet executed..." << std::endl;
    
    // The function will only execute when we call get()
    std::cout << "Calling get(), which will execute the function now." << std::endl;
    std::cout << "Result: " << result2.get() << std::endl;
    
    // Launch async task with async execution (new thread)
    std::cout << "\n3. Async execution (guaranteed new thread):" << std::endl;
    std::future<int> result3 = std::async(std::launch::async, compute_sum, 30, 40);
    
    std::cout << "Task is running asynchronously now..." << std::endl;
    
    // Check if result is ready (non-blocking)
    for (int i = 0; i < 10; ++i) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        
        auto status = result3.wait_for(std::chrono::milliseconds(0));
        if (status == std::future_status::ready) {
            std::cout << "Result is ready!" << std::endl;
            break;
        } else {
            std::cout << "Result not ready yet, continuing to wait..." << std::endl;
        }
    }
    
    // Get the result
    std::cout << "Result: " << result3.get() << std::endl;
    
    // Exception handling with async
    std::cout << "\n4. Exception handling with async:" << std::endl;
    std::future<double> div_result = std::async(std::launch::async, compute_division, 10.0, 0.0);
    
    try {
        double result = div_result.get();
        std::cout << "Result: " << result << std::endl;
    }
    catch (const std::exception& e) {
        std::cout << "Caught exception from async task: " << e.what() << std::endl;
    }
}

// Function for promise-future demonstration
void promise_future_demo() {
    std::cout << "\n=== Promise-Future Demo ===" << std::endl;
    
    // Create a promise to get a future
    std::promise<int> promise;
    std::future<int> future = promise.get_future();
    
    // Launch a thread to perform work and fulfill the promise
    std::thread worker(perform_work, std::move(promise), 42);
    
    // Main thread can do other work
    std::cout << "Main thread " << std::this_thread::get_id() 
              << " waiting for result..." << std::endl;
    
    // Wait for and get the result
    try {
        int result = future.get();
        std::cout << "Main thread received result: " << result << std::endl;
    }
    catch (const std::exception& e) {
        std::cout << "Main thread caught exception: " << e.what() << std::endl;
    }
    
    // Join the worker thread
    worker.join();
}

// Function for packaged_task demonstration
void packaged_task_demo() {
    std::cout << "\n=== Packaged Task Demo ===" << std::endl;
    
    // Create a packaged task for compute_sum
    std::packaged_task<int(int, int)> task(compute_sum);
    
    // Get the future
    std::future<int> future = task.get_future();
    
    // Launch the task in a thread
    std::thread task_thread(std::move(task), 25, 75);
    
    // Wait for and get the result
    std::cout << "Main thread waiting for packaged task result..." << std::endl;
    std::cout << "Result: " << future.get() << std::endl;
    
    // Join the task thread
    task_thread.join();
    
    // Create a vector of packaged tasks
    std::cout << "\nRunning multiple packaged tasks:" << std::endl;
    
    std::vector<std::packaged_task<int(int, int)>> tasks;
    std::vector<std::future<int>> futures;
    
    // Create 5 tasks
    for (int i = 0; i < 5; ++i) {
        std::packaged_task<int(int, int)> new_task(compute_sum);
        futures.push_back(new_task.get_future());
        tasks.push_back(std::move(new_task));
    }
    
    // Launch each task with different parameters
    std::vector<std::thread> threads;
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back(std::move(tasks[i]), i * 10, i * 20);
    }
    
    // Collect and print all results
    int total = 0;
    for (int i = 0; i < 5; ++i) {
        int result = futures[i].get();
        std::cout << "Task " << i << " result: " << result << std::endl;
        total += result;
    }
    
    std::cout << "Sum of all results: " << total << std::endl;
    
    // Join all threads
    for (auto& thread : threads) {
        thread.join();
    }
}

// Function to demonstrate shared_future
void shared_future_demo() {
    std::cout << "\n=== Shared Future Demo ===" << std::endl;
    
    // Create a promise and get a future
    std::promise<int> promise;
    std::future<int> future = promise.get_future();
    
    // Convert to shared_future (can be copied and shared among multiple threads)
    std::shared_future<int> shared_future = future.share();
    
    // Create multiple consumer threads waiting for the same result
    auto consumer = [](std::shared_future<int> sf, int id) {
        std::cout << "Consumer " << id << " waiting for shared result..." << std::endl;
        
        try {
            int result = sf.get(); // Multiple threads can call get() on the same shared_future
            std::cout << "Consumer " << id << " received result: " << result << std::endl;
        }
        catch (const std::exception& e) {
            std::cout << "Consumer " << id << " got exception: " << e.what() << std::endl;
        }
    };
    
    // Launch consumer threads
    std::vector<std::thread> consumers;
    for (int i = 1; i <= 3; ++i) {
        consumers.emplace_back(consumer, shared_future, i);
    }
    
    // Producer sets the value after a delay
    std::cout << "Main thread will provide the value in 1 second..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    // Set the value that all consumers are waiting for
    promise.set_value(99);
    
    // Join all consumer threads
    for (auto& thread : consumers) {
        thread.join();
    }
    
    std::cout << "shared_future allows multiple threads to receive the same result" << std::endl;
}

// Function to demonstrate async error handling
void async_error_handling_demo() {
    std::cout << "\n=== Async Error Handling Demo ===" << std::endl;
    
    // Function that will throw an exception
    auto throw_error = []() -> int {
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        throw std::runtime_error("Simulated error in async task");
        // Unreachable code, but that's intentional for the demo
        // No return statement needed here
    };
    
    // Start an async task that will throw
    std::future<int> future = std::async(std::launch::async, throw_error);
    
    std::cout << "Started async task that will throw an exception" << std::endl;
    
    // Try to get the result
    try {
        int result = future.get();
        std::cout << "Result: " << result << std::endl;
    }
    catch (const std::exception& e) {
        std::cout << "Successfully caught exception from async task: " << e.what() << std::endl;
        std::cout << "This demonstrates exception propagation from async tasks" << std::endl;
    }
}

// Function to demonstrate continuations with then()
// Note: C++11/14 doesn't have built-in continuation support,
// this is a simplified example showing how it could be implemented
void continuation_demo() {
    std::cout << "\n=== Continuation Demo (manual implementation) ===" << std::endl;
    
    // Our manual implementation of a continuation
    auto then = [](std::future<int>&& future, std::function<double(int)> func) -> std::future<double> {
        // Create a promise for the continuation's result
        std::promise<double> promise;
        std::future<double> result = promise.get_future();
        
        // Start a thread to wait for the input future and apply the continuation
        std::thread([](std::promise<double> p, std::future<int> f, std::function<double(int)> fn) {
            try {
                // Wait for the input future
                int value = f.get();
                
                // Apply the continuation function
                double continued_value = fn(value);
                
                // Set the result of the continuation
                p.set_value(continued_value);
            }
            catch (...) {
                // Propagate any exceptions
                p.set_exception(std::current_exception());
            }
        }, std::move(promise), std::move(future), func).detach();
        
        return result;
    };
    
    // Start with a simple async task
    std::future<int> future = std::async(std::launch::async, []() {
        std::cout << "Initial computation running..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        return 42;
    });
    
    // Add a continuation that squares the result
    std::future<double> continuation = then(std::move(future), [](int value) -> double {
        std::cout << "Continuation running with input: " << value << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        return value * value;
    });
    
    // Get the final result
    std::cout << "Waiting for continuation result..." << std::endl;
    std::cout << "Final result: " << continuation.get() << std::endl;
}

// Main function to run async pattern demos
int async_patterns_main() {
    std::cout << "=== Async Patterns Demo ===" << std::endl;
    
    // Run the std::async demo
    async_demo();
    
    // Run the promise-future demo
    promise_future_demo();
    
    // Run the packaged_task demo
    packaged_task_demo();
    
    // Run the shared_future demo
    shared_future_demo();
    
    // Run the async error handling demo
    async_error_handling_demo();
    
    // Run the continuation demo
    continuation_demo();
    
    std::cout << "\nAsync patterns demonstration completed" << std::endl;
    return 0;
} 