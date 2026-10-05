"""Операции над VFS."""

from src.vfs.node import DIR, PARENT_KEY, Node


def make_default_root():
    """
    Создаёт пустой корневой узел VFS.

    Returns:
        Корневой узел (директория).
    """
    return Node(DIR, {})


def pwd(node):
    """
    Возвращает абсолютный путь к текущей директории.

    Рекурсивно поднимается по '..' до корня. Корень —
    директория, у которой нет родителя.

    Args:
        node: Текущая директория VFS.

    Returns:
        Строка пути, начинающаяся и заканчивающаяся '/'.
    """
    if PARENT_KEY not in node.data:
        return "/"

    parent = node.data[PARENT_KEY]
    for name, child in parent.data.items():
        if name != PARENT_KEY and child is node:
            return pwd(parent) + name + "/"

    return "/"
