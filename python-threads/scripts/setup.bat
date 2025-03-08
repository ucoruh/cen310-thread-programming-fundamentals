@echo off
echo Setting up Python Threading Project...

cd ..

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup completed successfully!
echo.
echo To activate the virtual environment in the future, run:
echo   call venv\Scripts\activate.bat
echo To run the examples:
echo   python main.py
echo.
echo Or you can simply use the 'run.bat' script. 