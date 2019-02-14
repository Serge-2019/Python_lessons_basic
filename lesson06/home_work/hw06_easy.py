import math
from functools import reduce

# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.

class Figure:
    """базовый класс для фигур"""

    def __init__(self, points = [], minPoints = 3):
        self.points = []
        for i in points:
            if i not in self.points: self.points.append(i)

        ln = len(self.points)
        num = minPoints if minPoints > 2 else 3
        if ln != num:
            raise ValueError(f"Класс {self.__class__.__name__} требует {num} уникальные точки, получено {ln}")

        # из точек строим вектора
        self.vectors = [self.vector(self.points[i], self.points[i+1])
                        for i in range(len(self.points)-1)]
        self.vectors.append(self.vector( self.points[len(self.points)-1], self.points[0]))


    def perimeter(self):
        return sum(map(lambda x: x[2], self.vectors))

    def square(self):
        raise NotImplementedError

    @staticmethod
    def vector(a, b):
        """вектор между точками и его длина"""
        x, y = ((b[0] - a[0]), (b[1] - a[1]))  # вектор по координатам
        l = math.sqrt(x**2 + y**2) # длина вектора
        return (x, y, l)

    @staticmethod
    def angle(v1, v2):
        """угол между векторами в радианах"""
        return math.acos((v1[0]*v2[0] + v1[1]*v2[1]) / (v1[2]*v2[2]))




class Triangle(Figure):
    """Треугольник"""

    def square(self):
        pp = self.perimeter() / 2
        return math.sqrt(reduce(lambda x, y: x * y, map(lambda x: pp - x[2], self.vectors), pp))

    def heights(self):
        cf = 2 * self.square()
        return tuple(cf/h[2] for h in self.vectors)



t = Triangle([(0,0), (10,0), (5,5)])
h = t.heights()
print("Треугольник ABC имеет высоты:")
print(" Ha= {:0.2f}\n Hb= {:0.2f}\n Hc= {:0.2f}".format(*h))
print(f" периметр = {t.perimeter():0.2f}")
print(f" площадь = {t.square():0.2f}")
print(f" максимальная высота = {max(h):0.2f}\n")



# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;
# вычисления: длины сторон, периметр, площадь.


class Quadrangle(Figure):
    """Произвольный четырехугольник"""

    def __init__(self, points):
        super().__init__(points, 4)

    def square(self):
        a = self.angle(self.vectors[0], self.vectors[3])
        g = self.angle(self.vectors[1], self.vectors[2])

        pp = self.perimeter() / 2
        mul = reduce(lambda x, y: x * y, map(lambda x: pp - x[2], self.vectors), 1)
        abcd = reduce(lambda x, y: x * y[2], self.vectors, 1)
        cos2 = math.cos((a+g)/2) ** 2
        return math.sqrt(mul - abcd * cos2)

    def isTrapezium(self):
        a = math.degrees(self.angle(self.vectors[0], self.vectors[2]))
        g = math.degrees(self.angle(self.vectors[1], self.vectors[3]))
        return a == 0 or a == 180 or g == 0 or g == 180

    def isIsosceles(self):
        a,b,c,d = self.vectors
        return a[2] == c[2] or b[2] == d[2]


t = Quadrangle([(0, 0), (5, 5), (10, 5), (15, 0)])

tr = t.isTrapezium()
ss = t.isIsosceles()
ln = [k[2] for k in t.vectors]

trapezium = ("НЕ " if not tr else '') + "является" + (" РАВНОБОКОЙ" if tr and ss else '')

print(f"Четырехугольник ABCD {trapezium} трапецией и имеет стороны:")
print(" A= {:0.2f}\n B= {:0.2f}\n C= {:0.2f}\n D= {:0.2f}".format(*ln))
print(f" периметр = {t.perimeter():0.2f}")
print(f" площадь = {t.square():0.2f}")

