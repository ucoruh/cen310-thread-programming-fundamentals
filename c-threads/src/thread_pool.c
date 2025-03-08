/**
 * @file thread_pool.c
 * @brief Basic thread pool implementation using Windows threads
 */

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include <stdbool.h>

// Maximum number of jobs in the queue
#define MAX_QUEUE_SIZE 100

// Number of worker threads in the pool
#define THREAD_POOL_SIZE 4

// Structure for a work item
typedef struct {
    void (*function)(void*);   // Function to execute
    void* argument;            // Argument to the function
} work_item_t;

// Thread pool structure
typedef struct {
    work_item_t queue[MAX_QUEUE_SIZE];  // Work queue
    int queue_size;                      // Current size of the queue
    int head;                            // Head of the queue
    int tail;                            // Tail of the queue
    
    HANDLE worker_threads[THREAD_POOL_SIZE];  // Worker threads
    CRITICAL_SECTION queue_lock;              // Lock for queue access
    CONDITION_VARIABLE queue_not_empty;       // Condition for queue not empty
    CONDITION_VARIABLE queue_not_full;        // Condition for queue not full
    
    bool shutdown;                            // Flag to signal shutdown
} thread_pool_t;

// Global thread pool
thread_pool_t* g_pool = NULL;

// Initialize the thread pool
thread_pool_t* thread_pool_init() {
    // Allocate memory for the pool
    thread_pool_t* tp = (thread_pool_t*)malloc(sizeof(thread_pool_t));
    if (tp == NULL) {
        fprintf(stderr, "Error: Failed to allocate memory for thread pool\n");
        return NULL;
    }
    
    // Initialize pool properties
    tp->queue_size = 0;
    tp->head = 0;
    tp->tail = 0;
    tp->shutdown = false;
    
    // Initialize synchronization objects
    InitializeCriticalSection(&tp->queue_lock);
    InitializeConditionVariable(&tp->queue_not_empty);
    InitializeConditionVariable(&tp->queue_not_full);
    
    printf("Thread pool initialized\n");
    
    return tp;
}

// Function declaration for worker thread
DWORD WINAPI worker_thread(LPVOID arg);

// Start the thread pool
bool thread_pool_start(thread_pool_t* tp) {
    // Create worker threads
    for (int i = 0; i < THREAD_POOL_SIZE; i++) {
        tp->worker_threads[i] = CreateThread(
            NULL,            // Default security attributes
            0,               // Default stack size
            worker_thread,   // Thread function
            tp,              // Argument to thread function (the pool)
            0,               // Default creation flags
            NULL             // Don't store thread ID
        );
        
        if (tp->worker_threads[i] == NULL) {
            fprintf(stderr, "Error creating worker thread %d\n", i);
            
            // Shutdown the pool
            tp->shutdown = true;
            WakeAllConditionVariable(&tp->queue_not_empty);
            
            // Wait for created threads to exit
            for (int j = 0; j < i; j++) {
                WaitForSingleObject(tp->worker_threads[j], INFINITE);
                CloseHandle(tp->worker_threads[j]);
            }
            
            // Clean up synchronization objects
            DeleteCriticalSection(&tp->queue_lock);
            
            return false;
        }
    }
    
    printf("Thread pool started with %d worker threads\n", THREAD_POOL_SIZE);
    
    return true;
}

// Add work to the thread pool
bool thread_pool_add_work(thread_pool_t* tp, void (*function)(void*), void* argument) {
    // Enter critical section
    EnterCriticalSection(&tp->queue_lock);
    
    // Wait while the queue is full
    while (tp->queue_size == MAX_QUEUE_SIZE && !tp->shutdown) {
        printf("Queue full, waiting...\n");
        SleepConditionVariableCS(&tp->queue_not_full, &tp->queue_lock, INFINITE);
    }
    
    // Check if pool is shutting down
    if (tp->shutdown) {
        LeaveCriticalSection(&tp->queue_lock);
        return false;
    }
    
    // Add work to the queue
    tp->queue[tp->tail].function = function;
    tp->queue[tp->tail].argument = argument;
    tp->tail = (tp->tail + 1) % MAX_QUEUE_SIZE;
    tp->queue_size++;
    
    // Signal that the queue is not empty
    WakeConditionVariable(&tp->queue_not_empty);
    
    // Leave critical section
    LeaveCriticalSection(&tp->queue_lock);
    
    return true;
}

// Worker thread function
DWORD WINAPI worker_thread(LPVOID arg) {
    thread_pool_t* tp = (thread_pool_t*)arg;
    work_item_t work;
    
    while (true) {
        // Enter critical section
        EnterCriticalSection(&tp->queue_lock);
        
        // Wait while the queue is empty
        while (tp->queue_size == 0 && !tp->shutdown) {
            SleepConditionVariableCS(&tp->queue_not_empty, &tp->queue_lock, INFINITE);
        }
        
        // Check if we should exit
        if (tp->shutdown && tp->queue_size == 0) {
            LeaveCriticalSection(&tp->queue_lock);
            break;
        }
        
        // Get work from the queue
        work.function = tp->queue[tp->head].function;
        work.argument = tp->queue[tp->head].argument;
        tp->head = (tp->head + 1) % MAX_QUEUE_SIZE;
        tp->queue_size--;
        
        // Signal that the queue is not full
        WakeConditionVariable(&tp->queue_not_full);
        
        // Leave critical section
        LeaveCriticalSection(&tp->queue_lock);
        
        // Execute the work
        work.function(work.argument);
    }
    
    printf("Worker thread exiting\n");
    return 0;
}

// Shutdown the thread pool
void thread_pool_shutdown(thread_pool_t* tp) {
    if (tp == NULL) {
        return;
    }
    
    // Enter critical section
    EnterCriticalSection(&tp->queue_lock);
    
    // Set shutdown flag
    tp->shutdown = true;
    
    // Wake up all worker threads
    WakeAllConditionVariable(&tp->queue_not_empty);
    
    // Leave critical section
    LeaveCriticalSection(&tp->queue_lock);
    
    // Wait for all worker threads to finish
    for (int i = 0; i < THREAD_POOL_SIZE; i++) {
        WaitForSingleObject(tp->worker_threads[i], INFINITE);
        CloseHandle(tp->worker_threads[i]);
    }
    
    // Clean up synchronization objects
    DeleteCriticalSection(&tp->queue_lock);
    
    // Free the pool memory
    free(tp);
    
    printf("Thread pool shut down\n");
}

// Example job data
typedef struct {
    int id;
    int value;
} job_data_t;

// Example job function
void example_job(void* arg) {
    job_data_t* data = (job_data_t*)arg;
    
    printf("Job %d starting with value %d\n", data->id, data->value);
    
    // Simulate work
    Sleep(1000 + (data->id % 3) * 500);
    
    printf("Job %d completed\n", data->id);
    
    // Free job data
    free(data);
}

// Demo function for thread pool
void thread_pool_demo() {
    printf("\n=== Thread Pool Demo ===\n");
    
    // Initialize the thread pool
    g_pool = thread_pool_init();
    if (g_pool == NULL) {
        fprintf(stderr, "Failed to initialize thread pool\n");
        return;
    }
    
    // Start the thread pool
    if (!thread_pool_start(g_pool)) {
        fprintf(stderr, "Failed to start thread pool\n");
        free(g_pool);
        return;
    }
    
    // Add jobs to the thread pool
    for (int i = 0; i < 10; i++) {
        // Allocate job data
        job_data_t* job_data = (job_data_t*)malloc(sizeof(job_data_t));
        if (job_data == NULL) {
            fprintf(stderr, "Failed to allocate job data\n");
            continue;
        }
        
        // Initialize job data
        job_data->id = i;
        job_data->value = i * 10;
        
        // Add job to the thread pool
        if (!thread_pool_add_work(g_pool, example_job, job_data)) {
            fprintf(stderr, "Failed to add job %d to the thread pool\n", i);
            free(job_data);
        } else {
            printf("Added job %d to the thread pool\n", i);
        }
    }
    
    // Wait for some time to allow jobs to complete
    printf("Waiting for jobs to complete...\n");
    Sleep(5000);
    
    // Shutdown the thread pool
    printf("Shutting down thread pool...\n");
    thread_pool_shutdown(g_pool);
    g_pool = NULL;
}

// Main function to run the thread pool demo
int thread_pool_main() {
    printf("=== Thread Pool Demo ===\n");
    
    // Run the thread pool demo
    thread_pool_demo();
    
    printf("Thread pool demo completed\n");
    return 0;
} 