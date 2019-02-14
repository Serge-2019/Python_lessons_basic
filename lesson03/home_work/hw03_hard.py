import os
from math import gcd

# Задание-1:
# Написать программу, выполняющую операции (сложение и вычитание) с простыми дробями.
# Дроби вводятся и выводятся в формате:
# n x/y ,где n - целая часть, x - числитель, у - знаменатель.
# Дроби могут быть отрицательные и не иметь целой части, или иметь только целую часть.
# Примеры:
# Ввод: 5/6 + 4/7 (всё выражение вводится целиком в виде строки)
# Вывод: 1 17/42  (результат обязательно упростить и выделить целую часть)
# Ввод: -2/3 - -2
# Вывод: 1 1/3


def sumdiv(a, b, s=1):
    z1, r1, d1 = a
    z2, r2, d2 = b
    z, r, d, i = (0, 0, 1, 1)
    r1 = (abs(d1 * z1) + abs(r1)) * (-1 if r1 < 0 else 1) * (-1 if z1 < 0 else 1)
    r2 = s * (abs(d2 * z2) + abs(r2)) * (-1 if r2 < 0 else 1) * (-1 if z2 < 0 else 1)

    if d1 * d2:
        d = d1 * d2 // gcd(d1, d2)
        i = r1 * d/d1 + r2 * d/d2
        z, r = divmod(abs(i), d)
    if r != 0 and d % r == 0:
        d, r = d // r, 1
    if i < 0:
        if z != 0: z *= -1
        else: r *= -1

    return int(z), int(r), int(d)

el = input("Введите выражение: ").split()
s = 1
a = [0, 0, 1]
b = [0, 0, 1]
for i in el:
    try:
        b[0] = int(i)
    except ValueError:
        if (i.find('/') > 0):
            b[1:] = list(map(int, i.split('/')))
        elif i in ['+', '-']:
            a = sumdiv(a, b, s)
            s = int(i + '1')
            b = [0, 0, 1]
        else:
            print(f'ошибка в выражении "{i}"')
            break

z, r, d = sumdiv(a, b, s)

print(f"Результат:", z if z !=0 else "", f"{r}/{d}" if r else "")


# Задание-2:
# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки
# они получают удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

with open(os.path.join('data', 'workers'), 'r', encoding='UTF-8') as w, open(os.path.join('data', 'hours_of'), 'r', encoding='UTF-8') as h:
    workers = { s.split()[0] + " " + s.split()[1]: s.split() for s in w.readlines()[1:] }
    hours = { s.split()[0] + " " + s.split()[1]: int(s.split()[2]) for s in h.readlines()[1:] }

    print("Сотрудник             Ставка    Отработано      Зарплата")
    for fio, data in workers.items():
        base = int(data[2])
        rate = int(data[4])
        if fio not in hours:
            hours[fio] = salary = 0
        else:
            salary = base + base / rate * (hours[fio] - rate) * (2 if hours[fio] > rate else 1)
        print(f"{fio:<20} {data[4]:^10} {hours[fio]:^12} {salary:^14.2f}")

# Задание-3:
# Дан файл ("data/fruits") со списком фруктов.
# Записать в новые файлы все фрукты, начинающиеся с определенной буквы.
# Т.е. в одном файле будут все фрукты на букву “А”, во втором на “Б” и т.д.
# Файлы назвать соответственно.
# Пример имен файлов: fruits_А, fruits_Б, fruits_В ….
# Важно! Обратите внимание, что нет фруктов, начинающихся с некоторых букв.
# Напишите универсальный код, который будет работать с любым списком фруктов
# и распределять по файлам в зависимости от первых букв, имеющихся в списке фруктов.
# Подсказка:
# Чтобы получить список больших букв русского алфавита:
# print(list(map(chr, range(ord('А'), ord('Я')+1))))


with open(os.path.join('data', 'fruits.txt'), 'r', encoding='UTF-8') as f:
    dic = {}
    for s in list(filter(lambda x: len(x.strip()) > 0, f.readlines())):
        if s[0] not in dic:
            dic[s[0]] = []
        dic[s[0]].append(s)
    f.close()

    for letter, lines in dic.items():
        fl = os.path.join('data', 'fruits_' + letter + '.txt')
        with open(fl, 'w', encoding='UTF-8') as f:
            f.writelines(lines)
            f.close()
            print(f"Файл '{fl}' создан")
