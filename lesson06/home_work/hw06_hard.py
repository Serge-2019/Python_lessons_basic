import os

# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки они получают
# удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла


class Worker:
    def __init__(self, data):
        self.data = dict(zip(['first', 'last', 'base', 'title', 'norma'], data.split()))
        self.hours = 0

    @property
    def salary(self):
        return self.base + self.base / self.norma * (self.hours - self.norma) * (2 if self.hours > self.norma else 1)

    @property
    def hours(self):
        return int(self.data['hours'])

    @hours.setter
    def hours(self,value):
        self.data['hours'] = int(value) if value else 0

    @property
    def name(self):
        return " ".join([self.data['first'], self.data['last']])

    @property
    def base(self):
        return int(self.data['base'])

    @property
    def norma(self):
        return int(self.data['norma'])





with open(os.path.join('data', 'workers'), 'r', encoding='UTF-8') as fw, open(os.path.join('data', 'hours_of'), 'r', encoding='UTF-8') as fh:
    hours = {s.split()[0] + " " + s.split()[1]: s.split()[2] for s in fh.readlines()[1:]}

    print("Сотрудник             Ставка    Отработано      Зарплата")
    for s in fw.readlines()[1:]:
        w = Worker(s)
        w.hours = hours.get(w.name)
        print(f"{w.name:<20} {w.norma:^10} {w.hours:^12} {w.salary:^14.2f}")
