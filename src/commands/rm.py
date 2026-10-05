"""Команда rm: удаление файлов."""


def rm(node, name):
    """
    Удаляет файл name из текущей директории.

    Работает только с файлами (не с директориями).

    Args:
        node: Текущая директория VFS.
        name: Имя файла для удаления.
    """
    if name not in node.data:
        print(f"rm: {name}: No such file or directory")
        return

    target = node.data[name]
    if target.is_dir():
        print(f"rm: {name}: Is a directory")
        return

    del node.data[name]