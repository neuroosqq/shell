"""Тесты ядра shell."""

import io
import contextlib

from src import shell
from src.history import CommandHistory
from src.vfs.filesystem import pwd as get_pwd
from src.vfs.node import DIR, FILE, PARENT_KEY, Node


def _make_root():
    """Создаёт простое тестовое дерево VFS."""
    root = Node(DIR, {})
    docs = Node(DIR, {PARENT_KEY: root})
    root.data["docs"] = docs
    root.data["readme.txt"] = Node(FILE, "hello")
    return root


def _make_history():
    """Создаёт пустую историю команд."""
    return CommandHistory()


def _capture(func, *args):
    """Запускает func(*args), возвращает stdout как строку."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


def test_pwd_at_root():
    """В корне pwd возвращает '/'."""
    root = _make_root()
    assert get_pwd(root) == "/"


def test_pwd_in_subdir():
    """В поддиректории pwd возвращает путь."""
    root = _make_root()
    docs = root.data["docs"]
    assert get_pwd(docs) == "/docs/"


def test_ls_lists_children():
    """ls печатает имена детей без '..'."""
    root = _make_root()
    _, output = _capture(
        shell._dispatch, root, "ls", [], _make_history()
    )
    assert "docs" in output
    assert "readme.txt" in output
    assert ".." not in output


def test_cd_to_subdir():
    """cd переходит в поддиректорию."""
    root = _make_root()
    new_node, should_exit = shell._dispatch(
        root, "cd", ["docs"], _make_history()
    )
    assert new_node is root.data["docs"]
    assert should_exit is False


def test_cd_to_missing_dir():
    """cd в несуществующую директорию печатает ошибку."""
    root = _make_root()
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        new_node, _ = shell._dispatch(
            root, "cd", ["missing"], _make_history()
        )
    assert new_node is root
    assert "No such file or directory" in buffer.getvalue()


def test_exit_command():
    """exit возвращает should_exit=True."""
    root = _make_root()
    _, should_exit = shell._dispatch(
        root, "exit", [], _make_history()
    )
    assert should_exit is True


def test_unknown_command():
    """Неизвестная команда печатает ошибку."""
    root = _make_root()
    _, output = _capture(
        shell._dispatch, root, "foobar", [], _make_history()
    )
    assert "foobar: command not found" in output


def test_empty_command():
    """Пустая команда ничего не делает."""
    root = _make_root()
    new_node, should_exit = shell._dispatch(
        root, None, [], _make_history()
    )
    assert new_node is root
    assert should_exit is False


def test_pwd_command():
    """Команда pwd печатает путь."""
    root = _make_root()
    _, output = _capture(
        shell._dispatch, root, "pwd", [], _make_history()
    )
    assert output.strip() == "/"


def test_history_command():
    """Команда history печатает историю."""
    root = _make_root()
    hist = _make_history()
    hist.add("ls")
    hist.add("cd docs")
    _, output = _capture(
        shell._dispatch, root, "history", [], hist
    )
    assert "1  ls" in output
    assert "2  cd docs" in output


def test_find_command_found():
    """find находит файл в поддереве."""
    root = _make_root()
    _, output = _capture(
        shell._dispatch, root, "find", ["readme.txt"], _make_history()
    )
    assert "/readme.txt" in output


def test_find_command_missing():
    """find с несуществующим именем печатает ошибку."""
    root = _make_root()
    _, output = _capture(
        shell._dispatch, root, "find", ["missing"], _make_history()
    )
    assert "No such file or directory" in output

def test_cp_creates_copy():
    """cp создаёт копию файла."""
    root = _make_root()
    _, _ = _capture(
        shell._dispatch,
        root, "cp", ["readme.txt", "copy.txt"], _make_history()
    )
    assert "copy.txt" in root.data
    assert root.data["copy.txt"].is_file()
    assert root.data["copy.txt"].data == "hello"


def test_cp_missing_source():
    """cp с несуществующим источником печатает ошибку."""
    root = _make_root()
    _, output = _capture(
        shell._dispatch,
        root, "cp", ["missing.txt", "new.txt"], _make_history()
    )
    assert "No such file or directory" in output
    assert "new.txt" not in root.data


def test_rm_removes_file():
    """rm удаляет файл из директории."""
    root = _make_root()
    assert "readme.txt" in root.data
    _, _ = _capture(
        shell._dispatch,
        root, "rm", ["readme.txt"], _make_history()
    )
    assert "readme.txt" not in root.data


def test_rm_directory_error():
    """rm на директории печатает ошибку."""
    root = _make_root()
    _, output = _capture(
        shell._dispatch,
        root, "rm", ["docs"], _make_history()
    )
    assert "Is a directory" in output
    assert "docs" in root.data