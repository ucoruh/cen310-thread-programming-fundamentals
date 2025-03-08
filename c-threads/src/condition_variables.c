/**
 * @file condition_variables.c
 * @brief Thread signaling and waiting mechanisms using Windows condition variables
 */

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

// Shared data protected by critical section
typedef struct {
    int ready;              // Flag indicating data is ready
    int data;               // The shared data
    CRITICAL_SECTION cs;    // Critical section for synchronization
    CONDITION_VARIABLE cv;  // Condition variable for signaling
} shared_data_t;

// Initialize shared data structure
void init_shared_data(shared_data_t* shared_data) {
    shared_data->ready = 0;
    shared_data->data = 0;
    
    // Initialize critical section
    InitializeCriticalSection(&shared_data->cs);
    
    // Initialize condition variable
    InitializeConditionVariable(&shared_data->cv);
    
    printf("Shared data initialized\n");
}

// Clean up shared data structure
void cleanup_shared_data(shared_data_t* shared_data) {
    // Delete critical section
    DeleteCriticalSection(&shared_data->cs);
    
    // Note: Condition variables do not need explicit cleanup in Windows
    
    printf("Shared data cleaned up\n");
}

// Consumer thread function
DWORD WINAPI consumer_thread(LPVOID arg) {
    shared_data_t* shared_data = (shared_data_t*)arg;
    
    printf("Consumer: Waiting for data to be ready\n");
    
    // Enter critical section
    EnterCriticalSection(&shared_data->cs);
    
    // Wait until data is ready
    while (!shared_data->ready) {
        printf("Consumer: Waiting on condition...\n");
        
        // Wait for the condition variable to be signaled
        // This automatically releases the critical section while waiting
        SleepConditionVariableCS(&shared_data->cv, &shared_data->cs, INFINITE);
        
        printf("Consumer: Condition signaled, checking if data ready\n");
    }
    
    // At this point, data is ready and we own the critical section
    printf("Consumer: Data is ready, value = %d\n", shared_data->data);
    
    // Process the data
    int result = shared_data->data * 2;
    printf("Consumer: Processed data, result = %d\n", result);
    
    // Reset the ready flag
    shared_data->ready = 0;
    
    // Leave critical section
    LeaveCriticalSection(&shared_data->cs);
    
    return 0;
}

// Producer thread function
DWORD WINAPI producer_thread(LPVOID arg) {
    shared_data_t* shared_data = (shared_data_t*)arg;
    
    // Simulate some work before producing data
    printf("Producer: Working on producing data...\n");
    Sleep(2000); // Sleep for 2 seconds
    
    // Enter critical section
    EnterCriticalSection(&shared_data->cs);
    
    // Update the shared data
    shared_data->data = 42;
    shared_data->ready = 1;
    
    printf("Producer: Data is ready (value = %d)\n", shared_data->data);
    
    // Signal the condition variable
    WakeConditionVariable(&shared_data->cv);
    
    // Leave critical section
    LeaveCriticalSection(&shared_data->cs);
    
    return 0;
}

// Demo for simple signal/wait with condition variables
void simple_condition_demo() {
    HANDLE threads[2];
    shared_data_t shared_data;
    
    printf("\n=== Simple Condition Variable Demo ===\n");
    
    // Initialize shared data
    init_shared_data(&shared_data);
    
    // Create consumer thread (waits for condition)
    threads[0] = CreateThread(
        NULL,                // Default security attributes
        0,                   // Default stack size
        consumer_thread,     // Thread function
        &shared_data,        // Argument to thread function
        0,                   // Default creation flags
        NULL                 // Don't store thread ID
    );
    
    if (threads[0] == NULL) {
        fprintf(stderr, "Error creating consumer thread\n");
        cleanup_shared_data(&shared_data);
        exit(EXIT_FAILURE);
    }
    
    // Create producer thread (signals condition)
    threads[1] = CreateThread(
        NULL,                // Default security attributes
        0,                   // Default stack size
        producer_thread,     // Thread function
        &shared_data,        // Argument to thread function
        0,                   // Default creation flags
        NULL                 // Don't store thread ID
    );
    
    if (threads[1] == NULL) {
        fprintf(stderr, "Error creating producer thread\n");
        CloseHandle(threads[0]);
        cleanup_shared_data(&shared_data);
        exit(EXIT_FAILURE);
    }
    
    // Wait for both threads to finish
    WaitForMultipleObjects(2, threads, TRUE, INFINITE);
    
    // Close thread handles
    CloseHandle(threads[0]);
    CloseHandle(threads[1]);
    
    // Clean up shared data
    cleanup_shared_data(&shared_data);
    
    printf("Simple condition variable demo completed\n");
}

// Broadcast example with multiple consumers
#define NUM_CONSUMERS 3

DWORD WINAPI broadcast_consumer_thread(LPVOID arg) {
    shared_data_t* shared_data = (shared_data_t*)arg;
    int thread_id = GetCurrentThreadId() % 1000; // Use last 3 digits for readability
    
    printf("Consumer %d: Waiting for broadcast signal\n", thread_id);
    
    // Enter critical section
    EnterCriticalSection(&shared_data->cs);
    
    // Wait until data is ready
    while (!shared_data->ready) {
        printf("Consumer %d: Waiting on condition...\n", thread_id);
        SleepConditionVariableCS(&shared_data->cv, &shared_data->cs, INFINITE);
        printf("Consumer %d: Woke up from condition wait\n", thread_id);
    }
    
    // Process the data
    printf("Consumer %d: Received broadcast signal, data = %d\n", thread_id, shared_data->data);
    
    // Leave critical section
    LeaveCriticalSection(&shared_data->cs);
    
    return 0;
}

DWORD WINAPI broadcast_producer_thread(LPVOID arg) {
    shared_data_t* shared_data = (shared_data_t*)arg;
    
    // Simulate work before broadcast
    printf("Producer: Working before broadcast...\n");
    Sleep(3000); // Sleep for 3 seconds
    
    // Enter critical section
    EnterCriticalSection(&shared_data->cs);
    
    // Update shared data
    shared_data->data = 100;
    shared_data->ready = 1;
    
    printf("Producer: Broadcasting to all consumers, data = %d\n", shared_data->data);
    
    // Wake all waiting threads
    WakeAllConditionVariable(&shared_data->cv);
    
    // Leave critical section
    LeaveCriticalSection(&shared_data->cs);
    
    return 0;
}

// Demo for broadcasting to multiple threads
void broadcast_condition_demo() {
    HANDLE threads[NUM_CONSUMERS + 1]; // Consumers + 1 producer
    shared_data_t shared_data;
    
    printf("\n=== Broadcast Condition Variable Demo ===\n");
    
    // Initialize shared data
    init_shared_data(&shared_data);
    
    // Create multiple consumer threads
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        threads[i] = CreateThread(
            NULL,                      // Default security attributes
            0,                         // Default stack size
            broadcast_consumer_thread, // Thread function
            &shared_data,              // Argument to thread function
            0,                         // Default creation flags
            NULL                       // Don't store thread ID
        );
        
        if (threads[i] == NULL) {
            fprintf(stderr, "Error creating consumer thread %d\n", i);
            
            // Close already created threads
            for (int j = 0; j < i; j++) {
                CloseHandle(threads[j]);
            }
            
            cleanup_shared_data(&shared_data);
            exit(EXIT_FAILURE);
        }
    }
    
    // Create producer thread
    threads[NUM_CONSUMERS] = CreateThread(
        NULL,                       // Default security attributes
        0,                          // Default stack size
        broadcast_producer_thread,  // Thread function
        &shared_data,               // Argument to thread function
        0,                          // Default creation flags
        NULL                        // Don't store thread ID
    );
    
    if (threads[NUM_CONSUMERS] == NULL) {
        fprintf(stderr, "Error creating producer thread\n");
        
        // Close consumer threads
        for (int i = 0; i < NUM_CONSUMERS; i++) {
            CloseHandle(threads[i]);
        }
        
        cleanup_shared_data(&shared_data);
        exit(EXIT_FAILURE);
    }
    
    // Wait for all threads to finish
    WaitForMultipleObjects(NUM_CONSUMERS + 1, threads, TRUE, INFINITE);
    
    // Close thread handles
    for (int i = 0; i < NUM_CONSUMERS + 1; i++) {
        CloseHandle(threads[i]);
    }
    
    // Clean up shared data
    cleanup_shared_data(&shared_data);
    
    printf("Broadcast condition variable demo completed\n");
}

// Main function to run the demos
int condition_variables_main() {
    printf("=== Condition Variables Demo ===\n");
    
    // Run the simple condition variable demo
    simple_condition_demo();
    
    // Run the broadcast condition variable demo
    broadcast_condition_demo();
    
    printf("Condition variables demo completed\n");
    return 0;
} 