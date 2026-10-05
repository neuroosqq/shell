"""
Точка входа эмулятора shell.

Поддерживает параметры командной строки:
    --vfs PATH      путь к директории VFS
    --script PATH   путь к стартовому скрипту
"""

import argparse

from src import shell


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


def main(argv=None):
    """
    Запускает эмулятор.

    Если указан --script, выполняет скрипт и завершается.
    Иначе запускает интерактивный REPL.

    Args:
        argv: Аргументы командной строки (для тестов).
    """
    args = parse_args(argv)
    print_debug(args)

    if args.script:
        shell.run_script(args.script)
    else:
        shell.repl()


if __name__ == "__main__":
    main()