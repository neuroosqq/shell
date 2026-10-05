@echo off
REM Run emulator with both --vfs and --script parameters
cd /d "%~dp0\.."
python -m src.main --vfs examples/vfs_demo --script scripts/startup.txt
