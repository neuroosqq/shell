"""Тесты парсера команд."""

from src import parser


def test_empty_line():
    """Пустая строка даёт None и пустой список."""
    assert parser.parse_command("") == (None, [])


def test_simple_command():
    """Простая команда без аргументов."""
    assert parser.parse_command("ls") == ("ls", [])


def test_command_with_args():
    """Команда с аргументами."""
    assert parser.parse_command("cd dir") == ("cd", ["dir"])


def test_quoted_argument_double():
    """Аргумент в двойных кавычках."""
    cmd, args = parser.parse_command('echo "hello world"')
    assert cmd == "echo"
    assert args == ["hello world"]


def test_quoted_argument_single():
    """Аргумент в одинарных кавычках."""
    cmd, args = parser.parse_command("echo 'hello world'")
    assert cmd == "echo"
    assert args == ["hello world"]


def test_mixed_quotes():
    """Кавычки и обычные аргументы вместе."""
    cmd, args = parser.parse_command('cp "a b" c')
    assert cmd == "cp"
    assert args == ["a b", "c"]
