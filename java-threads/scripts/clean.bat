@echo off
echo Cleaning Java Threading Fundamentals project...

rem Navigate to the project root directory
cd ..

rem Run Maven clean command
call mvn clean

if %ERRORLEVEL% NEQ 0 (
    echo Clean failed!
    exit /b %ERRORLEVEL%
)

echo.
echo Project cleaned successfully!
echo. 