"""Команда cp: копирование файлов."""

from src.vfs.node import FILE, Node


def cp(node, source, dest):
    """
    Копирует файл source в файл dest текущей директории.

    Работает только с файлами (не с директориями).
    Если dest уже существует — перезаписывает.

    Args:
        node: Текущая директория VFS.
        source: Имя исходного файла.
        dest: Имя нового файла.
    """
    if source not in node.data:
        print(f"cp: {source}: No such file or directory")
        return

    src_node = node.data[source]
    if not src_node.is_file():
        print(f"cp: {source}: Not a file")
        return

    node.data[dest] = Node(FILE, src_node.data)
