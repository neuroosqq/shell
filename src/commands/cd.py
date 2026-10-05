"""Команда cd: смена текущей директории."""


def cd(node, name):
    """
    Возвращает новую текущую директорию.

    Если name — имя поддиректории текущей node, возвращает её.
    Если name — '..', возвращает родителя (если он есть).
    Иначе печатает ошибку и возвращает текущую node.

    Args:
        node: Текущая директория VFS.
        name: Имя поддиректории или '..'.

    Returns:
        Новая текущая директория (или та же при ошибке).
    """
    if name in node.data and node.data[name].is_dir():
        return node.data[name]

    print(f"cd: {name}: No such file or directory")
    return node