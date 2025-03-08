/**
 * @file thread_basics.c
 * @brief Basic thread creation, joining, and detachment examples using Windows API
 */

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

// Simple thread function - returns the thread ID as exit code directly instead of using memory allocation
DWORD WINAPI thread_function(LPVOID arg) {
    int thread_id = *((int*)arg);
    printf("Thread %d is running\n", thread_id);
    Sleep(1000); // Sleep for 1 second
    printf("Thread %d is exiting\n", thread_id);
    
    // Just return the thread ID directly as the exit code
    // This avoids memory allocation issues
    return (DWORD)(thread_id * 10);
}

// Detached thread function
DWORD WINAPI detached_thread_function(LPVOID arg) {
    int* thread_id_ptr = (int*)arg;
    int thread_id = *thread_id_ptr;
    
    printf("Detached thread %d is running\n", thread_id);
    
    // Clean up the argument since the caller won't join this thread
    // The argument must be heap-allocated by the caller
    free(thread_id_ptr);
    
    Sleep(2000); // Sleep for 2 seconds
    printf("Detached thread %d is exiting\n", thread_id);
    return 0;
}

// Demo for basic thread creation and joining
void thread_creation_demo() {
    HANDLE thread_handle;
    int thread_arg = 1; // Use stack variable since we'll wait for thread completion
    DWORD thread_id;
    
    printf("\n=== Thread Creation and Joining Demo ===\n");
    
    // Create a new thread
    thread_handle = CreateThread(
        NULL,               // Default security attributes
        0,                  // Default stack size
        thread_function,    // Thread function
        &thread_arg,        // Argument to thread function (stack variable is ok since we join)
        0,                  // Default creation flags
        &thread_id          // Receive thread identifier
    );
    
    if (thread_handle == NULL) {
        printf("Error creating thread: %d\n", GetLastError());
        exit(EXIT_FAILURE);
    }
    
    printf("Main thread: Created thread with ID %lu\n", thread_id);
    
    // Wait for the thread to finish
    DWORD wait_result = WaitForSingleObject(thread_handle, INFINITE);
    if (wait_result != WAIT_OBJECT_0) {
        printf("Error waiting for thread: %d\n", GetLastError());
        CloseHandle(thread_handle);
        exit(EXIT_FAILURE);
    }
    
    // Get the thread's exit code
    DWORD exit_code;
    if (!GetExitCodeThread(thread_handle, &exit_code)) {
        printf("Error getting thread exit code: %d\n", GetLastError());
        CloseHandle(thread_handle);
        exit(EXIT_FAILURE);
    }
    
    // The exit code is directly the result (thread_id * 10)
    printf("Main thread: Thread returned value: %lu\n", exit_code);
    
    // Close the thread handle
    CloseHandle(thread_handle);
}

// Demo for thread detachment
void thread_detachment_demo() {
    HANDLE thread_handle;
    int* arg;
    DWORD thread_id;
    
    printf("\n=== Thread Detachment Demo ===\n");
    
    // Allocate memory for the argument since the thread will outlive this function
    arg = malloc(sizeof(int));
    if (arg == NULL) {
        printf("Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }
    *arg = 2;
    
    // Create a new thread
    thread_handle = CreateThread(
        NULL,                   // Default security attributes
        0,                      // Default stack size
        detached_thread_function, // Thread function
        arg,                    // Argument to thread function
        0,                      // Default creation flags
        &thread_id              // Receives thread identifier
    );
    
    if (thread_handle == NULL) {
        printf("Thread creation failed with error: %d\n", GetLastError());
        free(arg);
        exit(EXIT_FAILURE);
    }
    
    // "Detach" the thread by closing its handle - we won't wait for it to finish
    CloseHandle(thread_handle);
    
    printf("Main thread: Detached thread %lu\n", thread_id);
    printf("Main thread: Continuing without waiting for the detached thread\n");
    
    // Sleep briefly so we can see the detached thread output
    Sleep(1000);
}

// Main function to run the demos
int thread_basics_main() {
    printf("=== Thread Basics Demo ===\n");
    
    // Run the thread creation and joining demo
    thread_creation_demo();
    
    // Run the thread detachment demo
    thread_detachment_demo();
    
    // Sleep to allow the detached thread to complete
    printf("\nMain thread: Sleeping to allow detached thread to complete...\n");
    Sleep(3000);
    
    printf("Thread basics demo completed\n");
    return 0;
} 