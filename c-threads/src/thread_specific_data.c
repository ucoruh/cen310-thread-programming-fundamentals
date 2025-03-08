/**
 * @file thread_specific_data.c
 * @brief Thread-local storage demonstration using Windows TLS
 */

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

// Global TLS index - each thread will have its own value at this index
DWORD tls_index = TLS_OUT_OF_INDEXES;

// Structure for thread-specific data
typedef struct {
    int thread_id;
    char* thread_name;
    int counter;
} thread_data_t;

// Function to clean up thread-specific data
void cleanup_thread_data(void* data) {
    thread_data_t* tdata = (thread_data_t*)data;
    if (tdata) {
        printf("Cleanup: Freeing thread-specific data for thread %d (%s)\n", 
               tdata->thread_id, tdata->thread_name);
        
        // Free the thread name string
        if (tdata->thread_name) {
            free(tdata->thread_name);
        }
        
        // Free the structure itself
        free(tdata);
    }
}

// Thread function that uses thread-specific data
DWORD WINAPI tls_thread_function(LPVOID arg) {
    int thread_num = *((int*)arg);
    
    // Allocate a thread-specific data structure
    thread_data_t* tdata = (thread_data_t*)malloc(sizeof(thread_data_t));
    if (!tdata) {
        printf("Thread %d: Failed to allocate thread-specific data\n", thread_num);
        return 1;
    }
    
    // Initialize the thread data
    tdata->thread_id = thread_num;
    
    // Allocate and set the thread name
    char name_buffer[32];
    sprintf(name_buffer, "Worker Thread %d", thread_num);
    tdata->thread_name = _strdup(name_buffer);
    tdata->counter = 0;
    
    // Store the pointer in TLS
    if (!TlsSetValue(tls_index, tdata)) {
        printf("Thread %d: TlsSetValue failed with error %d\n", thread_num, GetLastError());
        cleanup_thread_data(tdata);
        return 1;
    }
    
    printf("Thread %d: Stored thread-specific data at TLS index %u\n", thread_num, tls_index);
    
    // Simulate some work and access thread-specific data
    for (int i = 0; i < 3; i++) {
        // Get the thread-specific data
        thread_data_t* my_data = (thread_data_t*)TlsGetValue(tls_index);
        if (!my_data) {
            printf("Thread %d: TlsGetValue failed with error %d\n", thread_num, GetLastError());
            break;
        }
        
        // Update the counter
        my_data->counter++;
        
        // Use the thread-specific data
        printf("Thread %d (%s): Counter = %d\n", 
               my_data->thread_id, my_data->thread_name, my_data->counter);
        
        // Sleep to simulate work
        Sleep(500);
    }
    
    // Get the thread-specific data one last time
    thread_data_t* final_data = (thread_data_t*)TlsGetValue(tls_index);
    if (final_data) {
        printf("Thread %d (%s): Final counter = %d\n", 
               final_data->thread_id, final_data->thread_name, final_data->counter);
        
        // Clean up - in a real application, this would be done in a DLL detach or thread exit callback
        cleanup_thread_data(final_data);
        TlsSetValue(tls_index, NULL);
    }
    
    return 0;
}

// Demo showing TLS (Thread Local Storage) usage
void thread_local_storage_demo() {
    HANDLE threads[3];
    int thread_ids[3] = {1, 2, 3};
    
    printf("\n=== Thread Local Storage (TLS) Demo ===\n");
    
    // Allocate a TLS index
    tls_index = TlsAlloc();
    if (tls_index == TLS_OUT_OF_INDEXES) {
        fprintf(stderr, "Error: TlsAlloc failed with code %lu\n", GetLastError());
        return;
    }
    
    printf("Allocated TLS index: %lu\n", tls_index);
    
    // Create multiple threads, each with its own thread-specific data
    for (int i = 0; i < 3; i++) {
        threads[i] = CreateThread(
            NULL,                // Default security attributes
            0,                   // Default stack size
            tls_thread_function, // Thread function
            &thread_ids[i],      // Argument to thread function
            0,                   // Default creation flags
            NULL                 // Don't store thread ID
        );
        
        if (threads[i] == NULL) {
            fprintf(stderr, "Error creating thread %d\n", i + 1);
            // Close already created threads
            for (int j = 0; j < i; j++) {
                CloseHandle(threads[j]);
            }
            TlsFree(tls_index);
            return;
        }
    }
    
    // Wait for all threads to finish
    WaitForMultipleObjects(3, threads, TRUE, INFINITE);
    
    // Close all thread handles
    for (int i = 0; i < 3; i++) {
        CloseHandle(threads[i]);
    }
    
    // Free the TLS index
    if (!TlsFree(tls_index)) {
        fprintf(stderr, "Error: TlsFree failed with code %lu\n", GetLastError());
    } else {
        printf("Freed TLS index: %lu\n", tls_index);
    }
    
    printf("Thread local storage demo completed\n");
}

// Main function to run the demos
int thread_specific_data_main() {
    printf("=== Thread-Specific Data Demo ===\n");
    
    // Run the thread local storage demo
    thread_local_storage_demo();
    
    printf("Thread-specific data demo completed\n");
    return 0;
} 