import math
# Задание-1:
# Напишите функцию, возвращающую ряд Фибоначчи с n-элемента до m-элемента.
# Первыми элементами ряда считать цифры 1 1

def fibonacci(n, m):
    res = []
    a = b = 1
    for i in range(m):
        a, b = b, a + b
        if i >= n-1: res.append(a)
    return res

n = int(input("n="))
m = int(input("m="))
if m > n:
    print("от {} до {} = {}".format(n, m, fibonacci(n, m)))

# Задача-2:
# Напишите функцию, сортирующую принимаемый список по возрастанию.
# Для сортировки используйте любой алгоритм (например пузырьковый).
# Для решения данной задачи нельзя использовать встроенную функцию и метод sort()


def sort_to_max(origin_list):
    ln = len(origin_list)

    for i in range(ln - 1):
        for j in range(i + 1, ln):
            if origin_list[i] > origin_list[j]:
                origin_list[i], origin_list[j] = origin_list[j], origin_list[i]

    return origin_list

print(sort_to_max([2, 10, -12, 2.5, 20, -11, 4, 4, 0]))

# Задача-3:
# Напишите собственную реализацию стандартной функции filter.
# Разумеется, внутри нельзя использовать саму функцию filter.


def my_filter(fun, lst): return [s for s in lst if fun(s)]

print(my_filter(lambda x: x > 0, [1, 2, 0, 2, 3, 0, 2]))

# Задача-4:
# Даны четыре точки А1(х1, у1), А2(x2 ,у2), А3(x3 , у3), А4(х4, у4).
# Определить, будут ли они вершинами параллелограмма.

a = (10, 10)
b = (6, 0)
c = (20, 0)
d = (24, 10)


def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return math.hypot(x2 - x1, y2 - y1)


if distance(a, b) == distance(c, d) and distance(b, c) == distance(a, d) and (a[0] + c[0])/2 == (b[0] + d[0])/2 and (a[1] + c[1])/2 == (b[1] + d[1])/2:
    print('Точки являются вершинами параллелограмма')
else:
    print('Точки НЕ являются вершинами параллелограмма')
