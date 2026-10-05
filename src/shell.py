"""
Ядро эмулятора shell: REPL и диспетчер команд.
"""

from src import parser
from src.commands.cd import cd
from src.commands.cp import cp
from src.commands.find import find
from src.commands.history import history
from src.commands.ls import ls
from src.commands.pwd import pwd
from src.commands.rm import rm
from src.history import CommandHistory
from src.vfs.filesystem import pwd as get_pwd

EXIT_COMMAND = "exit"
COMMENT_PREFIX = "#"


def _prompt(node):
    """Формирует приглашение к вводу."""
    return f"{get_pwd(node)}> "


def _dispatch(node, command, args, history_obj):
    """
    Выполняет команду. Возвращает (node, should_exit).

    Args:
        node: Текущая директория VFS.
        command: Имя команды (или None).
        args: Список аргументов.
        history_obj: Объект CommandHistory.

    Returns:
        Кортеж (новая текущая директория, флаг выхода).
    """
    if command is None:
        return node, False

    match (command, args):
        case ("exit", _):
            return node, True
        case ("ls", []):
            ls(node)
        case ("pwd", []):
            pwd(node)
        case ("cd", [name]):
            node = cd(node, name)
        case ("history", []):
            history(history_obj)
        case ("find", [name]):
            find(node, name)
        case ("cp", [source, dest]):
            cp(node, source, dest)
        case ("rm", [name]):
            rm(node, name)
        case _:
            print(f"{command}: command not found")

    return node, False


def repl(node, history_obj=None):
    """
    Запускает интерактивный цикл Read-Eval-Print.

    Args:
        node: Корневая директория VFS.
        history_obj: Объект CommandHistory (создаётся, если None).
    """
    if history_obj is None:
        history_obj = CommandHistory()

    while True:
        try:
            line = input(_prompt(node))
        except (EOFError, KeyboardInterrupt):
            print()
            return

        stripped = line.strip()
        if not stripped or stripped.startswith(COMMENT_PREFIX):
            continue

        command, args = parser.parse_command(line)

        if command != "history":
            history_obj.add(stripped)

        node, should_exit = _dispatch(node, command, args, history_obj)
        if should_exit:
            return


def run_script(node, path, history_obj=None):
    """
    Выполняет команды из скрипта.

    Печатает каждую команду с приглашением (как диалог),
    затем её результат. Комментарии и пустые строки
    пропускаются. Останавливается по команде exit.

    Args:
        node: Корневая директория VFS.
        path: Путь к файлу скрипта.
        history_obj: Объект CommandHistory (создаётся, если None).
    """
    if history_obj is None:
        history_obj = CommandHistory()

    with open(path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            if not stripped or stripped.startswith(COMMENT_PREFIX):
                continue

            print(f"{_prompt(node)}{stripped}")

            command, args = parser.parse_command(line)

            if command != "history":
                history_obj.add(stripped)

            node, should_exit = _dispatch(node, command, args, history_obj)
            if should_exit:
                return
