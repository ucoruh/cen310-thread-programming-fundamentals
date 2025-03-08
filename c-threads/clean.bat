@echo off
setlocal

echo ===== Cleaning C Threads Project =====

REM Check if the build directory exists
if exist build (
    echo Removing build directory...
    rmdir /s /q build
)

REM Check if the bin directory exists
if exist bin (
    echo Removing bin directory...
    rmdir /s /q bin
)

echo.
echo Clean completed successfully!
echo.

exit /b 0

endlocal 