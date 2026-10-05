"""Команда ls: вывод содержимого директории."""

from src.vfs.node import PARENT_KEY


def ls(node):
    """
    Печатает имена детей директории node.

    Ключ '..' не выводится.

    Args:
        node: Текущая директория VFS.
    """
    names = [name for name in node.data if name != PARENT_KEY]
    if not names:
        return
    print("  ".join(sorted(names)))
