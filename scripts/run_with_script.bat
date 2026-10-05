@echo off
REM Run emulator with --script parameter
cd /d "%~dp0\.."
python -m src.main --script scripts/startup.txt
