#!/usr/bin/env python3

import os

# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.

def mkdir(folder, where=os.getcwd()):
    """
    создает директорию `folder` с полными правами на запись по пути `where` - по умолчанию том месте где запущен скрипт
    возвращает:
    * True - если каталог успешно создан
    * False - если произошла ошибка - в этом случае выводится ошибка в консоль
    """
    try:
        os.mkdir(os.path.join(where, folder), 0o777)
        return True
    except Exception as err:
        print(err)
        return False


def rmdir(folder, where=os.getcwd()):
    """
    удаляет директорию `folder` по пути `where` - по умолчанию том месте где запущен скрипт
    возвращает:
    * True - если каталог успешно удален
    * False - если произошла ошибка - в этом случае выводится ошибка в консоль
    """
    try:
        os.rmdir(os.path.join(where, folder))
        return True
    except os.error as err:
        print(err)
        return False


if __name__ == "__main__":
    print("Создаем каталоги dir_1 ... dir_9")
    flag = True
    for i in range(1, 9):
        flag = flag and mkdir('dir_' + str(i))
    print('Успешно' if flag else 'НЕ успешно')


    print("Удаляем каталоги dir_1 ... dir_9")
    flag = True
    for i in range(1, 9):
        flag = flag and rmdir('dir_' + str(i))
    print('Успешно' if flag else 'НЕ успешно')

# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.

def folderlist(where=os.getcwd(), andfiles = False): # флаг будет использован в задании normal
    """
    возвращает список папок из директорию `where` - по умолчанию том месте где запущен скрипт
    возвращает:
    * [List] - список папок
    * False - если произошла ошибка - в этом случае выводится ошибка в консоль
    """
    try:
        return [it.name for it in os.scandir(where) if it.is_dir() or andfiles]
    except os.error as err:
        print(err)
        return False


if __name__ == "__main__":
    folders = folderlist()
    if folders:
        print("Папки текущей директории: ", *folders, sep="\n")
    else:
        print("Произошла ошибка при попытке взять файлы в текущей директории")

# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.


def backup(file, where=False):
    """
    создает копию файла `file` добавляя расширение ".bak" по пути `where` или если where = False то рядом с исходным файлом
    возвращает:
    * True - если операция успешно выполнена
    * False - если произошла ошибка - в этом случае выводится ошибка в консоль
    """
    if not os.path.exists(file):
        print(f'Файл "{file}" не существует')
        return False
    if not os.path.isfile(file):
        print(f'"{file}" не является файлом')
        return False

    copy = os.path.abspath(file)
    if where and os.path.isdir(where):
        copy = os.path.join(where, os.path.basename(file))

    try:
        with open(file, 'rb') as fr:
            data = fr.read()
            with open(copy + '.bak', "wb") as to:
                to.write(data)
                return True
    except Exception as err:
        print(err)
        return False


def backup_shutil(file, where=False):  # другая реализация через shutil
    """
    создает копию файла `file` добавляя расширение ".bak" по пути `where` или если where = False то рядом с исходным файлом
    возвращает:
    * True - если операция успешно выполнена
    * False - если произошла ошибка - в этом случае выводится ошибка в консоль
    """
    import shutil

    copy = os.path.abspath(file)
    if where and os.path.isdir(where):
        copy = os.path.join(where, os.path.basename(file))

    try:
        shutil.copy(file, copy + '.bak')
        return True
    except Exception as err:
        print(err)
        return False


if __name__ == "__main__":
    if backup(__file__):
        print(f"Успешно создана копия {__file__} ")
