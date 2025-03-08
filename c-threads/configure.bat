@echo off
setlocal enabledelayedexpansion

echo ===== Configuring C Threads Project =====

REM Check for CMake
where cmake >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: CMake is not found in PATH.
    echo Please install CMake and add it to your PATH.
    exit /b 1
)

REM Create the build directory if it doesn't exist
if not exist build (
    echo Creating build directory...
    mkdir build
)

REM Navigate to the build directory
cd build

REM Configure the project with CMake
echo Configuring project with CMake...
cmake .. -A x64

if %ERRORLEVEL% neq 0 (
    echo Error: CMake configuration failed!
    exit /b 1
)

echo.
echo Configuration successful!
echo To build the project, run build.bat
echo.

exit /b 0

endlocal 