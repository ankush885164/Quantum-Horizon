@echo off
title Financial Market Intelligence — Multi-Engine Dashboard Launcher
echo =======================================================================
echo   Financial Market Intelligence — Executive Analytics Dashboard
echo =======================================================================
echo.
echo Choose an option to launch:
echo [1] Launch Microsoft Power BI Powered Dashboard (Web & Desktop Ready)
echo [2] Launch Aurora Green Executive Terminal (Laptop Edition)
echo [3] Launch Streamlit Python Server (Lakehouse Terminal)
echo.
set /p choice="Enter choice [1, 2, or 3, default is 1]: "

if "%choice%"=="2" (
    echo Opening Aurora Green Executive Terminal in your default browser...
    start "" "%~dp0index.html"
) else if "%choice%"=="3" (
    echo Starting Streamlit server...
    python -m streamlit run "%~dp0app.py"
) else (
    echo Opening Power BI Powered Dashboard...
    start "" "%~dp0..\05_powerbi_dashboard\powerbi_dashboard.html"
)
exit
