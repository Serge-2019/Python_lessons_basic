#!/usr/bin/env python3

import os
# import lesson05.home_work.hw05_easy as myos
import hw05_easy as myos

# Задача-1:
# Напишите небольшую консольную утилиту,
# позволяющую работать с папками текущей директории.
# Утилита должна иметь меню выбора действия, в котором будут пункты:
# 1. Перейти в папку
# 2. Просмотреть содержимое текущей папки
# 3. Удалить папку
# 4. Создать папку
# При выборе пунктов 1, 3, 4 программа запрашивает название папки
# и выводит результат действия: "Успешно создано/удалено/перешел",
# "Невозможно создать/удалить/перейти"

# Для решения данной задачи используйте алгоритмы из задания easy,
# оформленные в виде соответствующих функций,
# и импортированные в данный файл из easy.py

def chdir(folder, where = os.getcwd()):
    """
    переходит в директорию `folder` по пути `where` - по умолчанию том месте где запущен скрипт
    возвращает:
    * True - если успешно перешли в каталог
    * False - если folder не является директорией или произошла ошибка (ошибка выводиться в консоль)
    """
    new = folder if os.path.isabs(folder) else os.path.abspath(os.path.join(where, folder))
    try:
        if os.path.isdir(new):
            os.chdir(new)
            return True
        else:
            return False
    except Exception as err:
        print(err)
        return False



if __name__ == "__main__":
    answer = ''
    cwd = os.getcwd()
    while True:
        print('\nТекущая папка: ', cwd)
        answer = input("Выберите пункт меню:\n 1. Перейти в папку\n 2. Просмотреть содержимое текущей папки\n 3. Удалить папку\n 4. Создать папку\n 5. Выход\n:")
        print()

        if answer == '1':
            folder = input("Введите папку куда перейти: ")
            if chdir(folder, cwd):
                print(f"Успешно перешел в папку '{folder}'")
                cwd = os.getcwd()
            else:
                print(f"Невозможно перейти в папку '{folder}'")

        elif answer == '2':
            lst = myos.folderlist(cwd, True)
            if lst:
                print("Содержимое текущей директории:", *lst, sep="\n")
            else:
                print("Произошла ошибка при попытке взять содержимое в текущей директории")

        elif answer == '3':
            folder = input("Введите папку для удаления:")
            if myos.rmdir(folder, cwd):
                print(f"Папка '{folder}' успешно удалена")
            else:
                print(f"Невозможно удалить папку '{folder}'")

        elif answer == '4':
            folder = input("Введите папку для создания:")
            if myos.mkdir(folder, cwd):
                print(f"Папка '{folder}' успешно создана")
            else:
                print(f"Невозможно создать папку '{folder}'")

        elif answer == '5':
            print('Выход')
            break

        else:
            print('Неверный ввод команды, повторите')
