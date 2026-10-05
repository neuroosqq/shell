# Shell Emulator

Эмулятор командной оболочки UNIX-подобной ОС на языке Python.

## Описание

Проект представляет собой эмулятор shell с виртуальной файловой
системой (VFS). Работает в режиме REPL (Read-Eval-Print Loop),
а также умеет выполнять команды из стартового скрипта.

VFS строится **в памяти** из директории на диске. Исходная
директория при работе эмулятора **не изменяется** — все
модификации (создание, удаление файлов) происходят только
во внутреннем представлении VFS в оперативной памяти.

## Возможности

- `ls` — список файлов и папок в текущей директории VFS
- `cd NAME` — смена текущей директории VFS
- `pwd` — вывод текущего пути
- `find NAME` — поиск файла или папки по имени в поддереве
- `history` — история введённых команд с номерами
- `cp SOURCE DEST` — копирование файла
- `rm NAME` — удаление файла
- `exit` — выход из эмулятора

Дополнительно:

- Парсер команд с поддержкой одинарных и двойных кавычек
- Стартовый скрипт с комментариями
- Загрузка VFS из директории на диске
- Обработка ошибок загрузки VFS
- Параметры командной строки для настройки

## Параметры запуска

    python -m src.main [--vfs PATH] [--script PATH]

- `--vfs PATH` — путь к директории виртуальной файловой системы
- `--script PATH` — путь к стартовому скрипту с командами

Примеры:

    python -m src.main
    python -m src.main --vfs examples/vfs_demo
    python -m src.main --script scripts/startup.txt
    python -m src.main --vfs examples/vfs_deep --script scripts/startup.txt

## Тестовые VFS

В папке `examples/` находятся три варианта VFS для тестирования:

- `vfs_files/` — минимальный (файлы без папок)
- `vfs_demo/` — несколько файлов и одна подпапка
- `vfs_deep/` — вложенность 3+ уровней

## Стартовый скрипт

Файл со стартовым скриптом содержит команды эмулятора —
по одной на строку. Строки, начинающиеся с `#`, являются
комментариями и пропускаются.

При выполнении скрипта на экран выводится как сама команда
(с приглашением), так и её результат — имитация диалога
с пользователем.

## Скрипты запуска для Windows

В папке `scripts/` находятся `.bat`-файлы для тестирования
разных параметров запуска:

- `run_default.bat` — запуск без параметров (интерактивный режим)
- `run_with_vfs.bat` — запуск с параметром `--vfs` (vfs_demo)
- `run_with_script.bat` — запуск с параметром `--script`
- `run_all.bat` — запуск с обоими параметрами
- `run_vfs_minimal.bat` — тест минимального VFS (vfs_files)
- `run_vfs_files.bat` — тест VFS с несколькими файлами (vfs_demo)
- `run_vfs_deep.bat` — тест VFS с 3+ уровнями вложенности (vfs_deep)

Запуск из терминала:

    .\scripts\run_vfs_deep.bat

## Сборка

Проект не требует сборки. Требуется Python 3.10+.

## Тесты

    python -m pytest -v

Всего 26 тестов.

## Ограничения

- Команды `cp` и `rm` работают только с именами в текущей
  директории и не поддерживают пути через `/`.
- Команды `cp` и `rm` работают только с файлами, не с папками.
- Все модификации VFS происходят только в памяти и не
  сохраняются на диск.

## Примеры работы

### Интерактивный режим

    $ python -m src.main --vfs examples/vfs_demo
    VFS path: examples/vfs_demo
    Script path: None
    /> ls
    docs  hello.py  readme.txt
    /> cd docs
    /docs/> pwd
    /docs/
    /docs/> find about.txt
    /docs/about.txt
    /docs/> cd ..
    /> cp readme.txt backup.txt
    /> ls
    backup.txt  docs  hello.py  readme.txt
    /> rm backup.txt
    /> history
    1  ls
    2  cd docs
    3  pwd
    4  find about.txt
    5  cd ..
    6  cp readme.txt backup.txt
    7  ls
    8  rm backup.txt
    /> exit

### Режим скрипта

    $ python -m src.main --vfs examples/vfs_demo --script scripts/startup.txt
    VFS path: examples/vfs_demo
    Script path: scripts/startup.txt
    /> ls
    docs  hello.py  readme.txt
    ...