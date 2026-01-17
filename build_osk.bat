@echo off
REM Build OSK Launcher EXE with images
setlocal enabledelayedexpansion

REM Force the script to run from its own directory
cd /d "%~dp0"

echo.
echo ========================================
echo OSK Launcher - EXE Builder
echo ========================================
echo.

REM Show current directory and files
echo Current directory: %CD%
echo.
echo Files in this directory:
dir /b
echo.

REM Check if osk_launcher.py exists
if not exist "osk_launcher.py" (
    echo ERROR: osk_launcher.py not found!
    pause
    exit /b 1
)

echo [OK] Found osk_launcher.py
echo.

REM Check for images
set HAS_KEYBOARD=0
set HAS_ICON=0

if exist "keyboard_image.png" (
    echo [OK] Found keyboard_image.png
    set HAS_KEYBOARD=1
) else (
    echo [WARNING] keyboard_image.png not found - will use text button
)

if exist "icon.png" (
    echo [OK] Found icon.png
    set HAS_ICON=1
) else (
    echo [WARNING] icon.png not found - will use default icon
)
echo.

echo [1/3] Checking for PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] PyInstaller not found. Installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo [OK] PyInstaller installed
) else (
    echo [OK] PyInstaller found
)

echo.
echo [2/3] Checking for Pillow...
pip show pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Pillow not found. Installing...
    pip install pillow
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Pillow
        pause
        exit /b 1
    )
    echo [OK] Pillow installed
) else (
    echo [OK] Pillow found
)

echo.
echo [3/3] Building EXE with bundled images...
echo This may take a minute...
echo.

REM Clean old builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

REM Build command based on what images are available
set BUILD_CMD=pyinstaller --onefile --windowed --name "OSK_Launcher" --clean

REM Add keyboard image if exists
if %HAS_KEYBOARD%==1 (
    set BUILD_CMD=!BUILD_CMD! --add-data "keyboard_image.png;."
)

REM Add icon for both window icon AND exe icon if exists
if %HAS_ICON%==1 (
    set BUILD_CMD=!BUILD_CMD! --add-data "icon.png;." --icon "icon.png"
)

REM Add the main script
set BUILD_CMD=!BUILD_CMD! osk_launcher.py

echo Running: !BUILD_CMD!
echo.

REM Execute the build
!BUILD_CMD!

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Your EXE is ready at:
echo   %CD%\dist\OSK_Launcher.exe
echo.
if exist "dist\OSK_Launcher.exe" (
    for %%A in (dist\OSK_Launcher.exe) do echo File size: %%~zA bytes
)
echo.
echo The EXE includes:
if %HAS_KEYBOARD%==1 echo   ✓ keyboard_image.png (bundled inside EXE)
if %HAS_ICON%==1 echo   ✓ icon.png (bundled inside EXE)
echo.
echo You can now:
echo - Run OSK_Launcher.exe from the dist folder
echo - Move it anywhere you want
echo - No other files needed - images are inside the EXE!
echo.
pause