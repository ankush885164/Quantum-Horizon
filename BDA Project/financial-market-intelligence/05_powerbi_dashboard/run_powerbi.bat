@echo off
title Launch Power BI Financial Intelligence Dashboard
echo ================================================================
echo FINANCIAL MARKET INTELLIGENCE — POWER BI POWERED DASHBOARD
echo ================================================================
echo.
echo Launching Live Power BI Dashboard...
start http://localhost:8080/
start "" "%~dp0powerbi_dashboard.html"
exit
