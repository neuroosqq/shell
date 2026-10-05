"""Загрузка VFS из директории на диске."""

import os

from src.vfs.node import DIR, FILE, PARENT_KEY, Node


class VfsLoadError(Exception):
    """Ошибка загрузки VFS."""


def _build_node(path, parent):
    """
    Рекурсивно строит узел VFS для файла или директории.

    Args:
        path: Путь на диске.
        parent: Родительский узел (или None для корня).

    Returns:
        Построенный узел.
    """
    if os.path.isdir(path):
        node = Node(DIR, {})
        if parent is not None:
            node.data[PARENT_KEY] = parent
        for name in sorted(os.listdir(path)):
            child_path = os.path.join(path, name)
            child = _build_node(child_path, node)
            node.data[name] = child
        return node

    with open(path, "r", encoding="utf-8", errors="replace") as file:
        content = file.read()
    return Node(FILE, content)


def load_vfs(path):
    """
    Загружает VFS из директории на диске.

    Ничего не изменяет на диске — только читает.

    Args:
        path: Путь к директории VFS.

    Returns:
        Корневой узел VFS.

    Raises:
        VfsLoadError: Если путь не существует или не директория.
    """
    if not os.path.exists(path):
        raise VfsLoadError(f"VFS path not found: {path}")
    if not os.path.isdir(path):
        raise VfsLoadError(f"VFS path is not a directory: {path}")

    return _build_node(path, None)