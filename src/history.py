"""История команд."""


class CommandHistory:
    """
    Хранит историю введённых команд.

    Атрибуты:
        _items: список строк (команд) в порядке ввода.
    """

    def __init__(self):
        """Инициализирует пустую историю."""
        self._items = []

    def add(self, command):
        """
        Добавляет команду в историю.

        Пустые строки игнорируются.

        Args:
            command: Строка команды.
        """
        if command:
            self._items.append(command)

    def all(self):
        """
        Возвращает список всех команд.

        Returns:
            Копия списка команд.
        """
        return list(self._items)

    def __len__(self):
        """Возвращает количество команд в истории."""
        return len(self._items)