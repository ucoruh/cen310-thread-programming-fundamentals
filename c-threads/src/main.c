/**
 * @file main.c
 * @brief Main entry point for the C threading demos
 */

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include <shellapi.h>  // For CommandLineToArgvW function
#include <string.h>    // For strlen function

// Function declarations from other source files
extern int thread_basics_main();
extern int mutex_demo_main();
extern int condition_variables_main();
extern int producer_consumer_main();
extern int thread_specific_data_main();
extern int thread_cancellation_main();
extern int thread_pool_main();

// Main menu display function
void display_menu() {
    printf("\n=== C Threads Programming Demo Menu ===\n");
    printf("1. Thread Basics (Creation, Joining, Detachment)\n");
    printf("2. Mutex Demo (Synchronization)\n");
    printf("3. Condition Variables Demo\n");
    printf("4. Producer-Consumer Pattern\n");
    printf("5. Thread-Specific Data\n");
    printf("6. Thread Cancellation\n");
    printf("7. Thread Pool\n");
    printf("8. Run All Demos\n");
    printf("0. Exit\n");
    printf("Enter your choice: ");
}

// Run a specific demo with a header
void run_demo(int (*demo_func)(), const char* demo_name) {
    printf("\n\n%s\n", demo_name);
    printf("====");
    for (int i = 0; i < strlen(demo_name); i++) {
        printf("=");
    }
    printf("\n\n");
    
    demo_func();
    
    printf("\n\n%s completed.\n", demo_name);
    printf("Press Enter to continue...");
    getchar();
}

int main() {
    int choice;
    BOOL interactive = TRUE;
    
    // Check if there are command line arguments
    LPWSTR *szArglist;
    int nArgs;
    
    szArglist = CommandLineToArgvW(GetCommandLineW(), &nArgs);
    if (szArglist != NULL) {
        for (int i = 1; i < nArgs; i++) {
            if (wcscmp(szArglist[i], L"--run-all") == 0) {
                interactive = FALSE;
                choice = 8; // Run all demos automatically
                break;
            }
        }
        LocalFree(szArglist);
    }
    
    // Interactive mode or automatic run-all mode
    if (interactive) {
        do {
            display_menu();
            if (scanf("%d", &choice) != 1) {
                // Clear the input buffer if not a valid integer
                while (getchar() != '\n');
                choice = -1;
            }
            
            // Clear input buffer
            while (getchar() != '\n');
            
            printf("\n");
            
            switch (choice) {
                case 0:
                    printf("Exiting demo program. Goodbye!\n");
                    break;
                case 1:
                    run_demo(thread_basics_main, "Thread Basics Demo");
                    break;
                case 2:
                    run_demo(mutex_demo_main, "Mutex Demo");
                    break;
                case 3:
                    run_demo(condition_variables_main, "Condition Variables Demo");
                    break;
                case 4:
                    run_demo(producer_consumer_main, "Producer-Consumer Pattern Demo");
                    break;
                case 5:
                    run_demo(thread_specific_data_main, "Thread-Specific Data Demo");
                    break;
                case 6:
                    run_demo(thread_cancellation_main, "Thread Cancellation Demo");
                    break;
                case 7:
                    run_demo(thread_pool_main, "Thread Pool Demo");
                    break;
                case 8:
                    run_demo(thread_basics_main, "Thread Basics Demo");
                    run_demo(mutex_demo_main, "Mutex Demo");
                    run_demo(condition_variables_main, "Condition Variables Demo");
                    run_demo(producer_consumer_main, "Producer-Consumer Pattern Demo");
                    run_demo(thread_specific_data_main, "Thread-Specific Data Demo");
                    run_demo(thread_cancellation_main, "Thread Cancellation Demo");
                    run_demo(thread_pool_main, "Thread Pool Demo");
                    break;
                default:
                    printf("Invalid choice. Please try again.\n");
                    break;
            }
        } while (choice != 0);
    }
    else {
        // Non-interactive mode (run all)
        thread_basics_main();
        mutex_demo_main();
        condition_variables_main();
        producer_consumer_main();
        thread_specific_data_main();
        thread_cancellation_main();
        thread_pool_main();
        
        printf("\nAll demos completed successfully.\n");
    }
    
    return 0;
} 