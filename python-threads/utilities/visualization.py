"""
Visualization utilities for plotting benchmark results.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union


def plot_execution_times(
    data: Dict[str, List[float]],
    title: str = "Execution Time Comparison",
    xlabel: str = "Method",
    ylabel: str = "Time (seconds)",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> None:
    """
    Plot execution times for different methods.
    
    Args:
        data: Dictionary mapping method names to lists of execution times.
        title: Title for the plot.
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
        figsize: Figure size as (width, height) in inches.
        save_path: If provided, save the figure to this path.
    """
    plt.figure(figsize=figsize)
    
    methods = list(data.keys())
    means = [np.mean(times) for times in data.values()]
    stds = [np.std(times) for times in data.values()]
    
    # Create bar plot
    bars = plt.bar(methods, means, yerr=stds, capsize=10, alpha=0.7)
    
    # Add values on top of bars
    for bar, mean in zip(bars, means):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            mean + (0.1 * max(means)),
            f"{mean:.4f}s",
            ha='center',
            va='bottom',
            fontweight='bold'
        )
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_speedup(
    baseline: str,
    data: Dict[str, float],
    title: str = "Speedup Relative to Baseline",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> None:
    """
    Plot speedup of different methods relative to a baseline.
    
    Args:
        baseline: Name of the baseline method.
        data: Dictionary mapping method names to execution times.
        title: Title for the plot.
        figsize: Figure size as (width, height) in inches.
        save_path: If provided, save the figure to this path.
    """
    plt.figure(figsize=figsize)
    
    if baseline not in data:
        raise ValueError(f"Baseline '{baseline}' not found in data")
    
    baseline_time = data[baseline]
    methods = [m for m in data.keys() if m != baseline]
    speedups = [baseline_time / data[m] for m in methods]
    
    # Create bar plot
    bars = plt.bar(methods, speedups, alpha=0.7)
    
    # Add a horizontal line at y=1 (baseline)
    plt.axhline(y=1, color='r', linestyle='--', alpha=0.7, label=f"Baseline ({baseline})")
    
    # Add values on top of bars
    for bar, speedup in zip(bars, speedups):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            speedup + 0.1,
            f"{speedup:.2f}x",
            ha='center',
            va='bottom',
            fontweight='bold'
        )
    
    plt.title(title)
    plt.xlabel("Method")
    plt.ylabel("Speedup Factor (higher is better)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_scaling(
    data: Dict[int, Dict[str, float]],
    title: str = "Scaling Performance",
    xlabel: str = "Number of Workers",
    ylabel: str = "Time (seconds)",
    methods: Optional[List[str]] = None,
    figsize: Tuple[int, int] = (10, 6),
    log_scale: bool = False,
    save_path: Optional[str] = None
) -> None:
    """
    Plot scaling performance as the number of workers increases.
    
    Args:
        data: Dictionary mapping worker counts to dictionaries of method execution times.
        title: Title for the plot.
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
        methods: List of methods to include in the plot. If None, include all methods.
        figsize: Figure size as (width, height) in inches.
        log_scale: Whether to use a logarithmic scale for the y-axis.
        save_path: If provided, save the figure to this path.
    """
    plt.figure(figsize=figsize)
    
    worker_counts = sorted(data.keys())
    
    # If methods not specified, get all unique methods across all worker counts
    if methods is None:
        methods = set()
        for worker_data in data.values():
            methods.update(worker_data.keys())
        methods = sorted(methods)
    
    # Plot each method
    for method in methods:
        times = [data[workers].get(method, float('nan')) for workers in worker_counts]
        plt.plot(worker_counts, times, marker='o', label=method)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    if log_scale:
        plt.yscale('log')
    
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_resource_usage(
    cpu_usage: List[float],
    memory_usage: List[float],
    timestamps: List[float],
    title: str = "Resource Usage Over Time",
    figsize: Tuple[int, int] = (12, 8),
    save_path: Optional[str] = None
) -> None:
    """
    Plot CPU and memory usage over time.
    
    Args:
        cpu_usage: List of CPU usage percentages.
        memory_usage: List of memory usage values (MB).
        timestamps: List of timestamps (seconds from start).
        title: Title for the plot.
        figsize: Figure size as (width, height) in inches.
        save_path: If provided, save the figure to this path.
    """
    plt.figure(figsize=figsize)
    
    # Create two subplots sharing the same x-axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    # Plot CPU usage
    ax1.plot(timestamps, cpu_usage, 'b-', label='CPU Usage')
    ax1.set_ylabel('CPU Usage (%)')
    ax1.set_ylim(0, max(cpu_usage) * 1.1)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot memory usage
    ax2.plot(timestamps, memory_usage, 'g-', label='Memory Usage')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Memory Usage (MB)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.suptitle(title)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show() 