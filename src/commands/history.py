"""Команда history: вывод истории введённых команд."""


def history(history_obj):
    """
    Печатает историю команд с номерами.

    Формат строки: 'N  команда', начиная с 1.

    Args:
        history_obj: Объект CommandHistory.
    """
    for index, command in enumerate(history_obj.all(), start=1):
        print(f"{index}  {command}")
