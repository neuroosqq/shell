# Shell Emulator

Эмулятор командной оболочки UNIX-подобной ОС на языке Python.

## Описание

Проект представляет собой эмулятор shell с виртуальной файловой
системой (VFS). Работает в режиме REPL (Read-Eval-Print Loop),
а также умеет выполнять команды из стартового скрипта.

## Возможности

- `ls` — список файлов и папок
- `cd` — смена текущей директории
- `exit` — выход из эмулятора
- Парсер команд с поддержкой кавычек
- Стартовый скрипт с комментариями
- Параметры командной строки для настройки

## Параметры запуска

    python -m src.main [--vfs PATH] [--script PATH]

- `--vfs PATH` — путь к директории виртуальной файловой системы
- `--script PATH` — путь к стартовому скрипту с командами

Примеры:

    python -m src.main
    python -m src.main --vfs examples/vfs_demo
    python -m src.main --script scripts/startup.txt
    python -m src.main --vfs examples/vfs_demo --script scripts/startup.txt

## Стартовый скрипт

Файл со стартовым скриптом содержит команды эмулятора —
по одной на строку. Строки, начинающиеся с `#`, являются
комментариями и пропускаются.

При выполнении скрипта на экран выводится как сама команда
(с приглашением `vfs> `), так и её результат — имитация
диалога с пользователем.

## Скрипты запуска для Windows

В папке `scripts/` находятся 4 `.bat`-файла для тестирования
параметров командной строки:

- `run_default.bat` — запуск без параметров (интерактивный режим)
- `run_with_vfs.bat` — запуск с параметром `--vfs`
- `run_with_script.bat` — запуск с параметром `--script`
- `run_all.bat` — запуск с обоими параметрами

Запуск из терминала:

    .\scripts\run_all.bat

Или двойным кликом в проводнике Windows.

## Сборка

Проект не требует сборки. Требуется Python 3.10+.

## Тесты

    python -m pytest -v

## Примеры работы

### Интерактивный режим

    $ python -m src.main
    VFS path: None
    Script path: None
    vfs> ls
    ls: args=[]
    vfs> cd "my folder"
    cd: args=['my folder']
    vfs> exit

### Режим скрипта

    $ python -m src.main --script scripts/startup.txt
    VFS path: None
    Script path: scripts/startup.txt
    vfs> ls
    ls: args=[]
    vfs> cd docs
    cd: args=['docs']
    ...