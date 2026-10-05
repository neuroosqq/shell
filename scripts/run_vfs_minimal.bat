@echo off
REM Test VFS: files only, no subfolders
cd /d "%~dp0\.."
python -m src.main --vfs examples/vfs_files