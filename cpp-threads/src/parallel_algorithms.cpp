/**
 * @file parallel_algorithms.cpp
 * @brief Demonstration of C++17 parallel algorithms
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <random>
#include <chrono>
#include <execution>
#include <string>
#include <functional>
#include <iomanip>

// Function to measure execution time of a function
template<typename Func, typename... Args>
auto measure_time(Func func, Args&&... args) {
    auto start = std::chrono::high_resolution_clock::now();
    
    // Call the function with its arguments
    auto result = func(std::forward<Args>(args)...);
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    return std::make_pair(result, duration.count());
}

// Function to print duration with formatted output
void print_duration(const std::string& label, long duration) {
    std::cout << std::left << std::setw(25) << label << ": " 
              << duration << " ms" << std::endl;
}

// Fill a vector with random integers
void fill_random(std::vector<int>& vec, int min, int max) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(min, max);
    
    for (auto& element : vec) {
        element = distrib(gen);
    }
}

// Parallel for_each demonstration
void parallel_for_each_demo() {
    std::cout << "\n=== std::for_each with Parallel Execution Policies ===" << std::endl;
    
    // Create a large vector
    const size_t size = 10'000'000;
    std::vector<int> data(size);
    fill_random(data, 1, 100);
    
    // Function to process elements (simple but non-trivial)
    auto process = [](int& x) { 
        x = static_cast<int>(std::sqrt(x) * 10); 
    };
    
    // Sequential execution
    auto [_, seq_time] = measure_time([&data, &process]() {
        std::for_each(std::execution::seq, data.begin(), data.end(), process);
        return 0;
    });
    
    // Parallel execution
    auto [__, par_time] = measure_time([&data, &process]() {
        std::for_each(std::execution::par, data.begin(), data.end(), process);
        return 0;
    });
    
    // Parallel unsequenced execution
    auto [___, par_unseq_time] = measure_time([&data, &process]() {
        std::for_each(std::execution::par_unseq, data.begin(), data.end(), process);
        return 0;
    });
    
    // Print execution times
    print_duration("Sequential", seq_time);
    print_duration("Parallel", par_time);
    print_duration("Parallel Unsequenced", par_unseq_time);
    
    // Calculate speedup
    float par_speedup = static_cast<float>(seq_time) / par_time;
    float par_unseq_speedup = static_cast<float>(seq_time) / par_unseq_time;
    
    std::cout << "Parallel speedup: " << std::fixed << std::setprecision(2) << par_speedup << "x" << std::endl;
    std::cout << "Parallel unsequenced speedup: " << std::fixed << std::setprecision(2) << par_unseq_speedup << "x" << std::endl;
}

// Parallel transform demonstration
void parallel_transform_demo() {
    std::cout << "\n=== std::transform with Parallel Execution Policies ===" << std::endl;
    
    // Create a large vector
    const size_t size = 10'000'000;
    std::vector<int> input(size);
    std::vector<int> output(size);
    fill_random(input, 1, 100);
    
    // Transformation function
    auto transform_func = [](int x) { 
        return static_cast<int>(std::pow(x, 1.5)); 
    };
    
    // Sequential execution
    auto [_, seq_time] = measure_time([&input, &output, &transform_func]() {
        std::transform(std::execution::seq, 
                     input.begin(), input.end(), 
                     output.begin(), 
                     transform_func);
        return 0;
    });
    
    // Parallel execution
    auto [__, par_time] = measure_time([&input, &output, &transform_func]() {
        std::transform(std::execution::par, 
                     input.begin(), input.end(), 
                     output.begin(), 
                     transform_func);
        return 0;
    });
    
    // Parallel unsequenced execution
    auto [___, par_unseq_time] = measure_time([&input, &output, &transform_func]() {
        std::transform(std::execution::par_unseq, 
                     input.begin(), input.end(), 
                     output.begin(), 
                     transform_func);
        return 0;
    });
    
    // Print execution times
    print_duration("Sequential", seq_time);
    print_duration("Parallel", par_time);
    print_duration("Parallel Unsequenced", par_unseq_time);
    
    // Calculate speedup
    float par_speedup = static_cast<float>(seq_time) / par_time;
    float par_unseq_speedup = static_cast<float>(seq_time) / par_unseq_time;
    
    std::cout << "Parallel speedup: " << std::fixed << std::setprecision(2) << par_speedup << "x" << std::endl;
    std::cout << "Parallel unsequenced speedup: " << std::fixed << std::setprecision(2) << par_unseq_speedup << "x" << std::endl;
}

// Parallel sort demonstration
void parallel_sort_demo() {
    std::cout << "\n=== std::sort with Parallel Execution Policies ===" << std::endl;
    
    // Create a large vector
    const size_t size = 10'000'000;
    
    // Function to create and return a sorted copy of the data
    auto sorted_copy = [size]() {
        // Create the vector
        std::vector<int> data(size);
        fill_random(data, 1, 1'000'000);
        return data;
    };
    
    // Sequential sort
    auto data1 = sorted_copy();
    auto [_, seq_time] = measure_time([&data1]() {
        std::sort(std::execution::seq, data1.begin(), data1.end());
        return 0;
    });
    
    // Parallel sort
    auto data2 = sorted_copy();
    auto [__, par_time] = measure_time([&data2]() {
        std::sort(std::execution::par, data2.begin(), data2.end());
        return 0;
    });
    
    // Parallel unsequenced sort
    auto data3 = sorted_copy();
    auto [___, par_unseq_time] = measure_time([&data3]() {
        std::sort(std::execution::par_unseq, data3.begin(), data3.end());
        return 0;
    });
    
    // Print execution times
    print_duration("Sequential Sort", seq_time);
    print_duration("Parallel Sort", par_time);
    print_duration("Parallel Unsequenced Sort", par_unseq_time);
    
    // Calculate speedup
    float par_speedup = static_cast<float>(seq_time) / par_time;
    float par_unseq_speedup = static_cast<float>(seq_time) / par_unseq_time;
    
    std::cout << "Parallel sort speedup: " << std::fixed << std::setprecision(2) << par_speedup << "x" << std::endl;
    std::cout << "Parallel unsequenced sort speedup: " << std::fixed << std::setprecision(2) << par_unseq_speedup << "x" << std::endl;
}

// Parallel reduce demonstration
void parallel_reduce_demo() {
    std::cout << "\n=== std::reduce with Parallel Execution Policies ===" << std::endl;
    
    // Create a large vector
    const size_t size = 100'000'000;
    std::vector<double> data(size, 1.0);  // Initialize with 1.0
    
    // Sequential reduce (same as std::accumulate)
    auto [seq_result, seq_time] = measure_time([&data]() {
        return std::reduce(std::execution::seq, data.begin(), data.end(), 0.0);
    });
    
    // Parallel reduce
    auto [par_result, par_time] = measure_time([&data]() {
        return std::reduce(std::execution::par, data.begin(), data.end(), 0.0);
    });
    
    // Parallel unsequenced reduce
    auto [par_unseq_result, par_unseq_time] = measure_time([&data]() {
        return std::reduce(std::execution::par_unseq, data.begin(), data.end(), 0.0);
    });
    
    // Print results and execution times
    std::cout << "Sequential reduce result: " << seq_result << std::endl;
    std::cout << "Parallel reduce result: " << par_result << std::endl;
    std::cout << "Parallel unsequenced reduce result: " << par_unseq_result << std::endl;
    
    print_duration("Sequential Reduce", seq_time);
    print_duration("Parallel Reduce", par_time);
    print_duration("Parallel Unsequenced Reduce", par_unseq_time);
    
    // Calculate speedup
    float par_speedup = static_cast<float>(seq_time) / par_time;
    float par_unseq_speedup = static_cast<float>(seq_time) / par_unseq_time;
    
    std::cout << "Parallel reduce speedup: " << std::fixed << std::setprecision(2) << par_speedup << "x" << std::endl;
    std::cout << "Parallel unsequenced reduce speedup: " << std::fixed << std::setprecision(2) << par_unseq_speedup << "x" << std::endl;
}

// Parallel transform_reduce demonstration
void parallel_transform_reduce_demo() {
    std::cout << "\n=== std::transform_reduce with Parallel Execution Policies ===" << std::endl;
    
    // Create two large vectors
    const size_t size = 50'000'000;
    std::vector<double> v1(size);
    std::vector<double> v2(size);
    
    // Fill with some values
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);
    
    for (size_t i = 0; i < size; ++i) {
        v1[i] = dis(gen);
        v2[i] = dis(gen);
    }
    
    // Compute dot product: sum(v1[i] * v2[i])
    // Sequential transform_reduce
    auto [seq_result, seq_time] = measure_time([&v1, &v2]() {
        return std::transform_reduce(std::execution::seq,
                                  v1.begin(), v1.end(),
                                  v2.begin(),
                                  0.0);
    });
    
    // Parallel transform_reduce
    auto [par_result, par_time] = measure_time([&v1, &v2]() {
        return std::transform_reduce(std::execution::par,
                                  v1.begin(), v1.end(),
                                  v2.begin(),
                                  0.0);
    });
    
    // Parallel unsequenced transform_reduce
    auto [par_unseq_result, par_unseq_time] = measure_time([&v1, &v2]() {
        return std::transform_reduce(std::execution::par_unseq,
                                  v1.begin(), v1.end(),
                                  v2.begin(),
                                  0.0);
    });
    
    // Print results and execution times
    std::cout << "Dot product sequential: " << seq_result << std::endl;
    std::cout << "Dot product parallel: " << par_result << std::endl;
    std::cout << "Dot product parallel unsequenced: " << par_unseq_result << std::endl;
    
    print_duration("Sequential", seq_time);
    print_duration("Parallel", par_time);
    print_duration("Parallel Unsequenced", par_unseq_time);
    
    // Calculate speedup
    float par_speedup = static_cast<float>(seq_time) / par_time;
    float par_unseq_speedup = static_cast<float>(seq_time) / par_unseq_time;
    
    std::cout << "Parallel speedup: " << std::fixed << std::setprecision(2) << par_speedup << "x" << std::endl;
    std::cout << "Parallel unsequenced speedup: " << std::fixed << std::setprecision(2) << par_unseq_speedup << "x" << std::endl;
}

// Find first occurrence in parallel
void parallel_find_demo() {
    std::cout << "\n=== std::find and std::find_if with Parallel Execution Policies ===" << std::endl;
    
    // Create a large vector
    const size_t size = 100'000'000;
    std::vector<int> data(size);
    
    // Fill with ascending values
    std::iota(data.begin(), data.end(), 0);
    
    // Value to find (near the end of the vector to maximize search time)
    const int value_to_find = size - 100;
    
    // Predicate for find_if
    auto is_target = [value_to_find](int x) { return x == value_to_find; };
    
    // Sequential find
    auto [seq_result, seq_time] = measure_time([&data, value_to_find]() {
        return std::find(std::execution::seq, data.begin(), data.end(), value_to_find);
    });
    
    // Parallel find
    auto [par_result, par_time] = measure_time([&data, value_to_find]() {
        return std::find(std::execution::par, data.begin(), data.end(), value_to_find);
    });
    
    // Sequential find_if
    auto [seq_if_result, seq_if_time] = measure_time([&data, &is_target]() {
        return std::find_if(std::execution::seq, data.begin(), data.end(), is_target);
    });
    
    // Parallel find_if
    auto [par_if_result, par_if_time] = measure_time([&data, &is_target]() {
        return std::find_if(std::execution::par, data.begin(), data.end(), is_target);
    });
    
    // Verify all results are correct
    if (*seq_result == value_to_find && 
        *par_result == value_to_find &&
        *seq_if_result == value_to_find &&
        *par_if_result == value_to_find) {
        std::cout << "All find operations found the correct value: " << value_to_find << std::endl;
    } else {
        std::cout << "Error: Not all find operations found the correct value!" << std::endl;
    }
    
    // Print execution times
    print_duration("Sequential find", seq_time);
    print_duration("Parallel find", par_time);
    print_duration("Sequential find_if", seq_if_time);
    print_duration("Parallel find_if", par_if_time);
    
    // Calculate speedup
    float find_speedup = static_cast<float>(seq_time) / par_time;
    float find_if_speedup = static_cast<float>(seq_if_time) / par_if_time;
    
    std::cout << "Parallel find speedup: " << std::fixed << std::setprecision(2) << find_speedup << "x" << std::endl;
    std::cout << "Parallel find_if speedup: " << std::fixed << std::setprecision(2) << find_if_speedup << "x" << std::endl;
}

// Main function to run the parallel algorithms demos
int parallel_algorithms_main() {
    std::cout << "=== C++17 Parallel Algorithms Demo ===" << std::endl;
    
    // Run demos for different parallel algorithms
    parallel_for_each_demo();
    parallel_transform_demo();
    parallel_sort_demo();
    parallel_reduce_demo();
    parallel_transform_reduce_demo();
    parallel_find_demo();
    
    std::cout << "\nParallel algorithms demonstration completed" << std::endl;
    return 0;
} 