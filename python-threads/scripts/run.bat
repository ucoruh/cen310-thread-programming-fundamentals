@echo off
echo Running Python Threading Examples...

cd ..

if not exist venv (
    echo Virtual environment not found!
    echo Please run setup.bat first to create the virtual environment.
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting the application...
python main.py

echo.
echo Application finished. 