@echo off
echo Building Java Threading Fundamentals project...

rem Navigate to the project root directory
cd ..

rem Run Maven package command (skips tests for faster build)
call mvn package -DskipTests

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b %ERRORLEVEL%
)

echo.
echo Project built successfully!
echo.
echo The JAR file is available at: target\java-threads-1.0-SNAPSHOT.jar 