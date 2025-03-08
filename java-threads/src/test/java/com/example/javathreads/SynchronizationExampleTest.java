package com.example.javathreads;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Test class for SynchronizationExample
 */
public class SynchronizationExampleTest {
    
    @Test
    public void testSynchronizedIncrement() throws InterruptedException {
        SynchronizationExample example = new SynchronizationExample();
        example.resetCounter();
        
        // Create two threads that increment the counter with synchronization
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                example.incrementSynchronized();
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                example.incrementSynchronized();
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
        
        // The counter should be exactly 2000 since we used synchronized methods
        assertEquals(2000, example.getCounter(), 
                "Counter should be exactly 2000 when using synchronized methods");
    }
    
    @Test
    public void testIncrementWithLock() throws InterruptedException {
        SynchronizationExample example = new SynchronizationExample();
        example.resetCounter();
        
        // Create two threads that increment the counter with lock
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                example.incrementWithLock();
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                example.incrementWithLock();
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
        
        // The counter should be exactly 2000 since we used synchronized blocks
        assertEquals(2000, example.getCounter(), 
                "Counter should be exactly 2000 when using synchronized blocks");
    }
} 