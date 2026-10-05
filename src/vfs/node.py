"""Узел виртуальной файловой системы."""


DIR = "dir"
FILE = "file"

PARENT_KEY = ".."


class Node:
    """
    Узел VFS: файл или директория.

    Для директории data — словарь {имя: Node}, в который
    включён ключ '..' со ссылкой на родительскую директорию.
    Для файла data — строка с содержимым.
    """

    def __init__(self, file_type, data=None):
        """
        Создаёт узел.

        Args:
            file_type: DIR или FILE.
            data: Словарь детей (для DIR) или строка (для FILE).
        """
        self.file_type = file_type
        if data is None:
            data = {} if file_type == DIR else ""
        self.data = data

    def is_dir(self):
        """Возвращает True, если узел — директория."""
        return self.file_type == DIR

    def is_file(self):
        """Возвращает True, если узел — файл."""
        return self.file_type == FILE