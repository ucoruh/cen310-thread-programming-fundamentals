@echo off
rem build.bat - Script for building .NET project

rem Set UTF-8 character encoding
chcp 65001 >nul

rem Parameters
set Configuration=Debug
set Verbosity=minimal

rem Set configuration if first parameter is provided
if not "%~1"=="" set Configuration=%~1
rem Set verbosity if second parameter is provided
if not "%~2"=="" set Verbosity=%~2

echo ===================================
echo C# Threads Project - Build Operation
echo ===================================
echo Configuration: %Configuration%
echo Verbosity: %Verbosity%
echo.

rem Go to the project root directory
cd /d %~dp0

echo Running dotnet build command...
dotnet build .\src\CSharpThreads.sln --configuration %Configuration% --verbosity %Verbosity%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build completed successfully!
) else (
    echo.
    echo Build failed. Error code: %ERRORLEVEL%
)
