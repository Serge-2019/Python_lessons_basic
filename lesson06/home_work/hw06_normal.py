# Задание-1:
# Реализуйте описаную ниже задачу, используя парадигмы ООП:
# В школе есть Классы(5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя(мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать
# в неограниченном кол-ве классов свой определенный предмет.
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.

# Выбранная и заполненная данными структура должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов указанного ученика
#  (Ученик --> Класс --> Учителя --> Предметы)
# 4. Узнать ФИО родителей указанного ученика
# 5. Получить список всех Учителей, преподающих в указанном классе

class Person:
    """Человек"""

    def __init__(self, fio = ''):
        names = list(map(lambda x: x.capitalize(), fio.split()
                         if type(fio) == str else list(fio)))
        if len(names) < 3:
            names += ['#'] * (3-len(names))
        self.__name = dict(zip(['last', 'first', 'middle'], names))

    @property
    def fio(self):
        return " ".join(self.__name.values())

    @property
    def lastName(self):
        return self.__name['last']

    @property
    def firstName(self):
        return self.__name['first']

    @property
    def middleName(self):
        return self.__name['middle']

    @property
    def initials(self):
        return ".".join([self.firstName[0], self.middleName[0]]) + '.'

    @property
    def shortFIO(self):
        return " ".join([self.lastName, self.initials])

    def __str__(self):
        return self.shortFIO


class Teacher(Person):
    """Учитель - должен обязательно преподавать предмет"""

    def __init__(self, fio, subject):
        super().__init__(fio)
        self.subject = subject


class Children(Person):
    """Ребенок, должен иметь 2 родителей обязательно"""

    def __init__(self, fio, mom: Person, dad: Person):
        super().__init__(fio)
        self.mom = mom if type(mom) in [Person, Teacher] else Person(mom)
        self.dad = dad if type(dad) in [Person, Teacher] else Person(dad)


class Klass:
    """Класс"""

    def __init__(self, name:str):
        try:
            self.num = int(name[0:1])
            self.letter = name[1:2].upper()
            self.subjects = []
            self.students = {}
            self.school = None
        except:
            raise ValueError('Имя класса должно быть в формате ЦифраБуква например "4С" ')

    def addSubject(self, subject):
        if self.school == None:
            raise ValueError(f'Класс {self} не добавлен в школу')
        self.subjects.append(subject)

    def addStudent(self, child: Children):
        if not type(child) == Children:
            raise ValueError(f'{child} - не является ребенком')
        if self.school == None:
            raise ValueError(f'Класс {self} не добавлен в школу')
        if child.fio in self.school.students:
            raise ValueError(f'{child.fio} уже учиться в школе')
        self.students[child.fio] = child

    def findStudent(self, search):
        for k, v in self.students.items():
            if (k.find(search) >= 0): return v
        return False

    def student(self, kl):
        if not self.students.get(kl):
            raise KeyError(f'Ученик {kl} не найден')
        return self.students.get(kl)

    def __str__(self):
        return str(self.num) + self.letter


class School:
    """Школа"""

    def __init__(self):
        self.__klasses = {}
        self.__teachers = {}

    def hireTeacher(self, teacher: Teacher):
        if not type(teacher) == Teacher:
            raise ValueError(f'{teacher} - не является учителем')
        if self.__teachers.get(teacher.subject):
            raise ValueError(f'на предмет {teacher.subject} уже нанят учитель')
        self.__teachers[teacher.subject] = teacher

    def setupKlass(self, klass, students = [], subjects=[]):
        kl = klass if type(klass) == Klass else Klass(klass)
        id = str(kl)
        kl.school = self
        for s in subjects:
            kl.addSubject(s)
        for s in students:
            kl.addStudent(s)
        self.__klasses[id] = kl
        return self.__klasses[id]

    def teacher(self, subject):
        return self.__teachers.get(subject) if self.__teachers.get(subject) else 'N/A'

    def klass(self, kl):
        if not self.__klasses.get(kl):
            raise KeyError(f'Класс {kl} не найден')
        return self.__klasses.get(kl)

    def findStudentAndKlass(self, search):
        for v in self.__klasses.values():
            s = v.findStudent(search)
            if s: return (s, v)
        return False

    @property
    def klasses(self):
        return list(self.__klasses.keys())

    @property
    def students(self):
        s = []
        for v in self.__klasses.values():
            s += list(v.students.keys())
        return s




SUBJ_MAT = 'математика'
SUBJ_SON = 'пение'
SUBJ_RUS = 'русский язык'

teacher1 = Teacher('Сидоров Василий Артурович', SUBJ_MAT)
teacher2 = Teacher('Пухова Мария Ивановна', SUBJ_SON)
teacher3 = Teacher('Рыкова Виолета Эфимовна', SUBJ_RUS)

ivanov = Children('Иванов Сергей Петрович', 'Иванова Мария Федоровна', 'Иванов Петр Васильевич')
petrov = Children('Петров Василий Владимирович', 'Петрова Арина Михайловна', 'Петров Владимир Васильевич')
volkova = Children('Волкова Марина Петровна', 'Волкова Мария Федоровна', 'Волков Петр Васильевич')
sidorov = Children('Сидоров Артем Васильевич', 'Плюшкина Юлия Валерьевна', teacher1) # учитель тоже может быть родителем

# есть еще вот такой вариант
mom = Person('Белова Мария Федоровна')
dad = Person('Белов Сергей Васильевич')
belova = Children('Белова Анастасия Сергеевна', mom, dad)
belov = Children('Белов Даниил Сергеевич', mom, dad)


school = School()

# нанимаем учителей
school.hireTeacher(teacher1)
school.hireTeacher(teacher2)
school.hireTeacher(teacher3)

# добавляем классы
# можно сразу с предметами которые там будут
# добавляем туда учащихся
kl_6C = school.setupKlass('6B', [ivanov, petrov, volkova], [SUBJ_RUS, SUBJ_MAT])
kl_5C = school.setupKlass('5C', [sidorov, belova], [SUBJ_SON, SUBJ_MAT])
kl_4A = school.setupKlass('4A')
kl_4A.addSubject(SUBJ_SON) # можно и так
kl_4A.addStudent(belov)



klass = None
student = None
while True:

    if not klass:
        kl = school.klasses
        print("\nСписок классов:")
        for i in range(len(kl)):
            print(f" {i+1}. {kl[i]}")
        klass = input("Введите № класса или (пусто для выхода):")
        if klass == '':
            break
        klass = school.klass( kl[int(klass)-1] )

    if not student:
        print(f"\nВ выбранном классе '{klass}' преподают следущие предметы:")
        for x in klass.subjects:
            print(f"\t{x} - {school.teacher(x)}")

        print(f"\nКласс содержит следущий список учеников:")
        st = klass.students
        keys = list(st.keys())
        values = list(st.values())
        for i in range(len(values)):
            print(f" {i+1}. {values[i]}")
        student = input("Введите № ученика или (пусто для выхода в список классов):")
        if student == '':
            klass = None
            student = None
        else:
            student = klass.student(keys[int(student)-1])
    else:
        print(f"\nУ выбранного ученика '{student}':")
        print(f" Мама: '{student.mom}'")
        print(f" Папа: '{student.dad}'")

        input('\nчтобы выбрать другого ученика нажмите ввод')
        student = None


# найти любого ученика

print("\n\nПоиск в свободном стиле: Волкова")
res = school.findStudentAndKlass('Волкова')
if res:
    student, klass = res
    print(f"Найден ученик '{student}' в классе {klass}:")
    print(f" Мама: '{student.mom}'")
    print(f" Папа: '{student.dad}'")

    print(f"\nВ выбранном классе '{klass}' преподают следущие предметы:")
    for x in klass.subjects:
        print(f"\t{x} - {school.teacher(x)}")

print()

# тестирование ошибки

try:
    school.hireTeacher(Teacher('Крюков Станислав Эфимович', SUBJ_RUS))
except:
    print("Учитель русского языка уже есть в школе:", school.teacher(SUBJ_RUS))

