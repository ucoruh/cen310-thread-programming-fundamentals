@echo off
rem clean.bat - Script for cleaning .NET project

rem Set UTF-8 character encoding
chcp 65001 >nul

echo ===================================
echo C# Threads Project - Clean Operation
echo ===================================

rem Go to the project root directory
cd /d %~dp0

echo Removing bin and obj folders...

rem Find and delete bin and obj folders
for /d /r . %%d in (bin,obj) do (
    if exist "%%d" (
        echo Deleting: "%%d"
        rd /s /q "%%d"
    )
)

echo.
echo Running dotnet clean command...
dotnet clean .\src\CSharpThreads.sln

echo.
echo Cleaning completed!
