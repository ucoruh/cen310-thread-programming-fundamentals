"""
Main script to run all threading and concurrency examples.

This script provides a menu to run different examples from the project.
"""

import os
import sys
import importlib
from typing import Dict, Callable, Any, List


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str) -> None:
    """
    Print a header with the given title.
    
    Args:
        title: Header title.
    """
    print("\n" + "=" * 80)
    print(f"{title.center(80)}")
    print("=" * 80 + "\n")


def print_menu(options: Dict[str, str]) -> None:
    """
    Print a menu with the given options.
    
    Args:
        options: Dictionary mapping option keys to descriptions.
    """
    print("\nPlease select an option:")
    for key, description in options.items():
        print(f"  {key}) {description}")
    print("  q) Quit")


def run_module(module_path: str) -> None:
    """
    Import and run a module.
    
    Args:
        module_path: Dot-separated path to the module.
    """
    try:
        # Import the module
        module = importlib.import_module(module_path)
        
        # Look for a run_demo function
        if hasattr(module, 'run_demo'):
            module.run_demo()
        else:
            print(f"Module {module_path} does not have a run_demo function.")
    except ImportError as e:
        print(f"Error importing module {module_path}: {e}")
    except Exception as e:
        print(f"Error running module {module_path}: {e}")
    
    input("\nPress Enter to continue...")


def main() -> None:
    """Main function to run the examples."""
    # Define the available examples
    examples = {
        # Threading examples
        "1": {
            "name": "Basic Threading",
            "module": "threading_examples.basic_threads"
        },
        "2": {
            "name": "Thread Synchronization",
            "module": "threading_examples.synchronization"
        },
        "3": {
            "name": "Thread Communication",
            "module": "threading_examples.communication"
        },
        "4": {
            "name": "Producer-Consumer Pattern",
            "module": "threading_examples.producer_consumer"
        },
        
        # Multiprocessing examples
        "5": {
            "name": "Basic Multiprocessing",
            "module": "multiprocessing_examples.basic_processes"
        },
        "6": {
            "name": "Shared Memory",
            "module": "multiprocessing_examples.shared_memory"
        },
        "7": {
            "name": "Process Pools",
            "module": "multiprocessing_examples.process_pools"
        },
        
        # Asyncio examples
        "8": {
            "name": "Basic Asyncio",
            "module": "asyncio_examples.basic_asyncio"
        },
        "9": {
            "name": "Async I/O Operations",
            "module": "asyncio_examples.async_io_operations"
        },
        "10": {
            "name": "Async Web Requests",
            "module": "asyncio_examples.async_web_requests"
        },
        
        # Comparison examples
        "11": {
            "name": "I/O-Bound Task Comparison",
            "module": "comparison.io_bound_comparison"
        },
        "12": {
            "name": "CPU-Bound Task Comparison",
            "module": "comparison.cpu_bound_comparison"
        }
    }
    
    # Create a menu of options
    menu_options = {key: example["name"] for key, example in examples.items()}
    
    # Add special options
    menu_options["a"] = "Run all examples"
    
    # Main loop
    while True:
        clear_screen()
        print_header("Python Threading and Concurrency Examples")
        print_menu(menu_options)
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == 'q':
            print("\nExiting. Goodbye!")
            break
        elif choice == 'a':
            print("\nRunning all examples...")
            for key, example in examples.items():
                print_header(f"Running {example['name']}")
                run_module(example["module"])
        elif choice in examples:
            example = examples[choice]
            print_header(f"Running {example['name']}")
            run_module(example["module"])
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main() 