@echo off
title AgriVision AI Development Launcher
color 0B
echo ============================================================
echo         AGRIVISION AI - FULL STACK DEV ENVIRONMENT
echo ============================================================
echo.
echo Starting FastAPI Backend on http://localhost:8000 ...
start "AgriVision Backend API" python api_server.py

echo Starting Vite React Frontend on http://localhost:5173 ...
cd frontend
npm run dev
pause

