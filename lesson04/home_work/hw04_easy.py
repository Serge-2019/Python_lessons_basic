# Все задачи текущего блока решите с помощью генераторов списков!

# Задание-1:
# Дан список, заполненный произвольными целыми числами.
# Получить новый список, элементы которого будут
# квадратами элементов исходного списка
# [1, 2, 4, 0] --> [1, 4, 16, 0]

import random

lst = random.sample(range(0, 10), 10)

print("Исходный список:", lst)
print("Новый список:", [i ** 2 for i in lst])

# Задание-2:
# Даны два списка фруктов.
# Получить список фруктов, присутствующих в обоих исходных списках.

a = ['apple', 'blueberry', 'apricot', 'avocado', 'banana', 'blackberry']
b = ['blackcurrant', 'blueberry', 'banana', 'boysenberry', 'cherry' ]

print(f"Дано 2 списка {a} и {b}")
print("Фрукты присуствующие в обоих списках:", [i for i in a if i in b])


# Задание-3:
# Дан список, заполненный произвольными числами.
# Получить список из элементов исходного, удовлетворяющих следующим условиям:
# + Элемент кратен 3
# + Элемент положительный
# + Элемент не кратен 4

lst = random.sample(range(-5, 10), 15)

print("Исходный список:", lst)
print("Новый список:", [i for i in lst if i > 0 and i % 3 == 0 and i % 4 != 0])
