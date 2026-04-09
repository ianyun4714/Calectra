@REM Calectra Dashboard - Windows Batch Setup Script
@REM This script automates the complete setup process

@echo off
setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo               CALECTRA CEO DASHBOARD - SETUP WIZARD
echo ================================================================================
echo.

REM Check if Node.js is installed
echo Checking for Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ✗ Node.js is not installed!
    echo Please download and install from: https://nodejs.org/ (LTS version)
    echo Once installed, run this script again.
    pause
    exit /b 1
)

echo ✓ Node.js found: 
node --version

echo.
echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ✗ Python is not installed!
    echo Please install Python 3.7+ from: https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python found:
python --version

echo.
echo ================================================================================
echo Step 1: Installing Node.js dependencies
echo ================================================================================
echo.

cd dashboard
echo Installing npm packages (this may take 1-2 minutes)...
call npm install

if errorlevel 1 (
    echo.
    echo ✗ Failed to install npm packages
    pause
    exit /b 1
)

echo ✓ npm packages installed successfully

echo.
echo ================================================================================
echo Step 2: Verifying data files
echo ================================================================================
echo.

cd ..
if exist "dashboard\public\data\dashboard_data.json" (
    echo ✓ Dashboard data found: dashboard\public\data\dashboard_data.json
) else (
    echo ✓ Data not found, generating now...
    python process_data.py
    if errorlevel 1 (
        echo.
        echo ✗ Failed to process data
        pause
        exit /b 1
    )
)

echo.
echo ================================================================================
echo                          SETUP COMPLETE! ✓
echo ================================================================================
echo.
echo Your Calectra CEO Dashboard is ready to run!
echo.
echo To start the dashboard:
echo   1. Navigate to: cd dashboard
echo   2. Run: npm run dev
echo   3. Your browser will open at http://localhost:3000
echo.
echo The dashboard includes:
echo   - Flood View chart (RE generation vs battery capacity)
echo   - Interactive LMP analysis with duck curve patterns
echo   - Professional dark mode design
echo   - Dynamic headlines and metrics
echo.
echo For detailed information, see QUICK_START.md
echo.
echo ================================================================================

pause
