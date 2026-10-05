"""История команд (зарезервировано для Этапа 4)."""


class CommandHistory:
    """Хранит историю введённых команд."""

    def __init__(self):
        """Инициализирует пустую историю."""
        self._items = []

    def add(self, command):
        """Добавляет команду в историю."""
        if command:
            self._items.append(command)

    def all(self):
        """Возвращает список всех команд."""
        return list(self._items)