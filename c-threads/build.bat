@echo off
setlocal enabledelayedexpansion

echo ===== Building C Threads Project =====

REM Check if the build directory exists
if not exist build (
    echo Error: Build directory not found!
    echo Please run configure.bat first.
    exit /b 1
)

REM Navigate to the build directory
cd build

REM Build the project with CMake
echo Building project...
cmake --build . --config Release

if %ERRORLEVEL% neq 0 (
    echo Error: Build failed!
    exit /b 1
)

echo.
echo Build successful!
echo Executable can be found in build\bin\Release directory.
echo.

exit /b 0

endlocal 