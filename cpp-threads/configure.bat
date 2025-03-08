@echo off
setlocal enabledelayedexpansion

echo ===== Configuring C++ Threads Project =====

rem Create build directory if it doesn't exist
if not exist build (
    echo Creating build directory...
    mkdir build
) else (
    echo Build directory already exists.
)

rem Change to the build directory
cd build

rem Configure the project with CMake
echo Configuring project with CMake...
cmake .. -A x64

rem Check if CMake configuration was successful
if %ERRORLEVEL% neq 0 (
    echo.
    echo Configuration failed!
    echo Please check the error messages above and try again.
    exit /b 1
)

echo.
echo Configuration successful
echo To build the project, run build.bat

endlocal 