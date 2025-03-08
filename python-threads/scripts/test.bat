@echo off
echo Running tests for Python Threading Project...

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
echo Running pytest...
pytest

echo.
if %ERRORLEVEL% EQU 0 (
    echo All tests passed successfully!
) else (
    echo Some tests failed! Please check the test output above.
) 