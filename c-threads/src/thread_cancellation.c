/**
 * @file thread_cancellation.c
 * @brief Safe thread termination techniques for Windows threads
 */

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>
#include <stdbool.h>

// Structure for thread parameters
typedef struct {
    int thread_id;
    volatile bool* should_exit;  // Flag for cooperative cancellation
    HANDLE complete_event;       // Event to signal when cleanup is done
} thread_params_t;

// Thread function that checks for cancellation
DWORD WINAPI cancellable_thread(LPVOID arg) {
    thread_params_t* params = (thread_params_t*)arg;
    int thread_id = params->thread_id;
    volatile bool* should_exit = params->should_exit;
    
    printf("Thread %d: Starting work\n", thread_id);
    
    // Allocate some resources
    char* resource = (char*)malloc(100);
    if (resource == NULL) {
        fprintf(stderr, "Thread %d: Failed to allocate resource\n", thread_id);
        return 1;
    }
    
    sprintf_s(resource, 100, "Resource for thread %d", thread_id);
    printf("Thread %d: Allocated resource: %s\n", thread_id, resource);
    
    // Main work loop with cancellation points
    for (int i = 0; i < 20; i++) {
        // Check for cancellation request
        if (*should_exit) {
            printf("Thread %d: Cancellation requested, cleaning up...\n", thread_id);
            // Clean up resources
            free(resource);
            printf("Thread %d: Resources freed\n", thread_id);
            
            // Signal that cleanup is complete
            if (params->complete_event != NULL) {
                SetEvent(params->complete_event);
            }
            
            return 0;
        }
        
        // Do some work
        printf("Thread %d: Working... (%d/20)\n", thread_id, i + 1);
        Sleep(200);  // Simulate work
    }
    
    // Normal completion
    printf("Thread %d: Work completed normally\n", thread_id);
    
    // Clean up resources
    free(resource);
    printf("Thread %d: Resources freed\n", thread_id);
    
    return 0;
}

// Demo for cooperative cancellation
void cooperative_cancellation_demo() {
    HANDLE thread;
    HANDLE complete_event;
    volatile bool should_exit = false;
    thread_params_t params;
    
    printf("\n=== Cooperative Cancellation Demo ===\n");
    
    // Create event for signaling cleanup completion
    complete_event = CreateEvent(
        NULL,    // Default security attributes
        TRUE,    // Manual reset
        FALSE,   // Initial state non-signaled
        NULL     // Unnamed event
    );
    
    if (complete_event == NULL) {
        fprintf(stderr, "Failed to create event: %lu\n", GetLastError());
        return;
    }
    
    // Set up thread parameters
    params.thread_id = 1;
    params.should_exit = &should_exit;
    params.complete_event = complete_event;
    
    // Create the thread
    thread = CreateThread(
        NULL,                 // Default security attributes
        0,                    // Default stack size
        cancellable_thread,   // Thread function
        &params,              // Thread parameters
        0,                    // Default creation flags
        NULL                  // Don't store thread ID
    );
    
    if (thread == NULL) {
        fprintf(stderr, "Failed to create thread: %lu\n", GetLastError());
        CloseHandle(complete_event);
        return;
    }
    
    // Let the thread run for a while
    printf("Main thread: Letting thread run for 2 seconds...\n");
    Sleep(2000);
    
    // Request cancellation
    printf("Main thread: Requesting thread cancellation\n");
    should_exit = true;
    
    // Wait for the thread to signal it has cleaned up
    printf("Main thread: Waiting for thread to clean up...\n");
    DWORD wait_result = WaitForSingleObject(complete_event, 5000);  // 5 second timeout
    
    if (wait_result == WAIT_OBJECT_0) {
        printf("Main thread: Thread reported successful cleanup\n");
    } else if (wait_result == WAIT_TIMEOUT) {
        fprintf(stderr, "Main thread: Timeout waiting for thread cleanup\n");
    } else {
        fprintf(stderr, "Main thread: Wait error: %lu\n", GetLastError());
    }
    
    // Wait for the thread to exit
    WaitForSingleObject(thread, INFINITE);
    
    // Clean up handles
    CloseHandle(thread);
    CloseHandle(complete_event);
    
    printf("Cooperative cancellation demo completed\n");
}

// Thread function that doesn't check for cancellation
DWORD WINAPI uncancellable_thread(LPVOID arg) {
    int thread_id = *((int*)arg);
    
    printf("Uncancellable thread %d: Starting\n", thread_id);
    
    // Main work loop with no cancellation checks
    for (int i = 0; i < 10; i++) {
        printf("Uncancellable thread %d: Working... (%d/10)\n", thread_id, i + 1);
        Sleep(500);  // Simulate work
    }
    
    printf("Uncancellable thread %d: Completed\n", thread_id);
    return 0;
}

// Demo for forced termination (not recommended)
void forced_termination_demo() {
    HANDLE thread;
    int thread_id = 2;
    
    printf("\n=== Forced Termination Demo (Not Recommended) ===\n");
    
    // Create the thread
    thread = CreateThread(
        NULL,                  // Default security attributes
        0,                     // Default stack size
        uncancellable_thread,  // Thread function
        &thread_id,            // Thread parameters
        0,                     // Default creation flags
        NULL                   // Don't store thread ID
    );
    
    if (thread == NULL) {
        fprintf(stderr, "Failed to create thread: %lu\n", GetLastError());
        return;
    }
    
    // Let the thread run for a while
    printf("Main thread: Letting thread run for 2 seconds...\n");
    Sleep(2000);
    
    // Forcibly terminate the thread (not recommended)
    printf("Main thread: WARNING - About to forcibly terminate thread\n");
    printf("Main thread: This is NOT recommended as it can cause resource leaks!\n");
    
    if (TerminateThread(thread, 1)) {
        printf("Main thread: Thread terminated forcibly\n");
    } else {
        fprintf(stderr, "Main thread: Failed to terminate thread: %lu\n", GetLastError());
    }
    
    // Clean up handle
    CloseHandle(thread);
    
    printf("Forced termination demo completed\n");
    printf("WARNING: Forced termination can lead to resource leaks and other issues!\n");
    printf("It's always better to use cooperative cancellation.\n");
}

// Main function to run the demos
int thread_cancellation_main() {
    printf("=== Thread Cancellation Demo ===\n");
    
    // Run the cooperative cancellation demo
    cooperative_cancellation_demo();
    
    // Run the forced termination demo
    forced_termination_demo();
    
    printf("Thread cancellation demo completed\n");
    return 0;
} 