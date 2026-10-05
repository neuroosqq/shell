"""
Ядро эмулятора shell: REPL и диспетчер команд.
"""

from src import parser
from src.commands import cd, ls


PROMPT = "vfs> "
EXIT_COMMAND = "exit"

# Реестр команд: имя -> функция(args) -> строка
COMMANDS = {
    "ls": ls.execute,
    "cd": cd.execute,
}


def execute_command(command, args):
    """
    Выполняет команду по имени.

    Args:
        command: Имя команды.
        args: Список аргументов.

    Returns:
        Строка для вывода пользователю.
    """
    if command is None:
        return ""
    handler = COMMANDS.get(command)
    if handler is None:
        return f"{command}: command not found"
    return handler(args)


def repl():
    """
    Запускает цикл Read-Eval-Print.

    Читает строку, разбирает её, выполняет команду
    и печатает результат.
    """
    while True:
        try:
            line = input(PROMPT)
        except (EOFError, KeyboardInterrupt):
            print()
            break

        command, args = parser.parse_command(line)

        if command == EXIT_COMMAND:
            break

        result = execute_command(command, args)
        if result:
            print(result)