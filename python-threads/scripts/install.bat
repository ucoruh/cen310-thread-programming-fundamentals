@echo off
echo Installing Python Threading Project in development mode...

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
echo Installing project in development mode...
pip install -e .

echo.
echo Installation completed successfully!
echo The project is now installed in development mode. 