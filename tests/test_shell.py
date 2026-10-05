"""Тесты ядра shell."""

import io
import contextlib

from src import shell
from src.vfs.node import DIR, FILE, PARENT_KEY, Node


def _make_root():
    """Создаёт простое тестовое дерево VFS."""
    root = Node(DIR, {})
    docs = Node(DIR, {PARENT_KEY: root})
    root.data["docs"] = docs
    root.data["readme.txt"] = Node(FILE, "hello")
    return root


def _capture(func, *args):
    """Запускает func(*args), возвращает stdout как строку."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


def test_pwd_at_root():
    """В корне pwd возвращает '/'."""
    root = _make_root()
    assert shell.pwd(root) == "/"


def test_pwd_in_subdir():
    """В поддиректории pwd возвращает путь."""
    root = _make_root()
    docs = root.data["docs"]
    assert shell.pwd(docs) == "/docs/"


def test_ls_lists_children():
    """ls печатает имена детей без '..'."""
    root = _make_root()
    _, output = _capture(shell._dispatch, root, "ls", [])
    assert "docs" in output
    assert "readme.txt" in output
    assert ".." not in output


def test_cd_to_subdir():
    """cd переходит в поддиректорию."""
    root = _make_root()
    new_node, should_exit = shell._dispatch(root, "cd", ["docs"])
    assert new_node is root.data["docs"]
    assert should_exit is False


def test_cd_to_missing_dir():
    """cd в несуществующую директорию печатает ошибку."""
    root = _make_root()
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        new_node, _ = shell._dispatch(root, "cd", ["missing"])
    assert new_node is root
    assert "No such file or directory" in buffer.getvalue()


def test_exit_command():
    """exit возвращает should_exit=True."""
    root = _make_root()
    _, should_exit = shell._dispatch(root, "exit", [])
    assert should_exit is True


def test_unknown_command():
    """Неизвестная команда печатает ошибку."""
    root = _make_root()
    _, output = _capture(shell._dispatch, root, "foobar", [])
    assert "foobar: command not found" in output


def test_empty_command():
    """Пустая команда ничего не делает."""
    root = _make_root()
    new_node, should_exit = shell._dispatch(root, None, [])
    assert new_node is root
    assert should_exit is False