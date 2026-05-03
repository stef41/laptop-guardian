@echo off
REM Uninstall Laptop Guardian on Windows
echo Uninstalling Laptop Guardian...
rmdir /s /q "%USERPROFILE%\.laptop-guardian" 2>nul
rmdir /s /q "%USERPROFILE%\.config\laptop-guardian" 2>nul
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Laptop Guardian.lnk" 2>nul
del "%USERPROFILE%\Desktop\Laptop Guardian.lnk" 2>nul
echo Done. Laptop Guardian has been removed.
pause
