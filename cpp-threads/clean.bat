@echo off
setlocal enabledelayedexpansion

echo ===== Cleaning C++ Threads Project =====

rem Remove the build directory
if exist build (
    echo Removing build directory...
    rmdir /s /q build
) else (
    echo Build directory doesn't exist. Nothing to clean.
)

echo.
echo Clean completed successfully!

endlocal 