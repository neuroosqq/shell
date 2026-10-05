"""
Точка входа эмулятора shell.

Поддерживает параметры командной строки:
    --vfs PATH      путь к директории VFS
    --script PATH   путь к стартовому скрипту
"""

import argparse
import sys

from src import shell
from src.vfs.filesystem import make_default_root
from src.vfs.loader import VfsLoadError, load_vfs


def parse_args(argv=None):
    """
    Разбирает аргументы командной строки.

    Args:
        argv: Список аргументов (для тестов).
              Если None — берётся sys.argv.

    Returns:
        Объект с полями vfs и script.
    """
    parser = argparse.ArgumentParser(
        prog="shell",
        description="Shell emulator with virtual file system",
    )
    parser.add_argument(
        "--vfs",
        default=None,
        help="Path to the VFS directory",
    )
    parser.add_argument(
        "--script",
        default=None,
        help="Path to the startup script",
    )
    return parser.parse_args(argv)


def print_debug(args):
    """
    Печатает отладочный вывод параметров запуска.

    Args:
        args: Объект с полями vfs и script.
    """
    print(f"VFS path: {args.vfs}")
    print(f"Script path: {args.script}")


def load_root(args):
    """
    Загружает корневой узел VFS по параметрам запуска.

    Args:
        args: Объект с полями vfs и script.

    Returns:
        Корневой узел VFS или None при ошибке.
    """
    if args.vfs is None:
        return make_default_root()

    try:
        return load_vfs(args.vfs)
    except VfsLoadError as error:
        print(f"Error: {error}", file=sys.stderr)
        return None


def main(argv=None):
    """
    Запускает эмулятор.

    Загружает VFS по --vfs (или пустой корень, если не задан).
    Если указан --script — выполняет скрипт и завершается.
    Иначе запускает интерактивный REPL.

    Args:
        argv: Аргументы командной строки (для тестов).
    """
    args = parse_args(argv)
    print_debug(args)

    root = load_root(args)
    if root is None:
        sys.exit(1)

    if args.script:
        shell.run_script(root, args.script)
    else:
        shell.repl(root)


if __name__ == "__main__":
    main()