@echo off
title AgriVision AI Platform Launcher
color 0A
echo ============================================================
echo                    AGRIVISION AI PLATFORM
echo       Smart Agriculture - Brighter Tomorrow
echo ============================================================
echo.
echo [1/3] Initializing Neural ML Models and Intelligence Engines...
echo [2/3] Starting Unified Backend Server on http://localhost:8000 ...
echo [3/3] Opening AgriVision AI in your default web browser...
echo.

start "" http://localhost:8000/
python api_server.py
pause

