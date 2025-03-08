@echo off
setlocal enabledelayedexpansion

echo ===== Running C++ Threads Project =====

rem Check if the executable exists
if not exist build\bin\Release\CppThreads.exe (
    echo Executable not found in build\bin\Release directory.
    echo Please run build.bat first.
    exit /b 1
)

rem Run the executable with any provided arguments
echo Running executable...
build\bin\Release\CppThreads.exe %*

rem Check if execution was successful
if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Running demos failed
    exit /b 1
)

echo.
echo Execution completed successfully

endlocal 