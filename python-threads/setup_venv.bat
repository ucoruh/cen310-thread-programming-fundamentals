@echo off
REM Script to set up a virtual environment for the Python threading project on Windows

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Installing package in development mode...
pip install -e .

echo Setup complete! You can now run the examples with "python main.py"
echo To activate the virtual environment in the future, run "venv\Scripts\activate.bat"

pause 