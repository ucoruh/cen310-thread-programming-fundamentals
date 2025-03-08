package com.example.javathreads;

/**
 * Example class implementing the Runnable interface
 */
public class RunnableExample implements Runnable {
    private final String name;
    private final int iterations;
    
    /**
     * Constructor for RunnableExample
     * 
     * @param name The name of this runnable instance
     * @param iterations The number of iterations to run
     */
    public RunnableExample(String name, int iterations) {
        this.name = name;
        this.iterations = iterations;
    }
    
    @Override
    public void run() {
        for (int i = 0; i < iterations; i++) {
            System.out.println(name + ": " + i);
            try {
                // Random sleep between 100-200ms
                Thread.sleep((long) (100 + Math.random() * 100));
            } catch (InterruptedException e) {
                System.out.println(name + " was interrupted.");
                return;
            }
        }
        System.out.println(name + " has completed.");
    }
} 