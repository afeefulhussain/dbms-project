Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  MedCare Clinic and Hospital Management System" -ForegroundColor Green
Write-Host "  DBMS Project - Powered by MySQL & Python Flask" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Initializing MySQL Database (clinic_db)..." -ForegroundColor Cyan
python setup_db.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "[2/2] Launching Web Application on http://127.0.0.1:5000..." -ForegroundColor Green
    python app.py
} else {
    Write-Host "[ERROR] Could not connect to MySQL database." -ForegroundColor Red
}
