@echo off
echo Running Java Threading Fundamentals examples...

rem Navigate to the project root directory
cd ..

rem Check if JAR file exists
if not exist target\java-threads-1.0-SNAPSHOT.jar (
    echo Error: JAR file not found. Please build the project first using build.bat
    exit /b 1
)

rem Run the JAR file
echo.
echo Starting application...
echo.
java -jar target\java-threads-1.0-SNAPSHOT.jar

if %ERRORLEVEL% NEQ 0 (
    echo Application execution failed!
    exit /b %ERRORLEVEL%
)

echo.
echo Application completed successfully! 