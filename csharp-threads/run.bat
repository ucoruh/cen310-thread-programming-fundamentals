@echo off
rem run.bat - Script for running .NET project

rem Set UTF-8 character encoding
chcp 65001 >nul

rem Parameters
set Configuration=Debug

rem Set configuration if first parameter is provided
if not "%~1"=="" set Configuration=%~1

echo ===================================
echo C# Threads Project - Run Operation
echo ===================================
echo Configuration: %Configuration%
echo.

rem Go to the project root directory
cd /d %~dp0

echo Running dotnet run command...
dotnet run --project .\src\CSharpThreads\CSharpThreads.csproj --configuration %Configuration%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Program completed successfully!
) else (
    echo.
    echo Program terminated with error. Error code: %ERRORLEVEL%
)
