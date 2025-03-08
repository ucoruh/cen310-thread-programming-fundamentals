/**
 * @file mutex_demo.c
 * @brief Mutex usage patterns and deadlock avoidance examples for Windows threads
 */

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

// Global variables
#define NUM_THREADS 4
#define NUM_INCREMENTS 1000000

// Shared counter (no protection)
LONG unsafe_counter = 0;

// Shared counter (with mutex protection)
LONG safe_counter = 0;

// Mutex for protecting the counter
HANDLE counter_mutex = NULL;

// Thread function for unsafe increment
DWORD WINAPI unsafe_increment_thread(LPVOID arg) {
    int thread_id = *((int*)arg);
    printf("Unsafe thread %d starting\n", thread_id);
    
    // Repeatedly increment the counter without protection
    for (int i = 0; i < NUM_INCREMENTS; i++) {
        unsafe_counter++; // This is not atomic and can cause race conditions
    }
    
    printf("Unsafe thread %d finished\n", thread_id);
    return 0;
}

// Thread function for safe increment using mutex
DWORD WINAPI safe_increment_thread(LPVOID arg) {
    int thread_id = *((int*)arg);
    printf("Safe thread %d starting\n", thread_id);
    
    // Repeatedly increment the counter with mutex protection
    for (int i = 0; i < NUM_INCREMENTS; i++) {
        // Wait for mutex before accessing the shared counter
        WaitForSingleObject(counter_mutex, INFINITE);
        
        // Critical section - only one thread can be here at a time
        safe_counter++;
        
        // Release the mutex
        ReleaseMutex(counter_mutex);
    }
    
    printf("Safe thread %d finished\n", thread_id);
    return 0;
}

// Demo for race condition problem
void race_condition_demo() {
    HANDLE threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];
    
    printf("\n=== Race Condition Demo ===\n");
    printf("Starting %d threads to increment counter %d times each\n", 
           NUM_THREADS, NUM_INCREMENTS);
    
    // Reset counter
    unsafe_counter = 0;
    
    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i + 1;
        threads[i] = CreateThread(
            NULL,               // Default security attributes
            0,                  // Default stack size
            unsafe_increment_thread, // Thread function
            &thread_ids[i],     // Argument to thread function
            0,                  // Default creation flags
            NULL                // Don't store thread ID
        );
        
        if (threads[i] == NULL) {
            fprintf(stderr, "Error creating thread\n");
            exit(EXIT_FAILURE);
        }
    }
    
    // Wait for all threads to finish
    WaitForMultipleObjects(NUM_THREADS, threads, TRUE, INFINITE);
    
    // Close thread handles
    for (int i = 0; i < NUM_THREADS; i++) {
        CloseHandle(threads[i]);
    }
    
    // Check the final counter value
    printf("Expected counter value: %d\n", NUM_THREADS * NUM_INCREMENTS);
    printf("Actual counter value: %d\n", unsafe_counter);
    if (unsafe_counter != NUM_THREADS * NUM_INCREMENTS) {
        printf("Race condition detected! Counter value is incorrect.\n");
    }
}

// Demo for mutex protection
void mutex_protection_demo() {
    HANDLE threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];
    
    printf("\n=== Mutex Protection Demo ===\n");
    printf("Starting %d threads to increment counter %d times each (with mutex)\n", 
           NUM_THREADS, NUM_INCREMENTS);
    
    // Reset counter
    safe_counter = 0;
    
    // Create a mutex
    counter_mutex = CreateMutex(
        NULL,  // Default security attributes
        FALSE, // Initially not owned
        NULL   // Unnamed mutex
    );
    
    if (counter_mutex == NULL) {
        fprintf(stderr, "Error creating mutex\n");
        exit(EXIT_FAILURE);
    }
    
    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i + 1;
        threads[i] = CreateThread(
            NULL,                // Default security attributes
            0,                   // Default stack size
            safe_increment_thread, // Thread function
            &thread_ids[i],      // Argument to thread function
            0,                   // Default creation flags
            NULL                 // Don't store thread ID
        );
        
        if (threads[i] == NULL) {
            fprintf(stderr, "Error creating thread\n");
            CloseHandle(counter_mutex);
            exit(EXIT_FAILURE);
        }
    }
    
    // Wait for all threads to finish
    WaitForMultipleObjects(NUM_THREADS, threads, TRUE, INFINITE);
    
    // Close thread handles
    for (int i = 0; i < NUM_THREADS; i++) {
        CloseHandle(threads[i]);
    }
    
    // Close the mutex
    CloseHandle(counter_mutex);
    
    // Check the final counter value
    printf("Expected counter value: %d\n", NUM_THREADS * NUM_INCREMENTS);
    printf("Actual counter value: %d\n", safe_counter);
    if (safe_counter == NUM_THREADS * NUM_INCREMENTS) {
        printf("Mutex protection successful! Counter value is correct.\n");
    }
}

// Structure for deadlock prevention demo
typedef struct {
    int thread_id;
    HANDLE* mutex_a;
    HANDLE* mutex_b;
} deadlock_args_t;

// Demo for deadlock prevention
void deadlock_prevention_demo() {
    printf("\n=== Deadlock Prevention Demo ===\n");
    printf("Using ordered mutex acquisition to prevent deadlocks\n");
    
    // In a real scenario, we would demonstrate how to prevent deadlocks
    // Common techniques include:
    // 1. Always acquire locks in the same order
    // 2. Use try-lock and back off if not successful
    // 3. Use timeout-based lock acquisition
    
    printf("Deadlock prevention techniques:\n");
    printf("1. Always acquire locks in the same order\n");
    printf("2. Use try-lock and back off if not successful\n");
    printf("3. Use timeout-based lock acquisition\n");
}

// Main function to run the demos
int mutex_demo_main() {
    printf("=== Mutex Demo ===\n");
    
    // Run race condition demo
    race_condition_demo();
    
    // Run mutex protection demo
    mutex_protection_demo();
    
    // Run deadlock prevention demo
    deadlock_prevention_demo();
    
    printf("Mutex demo completed\n");
    return 0;
}