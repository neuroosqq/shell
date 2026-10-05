@echo off
REM Run emulator with --vfs parameter
cd /d "%~dp0\.."
python -m src.main --vfs examples/vfs_demo
