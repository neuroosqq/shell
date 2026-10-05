"""Узел виртуальной файловой системы (заготовка)."""


class Node:
    """
    Узел VFS: файл или директория.

    Attributes:
        file_type: Тип узла — 'dir' или 'file'.
        data: Содержимое (для файла) или словарь
              имя_ребёнка -> Node (для директории).
    """

    DIR = "dir"
    FILE = "file"

    def __init__(self, file_type, data=None):
        """
        Создаёт узел.

        Args:
            file_type: 'dir' или 'file'.
            data: Содержимое или словарь детей.
        """
        self.file_type = file_type
        if data is None:
            data = {} if file_type == self.DIR else ""
        self.data = data