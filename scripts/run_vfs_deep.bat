@echo off
REM Test VFS: 3+ levels of nested folders
cd /d "%~dp0\.."
python -m src.main --vfs examples/vfs_deep