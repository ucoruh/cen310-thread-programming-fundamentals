package com.example.javathreads;

/**
 * Example demonstrating thread synchronization concepts
 */
public class SynchronizationExample {
    
    private int counter = 0;
    private final Object lock = new Object(); // Lock object for synchronization
    
    /**
     * Increment the counter in a thread-safe manner using synchronized method
     */
    public synchronized void incrementSynchronized() {
        counter++;
    }
    
    /**
     * Increment the counter in a thread-safe manner using synchronized block
     */
    public void incrementWithLock() {
        synchronized (lock) {
            counter++;
        }
    }
    
    /**
     * Get the current counter value
     * 
     * @return The current counter value
     */
    public int getCounter() {
        return counter;
    }
    
    /**
     * Reset the counter to zero
     */
    public synchronized void resetCounter() {
        counter = 0;
    }
    
    /**
     * Demonstrate race condition without synchronization
     */
    public void demonstrateRaceCondition() {
        resetCounter();
        
        // Create two threads that increment the counter without synchronization
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                counter++; // This operation is not atomic!
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                counter++; // This operation is not atomic!
            }
        });
        
        thread1.start();
        thread2.start();
        
        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Without synchronization, counter = " + counter);
        System.out.println("Expected value: 20000");
    }
    
    /**
     * Demonstrate proper synchronization
     */
    public void demonstrateSynchronization() {
        resetCounter();
        
        // Create two threads that increment the counter with synchronization
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                incrementSynchronized();
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 10000; i++) {
                incrementSynchronized();
            }
        });
        
        thread1.start();
        thread2.start();
        
        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("With synchronization, counter = " + counter);
        System.out.println("Expected value: 20000");
    }
    
    /**
     * Run the synchronization demonstration
     */
    public static void runDemo() {
        SynchronizationExample example = new SynchronizationExample();
        
        System.out.println("\nSynchronization Example");
        System.out.println("======================");
        
        example.demonstrateRaceCondition();
        example.demonstrateSynchronization();
    }
} 