/**
 * @file main.cpp
 * @brief Main entry point for the C++ threading demos
 */

#include <iostream>
#include <string>
#include <Windows.h>

// Function declarations from other source files
extern int thread_basics_main();
extern int synchronization_main();
extern int atomic_operations_main();
extern int async_patterns_main();
extern int parallel_algorithms_main();
extern int data_races_main();

// Main menu display function
void display_menu() {
    std::cout << "\n=== C++ Threads Programming Demo Menu ===" << std::endl;
    std::cout << "1. Thread Basics (Creation, Joining, Detachment)" << std::endl;
    std::cout << "2. Synchronization (Mutex, Lock Guards)" << std::endl;
    std::cout << "3. Atomic Operations (Lock-free Programming)" << std::endl;
    std::cout << "4. Async Patterns (Futures, Promises)" << std::endl;
    std::cout << "5. Parallel Algorithms (C++17 Parallel Execution)" << std::endl;
    std::cout << "6. Data Races and Thread Safety" << std::endl;
    std::cout << "7. Run All Demos" << std::endl;
    std::cout << "0. Exit" << std::endl;
    std::cout << "Enter your choice: ";
}

// Run a specific demo with a header
void run_demo(int (*demo_func)(), const std::string& demo_name) {
    std::cout << "\n\n" << demo_name << std::endl;
    std::cout << "====";
    for (size_t i = 0; i < demo_name.length(); i++) {
        std::cout << "=";
    }
    std::cout << "\n\n";
    
    demo_func();
    
    std::cout << "\n\n" << demo_name << " completed." << std::endl;
    std::cout << "Press Enter to continue...";
    std::cin.get();
}

int main(int argc, char* argv[]) {
    int choice;
    bool interactive = true;
    
    // Check if there are command line arguments
    for (int i = 1; i < argc; i++) {
        if (std::string(argv[i]) == "--run-all") {
            interactive = false;
            choice = 7; // Run all demos automatically
            break;
        }
    }
    
    // Interactive mode or automatic run-all mode
    if (interactive) {
        do {
            display_menu();
            if (!(std::cin >> choice)) {
                // Clear the input buffer if not a valid integer
                std::cin.clear();
                std::cin.ignore(10000, '\n');
                choice = -1;
            }
            
            // Clear input buffer
            std::cin.ignore(10000, '\n');
            
            std::cout << std::endl;
            
            switch (choice) {
                case 0:
                    std::cout << "Exiting demo program. Goodbye!" << std::endl;
                    break;
                case 1:
                    run_demo(thread_basics_main, "Thread Basics Demo");
                    break;
                case 2:
                    run_demo(synchronization_main, "Synchronization Demo");
                    break;
                case 3:
                    run_demo(atomic_operations_main, "Atomic Operations Demo");
                    break;
                case 4:
                    run_demo(async_patterns_main, "Async Patterns Demo");
                    break;
                case 5:
                    run_demo(parallel_algorithms_main, "Parallel Algorithms Demo");
                    break;
                case 6:
                    run_demo(data_races_main, "Data Races Demo");
                    break;
                case 7:
                    run_demo(thread_basics_main, "Thread Basics Demo");
                    run_demo(synchronization_main, "Synchronization Demo");
                    run_demo(atomic_operations_main, "Atomic Operations Demo");
                    run_demo(async_patterns_main, "Async Patterns Demo");
                    run_demo(parallel_algorithms_main, "Parallel Algorithms Demo");
                    run_demo(data_races_main, "Data Races Demo");
                    break;
                default:
                    std::cout << "Invalid choice. Please try again." << std::endl;
                    break;
            }
        } while (choice != 0);
    }
    else {
        // Non-interactive mode (run all)
        thread_basics_main();
        synchronization_main();
        atomic_operations_main();
        async_patterns_main();
        parallel_algorithms_main();
        data_races_main();
        
        std::cout << "\nAll demos completed successfully." << std::endl;
    }
    
    return 0;
} 