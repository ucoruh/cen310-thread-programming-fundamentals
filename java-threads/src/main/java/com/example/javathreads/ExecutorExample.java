package com.example.javathreads;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Example demonstrating the Executor framework and thread pools
 */
public class ExecutorExample {
    
    /**
     * Demonstrate a fixed thread pool
     */
    public static void demonstrateFixedThreadPool() {
        System.out.println("\nFixed Thread Pool Example");
        System.out.println("========================");
        
        // Create a fixed thread pool with 3 threads
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Submit 5 tasks to the executor
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                String threadName = Thread.currentThread().getName();
                System.out.println("Task " + taskId + " is running on " + threadName);
                
                // Simulate work
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                
                System.out.println("Task " + taskId + " completed");
                return taskId;
            });
        }
        
        // Shutdown the executor
        executor.shutdown();
        try {
            // Wait for all tasks to complete or timeout after 10 seconds
            if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
        
        System.out.println("All tasks submitted to the fixed thread pool have completed");
    }
    
    /**
     * Demonstrate a scheduled thread pool
     */
    public static void demonstrateScheduledThreadPool() {
        System.out.println("\nScheduled Thread Pool Example");
        System.out.println("============================");
        
        // Create a scheduled thread pool with 2 threads
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
        
        // Schedule a task to run after a 2-second delay
        System.out.println("Scheduling a delayed task...");
        scheduler.schedule(() -> {
            System.out.println("Delayed task executed after 2 seconds");
            return "Delayed Result";
        }, 2, TimeUnit.SECONDS);
        
        // Schedule a task to run periodically every 1 second, starting after 0 seconds
        final AtomicInteger counter = new AtomicInteger(0);
        System.out.println("Scheduling a periodic task...");
        ScheduledFuture<?> periodicTask = scheduler.scheduleAtFixedRate(() -> {
            int count = counter.incrementAndGet();
            System.out.println("Periodic task executed: " + count);
            
            // Run only 3 times
            if (count >= 3) {
                throw new RuntimeException("Stopping periodic task");
            }
        }, 0, 1, TimeUnit.SECONDS);
        
        // Wait for the periodic task to complete (after 3 executions)
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Cancel the periodic task if it's still running
        periodicTask.cancel(false);
        
        // Shutdown the scheduler
        scheduler.shutdown();
        try {
            if (!scheduler.awaitTermination(5, TimeUnit.SECONDS)) {
                scheduler.shutdownNow();
            }
        } catch (InterruptedException e) {
            scheduler.shutdownNow();
        }
        
        System.out.println("Scheduled thread pool has been shut down");
    }
    
    /**
     * Demonstrate CompletableFuture for asynchronous programming
     */
    public static void demonstrateCompletableFuture() {
        System.out.println("\nCompletableFuture Example");
        System.out.println("=========================");
        
        // Create a CompletableFuture that completes after a delay
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> {
            try {
                System.out.println("Future 1 running in thread: " + Thread.currentThread().getName());
                Thread.sleep(1000);
                return "Result from Future 1";
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });
        
        // Create another CompletableFuture
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> {
            try {
                System.out.println("Future 2 running in thread: " + Thread.currentThread().getName());
                Thread.sleep(2000);
                return "Result from Future 2";
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });
        
        // Combine the results of both futures
        CompletableFuture<String> combinedFuture = future1.thenCombine(future2, (result1, result2) -> {
            System.out.println("Combining results in thread: " + Thread.currentThread().getName());
            return result1 + " + " + result2;
        });
        
        // Add a callback to be executed when the combined future completes
        combinedFuture.thenAccept(result -> {
            System.out.println("Combined result: " + result);
        });
        
        // Wait for the combined future to complete
        try {
            combinedFuture.get(5, TimeUnit.SECONDS);
        } catch (InterruptedException | ExecutionException | TimeoutException e) {
            e.printStackTrace();
        }
        
        System.out.println("CompletableFuture demonstration completed");
    }
    
    /**
     * Run the executor framework demonstration
     */
    public static void runDemo() {
        System.out.println("\nExecutor Framework Examples");
        System.out.println("==========================");
        
        demonstrateFixedThreadPool();
        demonstrateScheduledThreadPool();
        demonstrateCompletableFuture();
    }
} 