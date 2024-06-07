@echo off

REM Check if Python is already installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    REM If Python is not installed, download and install Python
    echo Installing Python...
    if "%PROCESSOR_ARCHITECTURE%" == "AMD64" (
        REM For 64-bit Windows
        curl -O https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
        python-3.9.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        del python-3.9.7-amd64.exe
    ) else (
        REM For 32-bit Windows
        curl -O https://www.python.org/ftp/python/3.9.7/python-3.9.7.exe
        python-3.9.7.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        del python-3.9.7.exe
    )
) else (
    echo Python is already installed.
)

REM Install Pygame
echo Installing Pygame...
pip install pygame

echo Installation completed.