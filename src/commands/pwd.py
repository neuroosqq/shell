"""Команда pwd: вывод текущего пути."""

from src.vfs.filesystem import pwd as _pwd


def pwd(node):
    """
    Печатает абсолютный путь текущей директории.

    Args:
        node: Текущая директория VFS.
    """
    print(_pwd(node))
