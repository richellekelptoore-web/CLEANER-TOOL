@echo off
:: Memory Clearer v2.0 - Launcher
:: 1) Starts the local web server (hosts index.html on :8765).
:: 2) Starts the always-on-top native toolbar (toolbar.py on :8766).
:: 3) Opens the web GUI in your default browser.
:: No dialogs, no prompts - everything is automated.

title Memory Clearer - Launcher
color 0A

cd /d "%~dp0"

echo.
echo Memory Clearer v2.0 - Starting...
echo.

if not exist ".official_marker" (
    > .official_marker echo OFFICIAL_INSTALLATION_VERIFIED
)

python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ERROR: Python is not installed.
    echo Download it from https://python.org and tick "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

python -c "import psutil" >nul 2>&1
if errorlevel 1 (
    python -m pip install psutil -q >nul 2>&1
)

if not exist "clear"        mkdir clear
if not exist "clear\logs"   mkdir clear\logs
if not exist "clear\cache"  mkdir clear\cache

if not exist "config.ini" (
    python setup_memory_clearer.py >nul 2>&1
)

:: --- Launch web server (background) and toolbar (foreground) ---------
:: Start the server in the background so it keeps running while the
:: toolbar owns the console. Closing the toolbar will not kill the
:: server (the server is daemonised via pythonw so it survives).
set MC_SILENT=1
start "" /B pythonw server.py

:: Give the server a moment to bind the port.
ping -n 2 127.0.0.1 >nul

:: Toolbar runs in the foreground - close it to exit the app.
python toolbar.py
if errorlevel 1 (
    color 0C
    echo.
    echo Toolbar failed to start. See "%~dp0clear\logs\memory_clearer.log"
    echo.
    pause
    exit /b 1
)

color 07
exit /b 0
