"""Операции над VFS (зарезервировано для Этапа 3)."""


def make_default_root():
    """
    Создаёт пустой корневой узел VFS.

    Returns:
        Корневой узел (директория).
    """
    from src.vfs.node import Node
    return Node(Node.DIR, {"..": None})