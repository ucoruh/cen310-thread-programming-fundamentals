@echo off
setlocal enabledelayedexpansion

echo ===== Running C Threads Project =====

REM Define path to executable
set EXECUTABLE=build\bin\Release\CThreads.exe

REM Check if the executable exists
if not exist %EXECUTABLE% (
    echo Error: Executable not found at %EXECUTABLE%
    echo Please make sure to run configure.bat and build.bat first.
    exit /b 1
)

REM Run the program with the specified arguments or default
if "%1"=="" (
    echo Running program in interactive mode...
    %EXECUTABLE%
) else if "%1"=="--run-all" (
    echo Running all demos in sequence...
    %EXECUTABLE% --run-all
) else (
    echo Running with specified arguments: %*
    %EXECUTABLE% %*
)

exit /b %ERRORLEVEL% 