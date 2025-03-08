@echo off
setlocal enabledelayedexpansion

echo ===== C Threads Project - Run All Steps =====

echo.
echo Step 1: Clean
call clean.bat
if %ERRORLEVEL% neq 0 (
    echo Error: Clean step failed!
    exit /b 1
)

echo.
echo Step 2: Configure
call configure.bat
if %ERRORLEVEL% neq 0 (
    echo Error: Configure step failed!
    exit /b 1
)

echo.
echo Step 3: Build
call build.bat
if %ERRORLEVEL% neq 0 (
    echo Error: Build step failed!
    exit /b 1
)

echo.
echo Step 4: Run All Demos
call run.bat --run-all
if %ERRORLEVEL% neq 0 (
    echo Error: Running demos failed!
    exit /b 1
)

echo.
echo All steps completed successfully!
echo.

exit /b 0 