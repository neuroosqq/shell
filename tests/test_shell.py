"""Тесты ядра shell."""

from src import shell


def test_unknown_command():
    """Неизвестная команда даёт ошибку."""
    result = shell.execute_command("foobar", [])
    assert result == "foobar: command not found"


def test_ls_stub():
    """Заглушка ls возвращает имя и аргументы."""
    result = shell.execute_command("ls", ["-l"])
    assert "ls" in result


def test_cd_stub():
    """Заглушка cd возвращает имя и аргументы."""
    result = shell.execute_command("cd", [".."])
    assert "cd" in result


def test_empty_command():
    """Пустая команда даёт пустую строку."""
    assert shell.execute_command(None, []) == ""