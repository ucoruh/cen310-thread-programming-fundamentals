@echo off
echo Running tests for Java Threading Fundamentals project...

rem Navigate to the project root directory
cd ..

rem Run Maven test command
call mvn test

if %ERRORLEVEL% NEQ 0 (
    echo Tests failed!
    exit /b %ERRORLEVEL%
)

echo.
echo All tests passed successfully!
echo. 