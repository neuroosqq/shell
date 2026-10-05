"""
Ядро эмулятора shell: REPL и диспетчер команд.
"""

from src import parser
from src.commands.cd import cd
from src.commands.ls import ls
from src.vfs.node import PARENT_KEY


EXIT_COMMAND = "exit"
COMMENT_PREFIX = "#"


def pwd(node):
    """
    Возвращает абсолютный путь к текущей директории.

    Рекурсивно поднимается по '..' до корня. Корень —
    директория, у которой нет родителя.

    Args:
        node: Текущая директория VFS.

    Returns:
        Строка пути, начинающаяся и заканчивающаяся '/'.
    """
    if PARENT_KEY not in node.data:
        return "/"

    parent = node.data[PARENT_KEY]
    for name, child in parent.data.items():
        if name != PARENT_KEY and child is node:
            return pwd(parent) + name + "/"

    return "/"


def _prompt(node):
    """Формирует приглашение к вводу."""
    return f"{pwd(node)}> "


def _dispatch(node, command, args):
    """
    Выполняет команду. Возвращает (node, should_exit).

    Args:
        node: Текущая директория VFS.
        command: Имя команды (или None).
        args: Список аргументов.

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
        case ("cd", [name]):
            node = cd(node, name)
        case _:
            print(f"{command}: command not found")

    return node, False


def repl(node):
    """
    Запускает интерактивный цикл Read-Eval-Print.

    Args:
        node: Корневая директория VFS.
    """
    while True:
        try:
            line = input(_prompt(node))
        except (EOFError, KeyboardInterrupt):
            print()
            return

        command, args = parser.parse_command(line)
        node, should_exit = _dispatch(node, command, args)
        if should_exit:
            return


def run_script(node, path):
    """
    Выполняет команды из скрипта.

    Печатает каждую команду с приглашением (как диалог),
    затем её результат. Комментарии и пустые строки
    пропускаются. Останавливается по команде exit.

    Args:
        node: Корневая директория VFS.
        path: Путь к файлу скрипта.
    """
    with open(path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            if not stripped or stripped.startswith(COMMENT_PREFIX):
                continue

            print(f"{_prompt(node)}{stripped}")

            command, args = parser.parse_command(line)
            node, should_exit = _dispatch(node, command, args)
            if should_exit:
                return