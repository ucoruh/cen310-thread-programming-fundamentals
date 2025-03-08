@echo off
echo Python Threading Project - Complete Workflow

echo.
echo Step 1: Cleaning the project...
call clean.bat
if %ERRORLEVEL% NEQ 0 (
    echo Process failed at the cleaning step!
    exit /b %ERRORLEVEL%
)

echo.
echo Step 2: Setting up the environment...
call setup.bat
if %ERRORLEVEL% NEQ 0 (
    echo Process failed at the setup step!
    exit /b %ERRORLEVEL%
)

echo.
echo Step 3: Installing the project...
call install.bat
if %ERRORLEVEL% NEQ 0 (
    echo Process failed at the installation step!
    exit /b %ERRORLEVEL%
)

echo.
echo Step 4: Running tests...
call test.bat
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Some tests failed! Continuing anyway...
)

echo.
echo Step 5: Running the application...
call run.bat
if %ERRORLEVEL% NEQ 0 (
    echo Process failed at the running step!
    exit /b %ERRORLEVEL%
)

echo.
echo All steps completed! 