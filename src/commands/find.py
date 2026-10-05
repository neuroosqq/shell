"""Команда find: поиск узла по имени в дереве VFS."""

from src.vfs.filesystem import pwd as _pwd
from src.vfs.node import PARENT_KEY


def _search(node, name, results):
    """
    Рекурсивно ищет узлы с именем name.

    Args:
        node: Текущая директория для обхода.
        name: Искомое имя.
        results: Список для накопления путей.
    """
    for child_name, child in node.data.items():
        if child_name == PARENT_KEY:
            continue
        if child_name == name:
            results.append(_join_path(node, child_name))
        if child.is_dir():
            _search(child, name, results)


def _join_path(node, name):
    """Собирает путь к ребёнку node с именем name."""
    base = _pwd(node)
    if base.endswith("/"):
        return base + name
    return base + "/" + name


def find(node, name):
    """
    Ищет узел с именем name в поддереве текущей директории.

    Выводит полные пути найденных узлов. Если ничего
    не найдено — печатает сообщение об ошибке.

    Args:
        node: Текущая директория VFS.
        name: Имя искомого узла.
    """
    results = []
    _search(node, name, results)

    if not results:
        print(f"find: {name}: No such file or directory")
        return

    for path in results:
        print(path)