package com.example.javathreads;

/**
 * Main class demonstrating basic Java threading concepts
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("Java Threading Fundamentals");
        System.out.println("==========================");
        
        // Example 1: Creating threads using Thread class
        System.out.println("\nExample 1: Creating threads using Thread class");
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Thread 1: " + i);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Thread 2: " + i);
                try {
                    Thread.sleep(150);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        
        thread1.start();
        thread2.start();
        
        try {
            // Wait for both threads to complete
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Example 2: Creating threads using Runnable interface
        System.out.println("\nExample 2: Creating threads using Runnable interface");
        RunnableExample runnable1 = new RunnableExample("Runnable-1", 5);
        RunnableExample runnable2 = new RunnableExample("Runnable-2", 5);
        
        Thread thread3 = new Thread(runnable1);
        Thread thread4 = new Thread(runnable2);
        
        thread3.start();
        thread4.start();
        
        try {
            thread3.join();
            thread4.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Run synchronization examples
        SynchronizationExample.runDemo();
        
        // Run executor framework examples
        ExecutorExample.runDemo();
        
        System.out.println("\nAll examples have completed execution.");
    }
} 