@echo off
title MedCare Clinic Web System (MySQL Server)
echo ========================================================
echo   MedCare Clinic and Hospital Management System
echo   DBMS Project - Powered by MySQL and Python Flask
echo ========================================================
echo.

echo [1/2] Checking & Initializing MySQL Database (clinic_db)...
python setup_db.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to connect to MySQL. Please ensure MySQL80 service is running.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Launching Web Application...
echo Open your browser at: http://127.0.0.1:5000
echo.
python app.py

pause
