"""
Парсер команд командной строки.

Разбирает строку ввода на имя команды и аргументы,
корректно обрабатывая аргументы в кавычках.
"""


def split_command(line):
    """
    Разбивает строку на токены с учётом кавычек.

    Поддерживает одинарные и двойные кавычки. Аргументы,
    заключённые в кавычки, могут содержать пробелы.

    Args:
        line: Строка ввода пользователя.

    Returns:
        Список токенов (имя команды и аргументы).
    """
    tokens = []
    current = []
    in_quotes = None

    for char in line:
        if char in ("'", '"'):
            if in_quotes is None:
                in_quotes = char
            elif in_quotes == char:
                in_quotes = None
            else:
                current.append(char)
        elif char.isspace() and in_quotes is None:
            if current:
                tokens.append("".join(current))
                current = []
        else:
            current.append(char)

    if current:
        tokens.append("".join(current))

    return tokens


def parse_command(line):
    """
    Разбирает строку в команду и аргументы.

    Args:
        line: Строка ввода пользователя.

    Returns:
        Кортеж (command, args). Если строка пустая —
        возвращает (None, []).
    """
    tokens = split_command(line)
    if not tokens:
        return None, []
    return tokens[0], tokens[1:]
