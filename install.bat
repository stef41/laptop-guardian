@echo off
REM Laptop Guardian — Windows installer
REM Usage: Right-click → Run as Administrator, or open CMD and run: install.bat
setlocal

echo.
echo === Installing Laptop Guardian ===
echo.

REM ── 1. Check Python ──────────────────────────────────────────
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Downloading Python installer...
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    start https://www.python.org/downloads/
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo    %%i

REM ── 2. Create virtual environment ────────────────────────────
set INSTALL_DIR=%USERPROFILE%\.laptop-guardian

if exist "%INSTALL_DIR%" (
    echo Removing previous installation...
    rmdir /s /q "%INSTALL_DIR%"
)

echo Creating environment in %INSTALL_DIR%...
python -m venv "%INSTALL_DIR%\venv"
call "%INSTALL_DIR%\venv\Scripts\activate.bat"

REM ── 3. Install the package ──────────────────────────────────
echo Installing laptop-guardian...
pip install --upgrade pip -q
pip install git+https://github.com/stef41/laptop-guardian.git -q

echo    Installed successfully.

REM ── 4. Create launcher batch file ───────────────────────────
(
echo @echo off
echo call "%INSTALL_DIR%\venv\Scripts\activate.bat"
echo start /b pythonw -m laptop_guardian.app
) > "%INSTALL_DIR%\laptop-guardian.bat"

REM ── 5. Create Start Menu shortcut ──────────────────────────
set SHORTCUT_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs
powershell -command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_DIR%\Laptop Guardian.lnk'); $s.TargetPath = '%INSTALL_DIR%\laptop-guardian.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'Anti-theft laptop protection'; $s.WindowStyle = 7; $s.Save()"

REM ── 6. Create Desktop shortcut ────────────────────────────
powershell -command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%USERPROFILE%\Desktop\Laptop Guardian.lnk'); $s.TargetPath = '%INSTALL_DIR%\laptop-guardian.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'Anti-theft laptop protection'; $s.WindowStyle = 7; $s.Save()"

echo.
echo === Laptop Guardian installed! ===
echo.
echo    How to launch:
echo    - Double-click "Laptop Guardian" on your Desktop
echo    - Or find it in the Start Menu
echo    - Or run: %INSTALL_DIR%\laptop-guardian.bat
echo.
echo    A shield icon will appear in your system tray.
echo    Right-click it to configure and arm.
echo.
pause
