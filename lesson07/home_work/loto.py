#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа,
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр,
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается
случайная карточка.

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.

Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87
      16 49    55 77    88
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать
модуль random: http://docs.python.org/3/library/random.html

"""

import random

CARD_LINES = 3
CARD_ITEMS = 5
CARD_COLS = 9
CASK_COUNT = 90


def getRandomList(count=5, population=False):
   """возвращает `count` элементов из случайного списока размерностью `population`"""
   p = count if not population or count > population else population
   return random.sample(range(1, p+1), count)


def bagOfCasks():
   """
   генератор мешочка бочонков
   в каждую итерацию вернет следующий бочонок
   """
   for i in getRandomList(CASK_COUNT):
      yield i


class Card:
   """
   Карточка лото содержит 3 строки по 9 клеток.
   В каждой строке по 5 случайных цифр, расположенных по возрастанию.
   """
   def __init__(self, title = 'Карточка'):
      self.title = title
      self.__crossed = set()  # сет для хранения зачеркнутых чисел
      self.__data = getRandomList(CARD_LINES * CARD_ITEMS, CASK_COUNT) # генерируем данные 15 чисел чтобы расположить на карточке
      self.__matrix = [] # данные в виде матрицы
      for i in range(CARD_LINES):
         m = self.__data[i*CARD_ITEMS:(i+1)*CARD_ITEMS]
         m.sort()
         while len(m) < CARD_COLS:
            j = random.randint(0, CARD_COLS-1)
            m[j:j] = ['']
         self.__matrix.append(m)

   # карточка ввиде матрицы 3x9
   @property
   def matrix(self):
      return [['-' if x in self.__crossed else x for x in self.__matrix[i]] for i in range(CARD_LINES)]

   # зачеркивает элемент в карточке если он там присутсвует
   def __isub__(self, value):
      if value in self.__data:
         self.__crossed.add(value)
      return self

   # считает количество не зачернутых чисел на карточке
   def __len__(self):
      return len(self.__data) - len(self.__crossed)

   # итератор по всем числам на карточке
   def __iter__(self):
      return iter(list(self.__data))


   # форматинг матрицы для вывода
   def __str__(self):
      s =  [("{:-^" + str(CARD_COLS * 3) + "}").format(" "+self.title+" ")]
      s += [("{:>3}" * CARD_COLS).format(*self.matrix[i]) for i in range(CARD_LINES)]
      s += ["-" * CARD_COLS * 3]
      return "\n".join(s)



# создаем карточки и начинаем играть
me = Card("Ваша карточка")
computer = Card("Карточка компьютера")

# цикл игры
turn = 1
winner = False
for cask in bagOfCasks():
   print(f"\nХод №{turn}(осталось {CASK_COUNT-turn}): Новый бочонок - {cask}")
   print(me)
   print(computer)

   computer -= cask  # компьютер в любом случае зачеркивает если есть

   if True:  # если поменять на False можно запустить в режиме Computer vs Computer

      a = input("\n[y] - зачеркнуть / [enter] - продолжить: ")
      exist = cask in me  # число есть на моей карточке
      if (not exist and a == 'y') or (a != 'y' and exist):
         print('!!! не верный выбор')
         winner = computer  # если пользователь делает не верный выбор компьютер побеждает
         break

   me -= cask  # зачеркиваем число у себя на карточке если оно там есть

   if not len(me) and not len(computer):
      break  # маловероятно но возможно ничья
   if not len(me):
      winner = me  # я выиграл
      break
   if not len(computer):
      winner = computer  # компьютер выиграл
      break

   turn += 1



# выводим название победившей карточки или ничья
print(f"\nИгра завершена", "в НИЧЬЮ" if winner is False else f"победила {winner.title}")
