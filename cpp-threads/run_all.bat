@echo off
setlocal enabledelayedexpansion

echo ===== C++ Threads Project - Run All Steps =====

rem Step 1: Clean
call clean.bat
if %ERRORLEVEL% neq 0 (
    echo Step 1 failed: Clean
    exit /b 1
)

echo.
echo Step 2: Configure
call configure.bat
if %ERRORLEVEL% neq 0 (
    echo Step 2 failed: Configure
    exit /b 1
)

echo.
echo Step 3: Build
call build.bat
if %ERRORLEVEL% neq 0 (
    echo Step 3 failed: Build
    exit /b 1
)

echo.
echo Step 4: Run All Demos
call run.bat --run-all
if %ERRORLEVEL% neq 0 (
    echo Step 4 failed: Run
    exit /b 1
)

echo.
echo All steps completed successfully

endlocal 