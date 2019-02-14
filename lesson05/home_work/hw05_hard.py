#!/usr/bin/env python3

import os
import sys

import hw05_normal as my

# Задание-1:
# Доработайте реализацию программы из примера examples/5_with_args.py,
# добавив реализацию следующих команд (переданных в качестве аргументов):
#   cp <file_name> - создает копию указанного файла
#   rm <file_name> - удаляет указанный файл (запросить подтверждение операции)
#   cd <full_path or relative_path> - меняет текущую директорию на указанную
#   ls - отображение полного пути текущей директории
# путь считать абсолютным (full_path) -
# в Linux начинается с /, в Windows с имени диска,
# все остальные пути считать относительными.

# Важно! Все операции должны выполняться в той директории, в который вы находитесь.
# Исходной директорией считать ту, в которой был запущен скрипт.

# P.S. По возможности, сделайте кросс-платформенную реализацию.

def print_help(do):
    print(f"\nПараметры запуска:\n   {__file__} <cmd> [param]\n\nгде <cmd> одна из следущих команд:")
    for cmd in do.items():
        print(" *", cmd[0], cmd[1][1])
    return True


def ping(*args):
    print("pong")
    return True


def remove_file(file, where=os.getcwd()):
    """
    удаляет файл `file` по пути `where` - по умолчанию том месте где запущен скрипт
    возвращает:
    * True - если каталог успешно удален
    * False - если произошла ошибка - в этом случае выводится ошибка в консоль
    """
    try:
        os.remove(os.path.join(where, file))
        return True
    except os.error as err:
        print(err)
        return False


def current_dir(*args):
    print('Полный путь текущей директории:', os.path.abspath(os.getcwd()))
    return True


if __name__ == "__main__":

    do = {
        "help": (print_help, "- печатает данную справку", False),
        "mkdir": (my.myos.mkdir, "<dir_name> - cоздает папку <dir_name>", True),
        "ping": (ping, "- тестовый ключ", False),
        "cp": (my.myos.backup, "<file_name> - создает копию файла <file_name> с расширением .bak в текущей директории", True),
        "rm": (remove_file, "<file_name> - удаляет файл <file_name>", True),
        "cd": (my.chdir, "<dir_name> - меняет текущую директорию на указанную в <dir_name>", True),
        "ls": (current_dir, "- отображает полный путь текущей директории", False),
    }

    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
    param = sys.argv[2] if len(sys.argv) > 2 else ''

    if not do.get(cmd):
        print('\n!!! Неверная команда')
    elif not param and do.get(cmd)[2]:
        print(f'\n!!! Отсуствует обязательный параметр для команды {cmd}')
    elif cmd == 'help':
        print_help(do)
    else:
        if do.get(cmd)[0](param, os.getcwd()):
            print('Операция успешно выполненна')
            cwd = os.getcwd()
            print(f'Текущая директория "{cwd}" содержит:', *my.myos.folderlist(cwd, True), sep="\n")
        else:
            print(f'Произошла ошибка во время операции: {cmd} {param}')
