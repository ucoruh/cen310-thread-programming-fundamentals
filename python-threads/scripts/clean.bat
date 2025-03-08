@echo off
echo Cleaning Python Threading Project...

echo.
echo Removing virtual environment...
if exist ..\venv (
    rmdir /s /q ..\venv
    echo Virtual environment removed.
) else (
    echo No virtual environment found.
)

echo.
echo Removing Python cache files...
cd ..
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
for /r . %%f in (*.pyc) do @del "%%f"

echo.
echo Removing distribution files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.egg-info rmdir /s /q *.egg-info

echo.
echo Cleaning completed successfully! 