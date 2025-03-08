@echo off
setlocal enabledelayedexpansion

echo ===== Building C++ Threads Project =====

rem Check if the build directory exists
if not exist build (
    echo Build directory does not exist.
    echo Please run configure.bat first.
    exit /b 1
)

rem Change to the build directory
cd build

rem Build the project
echo Building project...
cmake --build . --config Release

rem Check if build was successful
if %ERRORLEVEL% neq 0 (
    echo.
    echo Build failed!
    echo Please check the error messages above and try again.
    exit /b 1
)

echo.
echo Build successful
echo Executable can be found in build\bin\Release directory.

endlocal 