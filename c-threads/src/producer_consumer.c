/**
 * @file producer_consumer.c
 * @brief Producer-consumer pattern implementation using Windows threads
 */

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include <time.h>   // For time() function

// Size of the buffer
#define BUFFER_SIZE 5

// Number of items each producer/consumer will process
#define ITEMS_PER_PRODUCER 10
#define ITEMS_PER_CONSUMER 10

// Number of producer and consumer threads
#define NUM_PRODUCERS 2
#define NUM_CONSUMERS 2

// Bounded buffer structure
typedef struct {
    int buffer[BUFFER_SIZE];   // Circular buffer
    int count;                 // Number of items in the buffer
    int in;                    // Index for next insertion
    int out;                   // Index for next removal
    CRITICAL_SECTION mutex;    // Mutex for buffer access
    CONDITION_VARIABLE not_full;   // Condition for buffer not full
    CONDITION_VARIABLE not_empty;  // Condition for buffer not empty
} bounded_buffer_t;

// Global bounded buffer
bounded_buffer_t buffer;

// Initialize the bounded buffer
void init_buffer() {
    buffer.count = 0;
    buffer.in = 0;
    buffer.out = 0;
    
    // Initialize synchronization objects
    InitializeCriticalSection(&buffer.mutex);
    InitializeConditionVariable(&buffer.not_full);
    InitializeConditionVariable(&buffer.not_empty);
    
    printf("Buffer initialized\n");
}

// Clean up the bounded buffer
void cleanup_buffer() {
    DeleteCriticalSection(&buffer.mutex);
    
    // No cleanup needed for condition variables in Windows
    
    printf("Buffer cleaned up\n");
}

// Insert an item into the buffer (producer operation)
void buffer_insert(int item) {
    // Acquire the mutex
    EnterCriticalSection(&buffer.mutex);
    
    // Wait while the buffer is full
    while (buffer.count == BUFFER_SIZE) {
        printf("Producer: Buffer full, waiting...\n");
        SleepConditionVariableCS(&buffer.not_full, &buffer.mutex, INFINITE);
    }
    
    // Insert the item into the buffer
    buffer.buffer[buffer.in] = item;
    buffer.in = (buffer.in + 1) % BUFFER_SIZE;
    buffer.count++;
    
    printf("Producer: Inserted item %d, buffer count = %d\n", item, buffer.count);
    
    // Signal that the buffer is not empty
    WakeConditionVariable(&buffer.not_empty);
    
    // Release the mutex
    LeaveCriticalSection(&buffer.mutex);
}

// Remove an item from the buffer (consumer operation)
int buffer_remove() {
    int item;
    
    // Acquire the mutex
    EnterCriticalSection(&buffer.mutex);
    
    // Wait while the buffer is empty
    while (buffer.count == 0) {
        printf("Consumer: Buffer empty, waiting...\n");
        SleepConditionVariableCS(&buffer.not_empty, &buffer.mutex, INFINITE);
    }
    
    // Remove an item from the buffer
    item = buffer.buffer[buffer.out];
    buffer.out = (buffer.out + 1) % BUFFER_SIZE;
    buffer.count--;
    
    printf("Consumer: Removed item %d, buffer count = %d\n", item, buffer.count);
    
    // Signal that the buffer is not full
    WakeConditionVariable(&buffer.not_full);
    
    // Release the mutex
    LeaveCriticalSection(&buffer.mutex);
    
    return item;
}

// Producer thread function
DWORD WINAPI pc_producer_thread(LPVOID arg) {
    int id = *((int*)arg);
    
    printf("Producer %d starting\n", id);
    
    for (int i = 0; i < ITEMS_PER_PRODUCER; i++) {
        // Generate an item (producer ID * 100 + iteration)
        int item = (id * 100) + i;
        
        // Simulate some work
        Sleep(rand() % 500 + 500);
        
        // Insert the item into the buffer
        buffer_insert(item);
        printf("Producer %d inserted item %d\n", id, item);
    }
    
    printf("Producer %d finished\n", id);
    return 0;
}

// Consumer thread function
DWORD WINAPI pc_consumer_thread(LPVOID arg) {
    int id = *((int*)arg);
    
    printf("Consumer %d starting\n", id);
    
    for (int i = 0; i < ITEMS_PER_CONSUMER; i++) {
        // Simulate some work
        Sleep(rand() % 1000 + 500);
        
        // Remove an item from the buffer
        int item = buffer_remove();
        printf("Consumer %d removed item %d\n", id, item);
    }
    
    printf("Consumer %d finished\n", id);
    return 0;
}

// Main function to run the producer-consumer demo
int producer_consumer_main() {
    HANDLE producers[NUM_PRODUCERS];
    HANDLE consumers[NUM_CONSUMERS];
    int producer_ids[NUM_PRODUCERS];
    int consumer_ids[NUM_CONSUMERS];
    
    printf("=== Producer-Consumer Pattern Demo ===\n");
    
    // Initialize random seed
    srand((unsigned int)time(NULL));
    
    // Initialize the bounded buffer
    init_buffer();
    
    // Create producer threads
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        producer_ids[i] = i + 1;
        producers[i] = CreateThread(
            NULL,                // Default security attributes
            0,                   // Default stack size
            pc_producer_thread,  // Thread function
            &producer_ids[i],    // Argument to thread function
            0,                   // Default creation flags
            NULL                 // Don't store thread ID
        );
        
        if (producers[i] == NULL) {
            fprintf(stderr, "Error creating producer thread %d\n", i + 1);
            
            // Close already created threads
            for (int j = 0; j < i; j++) {
                CloseHandle(producers[j]);
            }
            
            cleanup_buffer();
            exit(EXIT_FAILURE);
        }
    }
    
    // Create consumer threads
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        consumer_ids[i] = i + 1;
        consumers[i] = CreateThread(
            NULL,                // Default security attributes
            0,                   // Default stack size
            pc_consumer_thread,  // Thread function
            &consumer_ids[i],    // Argument to thread function
            0,                   // Default creation flags
            NULL                 // Don't store thread ID
        );
        
        if (consumers[i] == NULL) {
            fprintf(stderr, "Error creating consumer thread %d\n", i + 1);
            
            // Close producer threads
            for (int j = 0; j < NUM_PRODUCERS; j++) {
                CloseHandle(producers[j]);
            }
            
            // Close already created consumer threads
            for (int j = 0; j < i; j++) {
                CloseHandle(consumers[j]);
            }
            
            cleanup_buffer();
            exit(EXIT_FAILURE);
        }
    }
    
    // Wait for all producer threads to finish
    WaitForMultipleObjects(NUM_PRODUCERS, producers, TRUE, INFINITE);
    
    // Wait for all consumer threads to finish
    WaitForMultipleObjects(NUM_CONSUMERS, consumers, TRUE, INFINITE);
    
    // Close all thread handles
    for (int i = 0; i < NUM_PRODUCERS; i++) {
        CloseHandle(producers[i]);
    }
    
    for (int i = 0; i < NUM_CONSUMERS; i++) {
        CloseHandle(consumers[i]);
    }
    
    // Clean up the buffer
    cleanup_buffer();
    
    printf("Producer-consumer demo completed\n");
    return 0;
} 