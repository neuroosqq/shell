"""
Ядро эмулятора shell: REPL и диспетчер команд.
"""

from src import parser
from src.commands import cd, ls


PROMPT = "vfs> "
EXIT_COMMAND = "exit"
COMMENT_PREFIX = "#"

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


def process_line(line):
    """
    Обрабатывает одну строку ввода.

    Возвращает (should_exit, output).
    Если строка — комментарий или пустая, output пустой.

    Args:
        line: Строка ввода (без \\n).

    Returns:
        Кортеж (should_exit, output).
    """
    stripped = line.strip()
    if not stripped or stripped.startswith(COMMENT_PREFIX):
        return False, ""

    command, args = parser.parse_command(line)

    if command == EXIT_COMMAND:
        return True, ""

    output = execute_command(command, args)
    return False, output


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

        should_exit, output = process_line(line)
        if should_exit:
            break
        if output:
            print(output)


def run_script(path):
    """
    Выполняет команды из скрипта.

    Печатает каждую команду с приглашением (как диалог),
    затем её результат. Комментарии и пустые строки
    пропускаются. Останавливается по команде exit.

    Args:
        path: Путь к файлу скрипта.
    """
    with open(path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            if not stripped or stripped.startswith(COMMENT_PREFIX):
                continue

            print(f"{PROMPT}{stripped}")

            should_exit, output = process_line(line)
            if output:
                print(output)
            if should_exit:
                break