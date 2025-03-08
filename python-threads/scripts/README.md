# Python Threading Examples - Script Guide

This folder contains helpful scripts to simplify working with the Python Threading examples project.

## Available Scripts

- **clean.bat**: Removes temporary files and virtual environment
- **setup.bat**: Creates a virtual environment and installs dependencies
- **install.bat**: Installs the project in development mode
- **run.bat**: Runs the threading examples application
- **test.bat**: Runs all tests for the project
- **all.bat**: Executes all steps in sequence (clean, setup, install, test, run)

## Quick Guide

### For First Time Setup:

```
cd python-threads/scripts
setup.bat
install.bat
```

### For Regular Use:

```
cd python-threads/scripts
run.bat
```

### For Complete Reset and Run:

```
cd python-threads/scripts
all.bat
```

### For Development Workflow:

```
cd python-threads/scripts
clean.bat   # When you want to start fresh
setup.bat   # If virtual environment doesn't exist
install.bat # After you've made changes to the code
test.bat    # To verify your changes work correctly
run.bat     # To run the application
```

## Notes

- These scripts should be run from the `scripts` directory
- All scripts provide verbal feedback on what they're doing
- If you encounter any issues, try running `clean.bat` followed by `setup.bat` 