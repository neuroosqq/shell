"""Тесты разбора аргументов командной строки."""

from src import main


def test_default_args():
    """Без параметров — оба пути None."""
    args = main.parse_args([])
    assert args.vfs is None
    assert args.script is None


def test_vfs_arg():
    """Параметр --vfs сохраняется."""
    args = main.parse_args(["--vfs", "examples/vfs_demo"])
    assert args.vfs == "examples/vfs_demo"
    assert args.script is None


def test_script_arg():
    """Параметр --script сохраняется."""
    args = main.parse_args(["--script", "scripts/startup.txt"])
    assert args.vfs is None
    assert args.script == "scripts/startup.txt"


def test_both_args():
    """Оба параметра вместе."""
    args = main.parse_args([
        "--vfs", "examples/vfs_demo",
        "--script", "scripts/startup.txt",
    ])
    assert args.vfs == "examples/vfs_demo"
    assert args.script == "scripts/startup.txt"