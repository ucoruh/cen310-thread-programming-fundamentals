#!/bin/bash
# Script to set up a virtual environment for the Python threading project

# Exit on error
set -e

# Create a virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "Installing package in development mode..."
pip install -e .

echo "Setup complete! You can now run the examples with 'python main.py'"
echo "To activate the virtual environment in the future, run 'source venv/bin/activate'" 