"""
== OpenWeatherMap ==

OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.

Необходимо решить следующие задачи:

== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.

    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID,
    используя дополнительную библиотеку GRAB (pip install grab)

        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up

        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in

        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys

        Ключ имеет смысл сохранить в локальный файл, например, "app.id"


== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz

    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка
     (воспользоваться модулем gzip
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)

    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}


== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a

    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a

    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a


    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}


== Сохранение данных в локальную БД ==
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):

    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных

2. Выводить список стран из файла и предлагать пользователю выбрать страну
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))

3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.


При работе с XML-файлами:

Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с пространствами имен удобно пользоваться такими функциями:

    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''

    tree = ET.parse(f)
    root = tree.getroot()

    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}

    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...

"""
import os
import sys
import sqlite3
import csv
import urllib.request
import gzip
import json
import pickle
import functools
import logging
import argparse
from datetime import datetime

from grab import Grab

class API:
    'Класс для работы с API'

    __api_id = None
    def __init__(self, api_id=None):
        if api_id:
            self.api_id = api_id
        if not self.api_id:
            logging.warning("Нет API_ID ключа для работы с API попробуйте получить его через grabApiID")

    def __call__(self, cities=[]):
        if not cities or not self.api_id:
            return []
        ids = [str(i) for i in cities if i and int(i) > 0]
        url = 'https://api.openweathermap.org/data/2.5/group?id='
        url += ','.join(ids) + f'&units=metric&appid={self.api_id}'
        try:
            logging.debug("\n\tСкачиваем погоду для городов: %s", cities)
            with urllib.request.urlopen(url) as w:
                a = w.read()
            logging.debug("\n\tПолучили данные - парсим JSON")
            b = json.loads(a, encoding='utf-8')
            return b['list']
        except Exception as ex:
            logging.error("Невозможно получить погоду\n\t\t%s\n\tURL: %s", ex, url)
            return False

    @staticmethod
    def grabApiId(user, password):
        g = Grab()

        try:
            logging.debug("\n\tЗаходим на страницу для логина, получаем форму логина")
            g.go('https://home.openweathermap.org/users/sign_in')
            g.doc.set_input('user[email]', user)
            g.doc.set_input('user[password]', password)
            g.doc.set_input('user[remember_me]', '1')
            g.submit()
        except Exception as ex:
            logging.error("[%s] Невозможно отправить форму логина:\n\t\t%s\n\tURL: %s", g.doc.code, ex, g.doc.url)
            return None

        err = g.doc('//div[text()="Alert"]/following-sibling::div').text(False)
        if err:
            logging.error("[%s] Невозможно залогинется: %s\n\tURL: %s", 401, err, g.doc.url)
            return None

        try:
            logging.debug("\n\tЗаходим на страницу ключей, получаем ключ")
            g.go('https://home.openweathermap.org/api_keys')
        except Exception as ex:
            logging.error("[%s] Ошибка на странице ключей:\n\t\t%s\n\tURL: %s", g.doc.code, ex, g.doc.url)
            return None

        appid = g.doc('//th[text()="Key"]/following::pre').text(False)
        err = g.doc('//div[text()="Alert"]/following-sibling::div').text(False)
        if not appid and not err:
            logging.warning("[%s] Ключ не найден, создайте ключ\n\tURL: %s", 404, g.doc.url)
            return None
        if err:
            logging.error("[%s] Ошибка на странице: %s\n\tURL: %s", 403, err, g.doc.url)
            return None

        return appid

    @property
    def api_id(self):
        if API.__api_id: return API.__api_id
        cache = os.path.join(os.path.dirname(__file__), 'app.id')
        if not os.path.isfile(cache): return None
        try:
            logging.debug("\n\tЧитаем ключ из кеш файла %s", cache)
            with open(cache, "r") as f: API.__api_id = f.read().strip()
        except Exception as ex:
            logging.warning("Не возможно прочитать ключ из файла %s\n\tERROR: %s", cache, ex)
        finally:
            return API.__api_id

    @api_id.setter
    def api_id(self, api_id):
        try:
            value = str(api_id).strip()
            if value == '':
                value = None
            cache = os.path.join(os.path.dirname(__file__), 'app.id')
            if value and value != self.api_id:
                logging.debug("\n\tСохранем ключ в кеш файл %s", cache)
                with open(cache, "w") as f: f.write(value)
            elif not value and os.path.isfile(cache):
                logging.debug("\n\tКлюч пустой удаляем кеш файл %s", cache)
                os.remove(cache)
        except Exception as ex:
            logging.warning("Не возможно сохранить ключ в файл %s\n\tERROR: %s", cache, ex)
        finally:
            API.__api_id = value


class Database:
    'Класс для работы с базой данных SQLite'

    __connections = {}

    def __init__(self, database='database.db'):
        self.database = os.path.join(os.path.dirname(__file__), database)
        logging.debug("Инициализация БД %s", self.database)
        self.initTables()

    def __del__(self):
        if Database.__connections.get(self.database):
            con = Database.__connections.pop(self.database)
            con.close()

    @property
    def db(self):
        if not Database.__connections.get(self.database):
            logging.debug("\n\tСоздаем соеденение с базой данных")
            Database.__connections[self.database] = sqlite3.connect(self.database)
            Database.__connections[self.database].row_factory = sqlite3.Row
        return Database.__connections[self.database]

    def select(self, sql, params=[]):
        try:
            cur = self.db.cursor()
            logging.debug("\n\tЗапуск SQL: %s\n\tPARAMS: %s", sql, params)
            cur.execute(sql, params)
            return cur
        except Exception as ex:
            cur.close()
            logging.error("Ошибка БД: %s\n\tSQL: %s\n\tPARAMS: %s", ex.args[0], sql, params)
            raise

    def execute(self, sql, params=[]):
        try:
            cur = self.db.cursor()
            logging.debug("\n\tЗапуск SQL: %s\n\tPARAMS: %s", sql, params)
            cur.execute(sql, params)
            self.db.commit()
            lastrowid = cur.lastrowid
            cur.close()
            return lastrowid
        except Exception as ex:
            cur.close()
            self.db.rollback()
            logging.error("Ошибка БД: %s\n\tSQL: %s\n\tPARAMS: %s", ex.args[0], sql, params)
            raise

    def bulk(self, sql, array=[]):
        try:
            cur = self.db.cursor()
            logging.debug("\n\tЗапуск MANY SQL: %s\n\tITEMS: %s", sql, len(array))
            cur.executemany(sql, array)
            self.db.commit()
            rowcount = cur.rowcount
            cur.close()
            return rowcount
        except Exception as ex:
            cur.close()
            self.db.rollback()
            logging.error("Ошибка БД: %s\n\tSQL: %s\n\tPARAMS: %s", ex.args[0], sql, array)
            raise

    def script(self, sql):
        try:
            cur = self.db.cursor()
            logging.debug("\n\tЗапуск SCRIPT SQL: %s", sql)
            cur.executescript(sql)
            self.db.commit()
            rowcount = cur.rowcount
            cur.close()
            return rowcount
        except Exception as ex:
            cur.close()
            self.db.rollback()
            logging.error("Ошибка БД: %s\n\tSQL: %s", ex.args[0], sql)
            raise

    def countriesSeed(self):
        # данные качаем и кешируем отсюда https://datahub.io/core/country-list/r/data.csv
        url = 'https://datahub.io/core/country-list/r/data.csv'
        fname = os.path.join(os.path.dirname(__file__), 'countries.csv')

        if not os.path.isfile(fname):
            try:
                logging.debug("\n\tКеш файл для стран НЕ существует - скачиваем даные с %s", url)
                with urllib.request.urlopen(url) as w, open(fname, 'w', encoding='UTF-8') as z:
                    z.write(w.read().decode('utf-8'))
            except Exception as ex:
                logging.error("Невозможно скачать страны: %s", ex)
                raise

        try:
            logging.debug("\n\tПарсим данные стран из кеш файла")
            with open(fname, 'r', encoding='UTF-8') as csvfile:
                values = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
                values.pop(0)
        except Exception as ex:
            logging.error("Невозможно спарсить страны из файла: %s", ex)
            raise

        return ('INSERT INTO `countries` (name, code) VALUES (?, ?) ', values)

    def citiesSeed(self):
        # данные качаем и кешируем отсюда http://bulk.openweathermap.org/sample/city.list.json.gz
        url = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
        fname = os.path.join(os.path.dirname(__file__), 'cities.json')

        if not os.path.isfile(fname):
            try:
                logging.debug("\n\tКеш файл для городов НЕ существует - скачиваем даные с %s", url)
                with urllib.request.urlopen(url) as w, open(fname, 'wb') as z:
                    z.write(gzip.decompress(w.read()))
            except Exception as ex:
                logging.error("Невозможно скачать города: %s", ex)
                raise

        def parse(data):
            return functools.reduce(
                lambda x, y: x + ([y] if type(y) != list else y),
                list(data.values()), [])
        try:
            logging.debug("\n\tПарсим данные городов из кеш файла")
            with open(fname, 'rb') as f:
                values = json.load(f, object_hook=parse)
        except Exception as ex:
            logging.error("Невозможно спарсить города из файла: %s", ex)
            raise

        return ('INSERT INTO `cities` (id, name, country, lon, lat) VALUES (?, ?, ?, ?, ?) ', values)

    def initTables(self):
        tables = {
            'countries': """
                CREATE TABLE IF NOT EXISTS `countries` ( `code` TEXT NOT NULL, `name` TEXT, PRIMARY KEY(`code`) );
                CREATE INDEX IF NOT EXISTS cn_nam ON countries (`name`);
                """,
            'cities': """
                CREATE TABLE IF NOT EXISTS `cities` (
                    `id` INTEGER  NOT NULL,
                    `name` VARCHAR(30),
                    `country` VARCHAR(2),
                    `lon` REAL,
                    `lat` REAL,
                    favorite INTEGER DEFAULT 0,
                    PRIMARY KEY(`id`)
                );
                CREATE INDEX IF NOT EXISTS c_cnt ON cities (`country`);
                CREATE INDEX IF NOT EXISTS c_nam ON cities (`name`);
                CREATE INDEX IF NOT EXISTS c_fav ON cities (`favorite`);
                """,
            'wheather': """
                CREATE TABLE IF NOT EXISTS `wheather` (
                    `city_id` INTEGER,
                    `dt` INTEGER,
                    `temp` REAL,
                    `wheather_id` INTEGER,
                    `wheather` TEXT,
                    PRIMARY KEY(`city_id`, `dt`)
                );
                """
        }

        for t in tables.keys():
            self.script(tables[t])
            cnt = self.select(f"SELECT COUNT(*) as cnt FROM `{t}`").fetchone()['cnt']
            seed = getattr(self, f"{t}Seed", None)
            if cnt < 1 and seed:
                sql, values = seed()
                if sql:
                    logging.debug("Заполняем таблицу %s ...", t)
                    r = self.bulk(sql, values)
                    logging.debug("... добавлено %s записей", r)

class Wheather:

    def __init__(self, database='database.db', api_id=None, loglevel=logging.ERROR):
        self.setupLogging(loglevel)
        self.db = Database(database)
        self.api = API(api_id)
        self.cities_count = self.countCities(favorite=1)

    def setupLogging(self, loglevel):
        if type(loglevel) == str:
            loglevel = getattr(logging, str(loglevel).upper(), logging.ERROR)
        logging.getLogger().setLevel(loglevel)

    def setupApiId(self, username, password):
        logging.debug('Получаем API ID через логин/пароль')
        api_id = API.grabApiId(username, password)
        if api_id:
            self.api.api_id = api_id
            return True
        return False

    def clearList(self):
        self.cities_count = self.setCities(0)
        return 0

    def sqlCities(self, **kwargs):
        country = kwargs.get('country', None)
        city = kwargs.get('city', None)
        ids = kwargs.get('ids', None)
        favorite = kwargs.get('favorite', None)
        flt = {}
        sql = ["FROM cities as c"]
        if country:
            sql += ["INNER"]
            flt['country'] = country
        else:
            sql += ["LEFT"]
        sql += ["JOIN countries as cn ON c.country = cn.code"]
        if country: sql += ["AND (cn.name LIKE :country OR cn.code LIKE :country)"]
        sql += ["WHERE 1"]
        if city:
            sql += ["AND c.name LIKE :city"]
            flt['city'] = city
        if ids and type(ids) == list and len(ids)>0:
            sql += ["AND c.id IN (" + ",".join(map(lambda x: str(x), ids)) + ")"]
        if favorite:
            sql += ["AND favorite = :favorite"]
            flt['favorite'] = favorite
        return (" ".join(sql), flt)

    def countCities(self, **kwargs):
        sql, flt = self.sqlCities(**kwargs)
        return self.db.select(f'SELECT COUNT(*) as cnt {sql}', flt).fetchone()['cnt']

    def cities(self, page=0, limit=20, **kwargs):
        sql, flt = self.sqlCities(**kwargs)
        limit = f'LIMIT {page * limit},{limit}' if limit else ''
        return self.db.select(f'SELECT c.id, c.name, cn.name as country_name, CASE favorite WHEN 1 THEN "*" ELSE "" END as saved {sql} ORDER BY c.name ASC {limit}', flt)

    def setCities(self, flag=1, **kwargs):
        sql, flt = self.sqlCities(**kwargs)
        flag = 1 if flag else 0
        self.db.execute(f'UPDATE cities SET favorite = {flag} WHERE id IN (SELECT c.id {sql})', flt)
        return self.countCities(favorite=1)

    def printList(self, data, columns={}, idd='id', frm={}):
        if not data: return

        def prn(header, columns, line=None, num = 0, frms = {}):
            frm = []
            for j in header:
                value = line[j] if line else j
                size = columns[j] if columns.get(j) else 50
                if line and frms and frms.get(j):
                    value = frms[j](value)
                frm.append(('{:^{}}').format(value, size))
            st = '|{:^5}|'.format(num if num else '#') + '|'.join(frm) + '|'
            print('–'*len(st), st, sep='\n')
            return '–'*len(st)

        try:
            k = 0
            d = []
            header = False
            footer = False
            for i in data:
                if not header:
                    header = list(i.keys())
                    if idd not in header: idd = None
                    prn(header, columns, frms=frm)
                k += 1
                if idd: d += [i[idd]]
                footer = prn(header, columns, i, k, frms=frm)
            if footer:
                print(footer)
                print()
            return d
        except Exception as ex:
            logging.error('Невозможно показать список %s', ex)
            return []

    def sqlWheather(self, **kwargs):
        flt = {}
        fld = ['c.name as "Город", cn.name as "Страна", w.temp as "Температура", w.dt as "Дата"']
        sql = ['FROM wheather as w INNER JOIN cities as c ON c.id = w.city_id']
        if kwargs.get('favorite'):
            sql += ['AND c.favorite = 1']
        sql += ['INNER JOIN countries as cn ON cn.code = c.country']
        if not kwargs.get('export'):
            sql += ['GROUP BY w.city_id']
        sql += ['ORDER BY w.dt DESC']
        return (" ".join(sql), ",".join(fld), flt)

    def exportWheather(self, city=None):
        cnt = 0
        cur = None
        params = {'city': city}
        sql = ['FROM wheather as w INNER JOIN cities as c ON c.id = w.city_id']
        if city:
            sql += ['AND c.name LIKE :city']
        sql += ['INNER JOIN countries as cn ON cn.code = c.country']
        sql += ['ORDER BY c.id ASC, w.dt DESC']
        count = f'SELECT COUNT(*) as cnt {" ".join(sql)}'
        select = f'SELECT c.id, c.name as city, cn.name as country, w.temp, w.dt, w.wheather_id, w.wheather {" ".join(sql)}'

        try:
            cnt = int(self.db.select(count, params).fetchone()['cnt'])
            if cnt > 0:
                cur = self.db.select(select, params)
        except Exception as ex:
            logging.error('Ошибка получения данных погоды %s', ex)

        return (cnt, cur)

    def wheather(self, **kwargs):
        sql, fld, flt = self.sqlWheather(**kwargs)
        return self.db.select(f'SELECT {fld} {sql}', flt)

    def updateWheather(self, **kwargs):
        if not self.api.api_id:
            print('Ключ не установлен, попробуйте получить через интерактивный режим -interactive')
            return 0
        def ob(o):
            dt = datetime.fromtimestamp(o['dt'])
            dt = int(datetime(dt.year, dt.month, dt.day).timestamp())
            r = [o['id'], dt, o['main']['temp'], o['weather'][0]['id'], pickle.dumps(o)]
            return r

        ids = [i['id'] for i in self.db.select(
            "SELECT id FROM cities WHERE favorite = 1")]
        total = 0
        print(f'Обновляем погоду для {len(ids)} городов...', end='')
        for i in range(0, len(ids), 20):
            lst = ids[i:20+i]
            lst = self.api(lst)
            if lst == False:
                print('...ошибка')
                return total
            lst = list(map(ob, lst))
            self.db.bulk("INSERT OR REPLACE INTO wheather VALUES (?,?,?,?,?)", lst)
            total += len(lst)
        print('...готово')
        return total

    def printCities(self):
        lst = self.cities(favorite=1, limit=None)
        a = self.printList(lst, {'id': 10, 'name': 50, 'country': 50, 'saved': 5})
        print('Не найдено сохраненных городов' if not len(a) else '')
        return False

    def wheatherList(self, **kwargs):
        def mm(a):
            try:
                tm = datetime.fromtimestamp(int(a))
                a = tm.strftime('%Y-%m-%d')
                return a
            except:
                return a

        lst = self.wheather(**kwargs)
        lst = self.printList(
            lst, {'Температура': 15, 'Дата': 20}, 'Город', {'Дата': mm})
        if not len(lst):
            print('\tнет сохраненной погоды попробуйте обновить')
        return False

    def interactive(self, params):
        'интерактивный режим'

        def print_menu(menu, default = 0):
            print('\t0. <<<< выход')
            print(*[f'\t{i+1}. {menu[i]}' for i in range(len(menu))], sep='\n')
            try:
                ask = int(input(f'   Выберите вариант [{default} - enter]:'))
                print()
            except:
                ask = default
            if 0 >= ask > len(menu):
                ask = default
            return ask

        def api():
            print('\nУправление API ключом - API ключ: ' + (self.api.api_id if self.api.api_id else 'НЕ УСТАНОВЛЕН:'))
            a = print_menu(['установить вручную', 'получить через логин/пароль'])
            if not a:
                return False
            elif a==1:
                self.api.api_id = input('\tВведите API ID:')
            elif a==2:
                key = API.grabApiId(input('\tВведите username:'), input('\tВведите password:'))
                self.api.api_id = key
            return True

        def level():
            print('\nУправление уровнем логирования - LEVEL: ' + logging.getLevelName(logging.getLogger().level))
            levels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
            a = print_menu(levels)
            if not a:
                return False
            self.setupLogging(levels[a-1])
            return True

        def askRange(message, idd):
            def bound(i, mx):
                r = int(i)-1
                if r < 0: r = 0
                if r > mx: r = mx
                return r

            ids = []
            ask = input(message).split()
            print()
            for i in ask:
                try:
                    i = i.split('-')
                    a = bound(i[0], len(idd))
                    if len(i) == 1:
                        b = a + 1
                    else:
                        b = bound(i[1], len(idd)) + 1
                    if a >= b: b = a + 1
                except:
                    continue
                ids += idd[a:b]
            return ids

        def askAddCity():
            page = 0
            total = set()
            country = input('\tВведите фильтр по стране [пусто - нет фильтра - все страны]:').strip()
            city = input('\tВведите фильтр по городу [пусто - нет фильтра - все города]:').strip()
            if len(city)<2 and len(country)<2:
                print('Введите хотя бы 2 буквы страны или города')
                return 0
            city = f'%{city}%' if city else None
            country = f'%{country}%' if country else None
            cnt = self.countCities(city=city, country=country)
            if cnt > 0:
                print(f'\nВсего найдено {cnt} городов')
            else:
                print('Ничего не найдено, попробуйте другой фильтр')

            while cnt:
                print(f'\nСтраница {page+1} из {cnt // 20}, фильтр по ГОРОД: [{city}], СТРАНА: [{country}]')
                lst = self.cities(city=city, country=country, page=page)
                ids = self.printList(lst, {'id': 10, 'saved': 5})
                menu = ['выбрать в буфер', f'сохранить буфер [{len(total)} городов] и выйти',  f'очистить буфер',
                        f'сохранить все [{cnt} городов] и выйти']
                if cnt > 0:
                    if page < cnt//20: menu += ['> вперед']
                    if page > 0: menu += ['< назад']

                print(f'\nВсего в буфере {len(total)} городов')
                a = print_menu(menu, 5 if cnt//20 else 0)
                if a == 5: page += 1
                elif a == 6: page -= 1
                elif a == 1:
                    ids = askRange('   Выберите города - можно вводить range (например 1 2 3-10) :', ids)
                    for i in ids: total.add(i)
                    if len(ids) > 0: print(f'\nДобавлено {len(ids)} городов')
                elif a == 2:
                    if len(total) > 0:
                        self.cities_count = self.setCities(1, ids=list(total))
                    print(f'\n>>> Добавлено {len(total)} городов')
                    return False
                elif a == 3:
                    total.clear()
                    print("Буфер очищен")
                elif a == 4:
                    self.cities_count = self.setCities(1, city=city, country=country)
                    print(f'\n>>> Добавлено {cnt} городов')
                    return False
                else: return False

        def askDelCity():
            page = 0
            if self.cities_count > 0:
                print(f'\nВсего {self.cities_count} сохраненных городов')
            else:
                print('Нет сохраненных городов')

            while self.cities_count:
                print(f'\nВсего {self.cities_count} сохраненных городов')
                print(f'\nСтраница {page+1} из {self.cities_count // 20}')
                lst = self.cities(favorite=1, page=page)
                ids = self.printList(lst, {'id': 10, 'saved': 5})
                menu = ['выбрать определенные и удалить', f'удалить все']
                if self.cities_count > 0:
                    if page < self.cities_count//20:
                        menu += ['> вперед']
                    if page > 0:
                        menu += ['< назад']

                a = print_menu(menu, 3 if self.cities_count//20 else 0)
                if a == 3:
                    page += 1
                elif a == 4:
                    page -= 1
                elif a == 1:
                    ids = askRange('   Выберите города - можно вводить range (например 1 2 3-10) :', ids)
                    if len(ids) > 0:
                        self.cities_count = self.setCities(0, ids=list(ids))
                        print(f'\n>>> Удалено {len(ids)} городов')
                        if not self.cities_count:
                            print('\nБольше нет сохраненных городов')
                            return False
                elif a == 2:
                    self.cities_count = self.setCities(0)
                    print('\nВсе cохраненные города удалены')
                    return False
                else: return False

        def wheatherUpdate():
            print('>'*20 + f' ОБНОВЛЕНО {self.updateWheather()} ГОРОДОВ\n')
            print('Последняя сохраненная погода по городам:')
            self.wheatherList(favorite=True)
            return False

        menu = [api, level, self.wheatherList, askAddCity,
                wheatherUpdate, self.printCities, askDelCity]
        while True:
            print("{:-^50}".format(' Главное меню '))
            print('   API ключ: ' + (self.api.api_id if self.api.api_id else 'НЕ УСТАНОВЛЕН:'))
            print('   LOGLEVEL: ' + logging.getLevelName(logging.getLogger().level))
            print(f'   Количество добавленных городов: {self.cities_count}')
            print("-"*50)
            mm = ['Управление API ID', 'Управление LOG LEVEL',
                  'Посмотреть ВСЮ сохраненную погоду']
            if self.api.api_id:
                mm += ['Поиск и добавление города']
                if self.cities_count:
                    mm += ['Получить погоду для добавленных городов', 'Показать список городов',
                           'Удалить города из списка']
            a = print_menu(mm)
            if not a: break
            while menu[a-1](): pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='"%(prog)s" скрипт для получения погоды для города с помощью OpenWheatherAPI',
        usage='%(prog)s [-interactive]',
        prefix_chars='-')

    parser.add_argument('-list', action='count',help="показать список городов")
    parser.add_argument('-id', action='append',help="добавить город по ID")
    parser.add_argument("-search", help="Поиск города -search city=mos -search country=russ",
               action="append",
               type=lambda kv: dict([i.split('=')for i in kv.split(" ")]))
    parser.add_argument('-last', action='count', help="показать последнюю сохраненную погоду")
    parser.add_argument('-all', action='count', help="показать всю сохраненную погоду")
    parser.add_argument('-download', action='count', help="скачать актуальную погоду для сохраненных городов")
    parser.add_argument('-interactive', action='count', help="переходит в интерактивный режим")
    parser.add_argument('-api_id', action='store', type=str, help="можно установить свой API_ID для API")
    parser.add_argument('-log', action='store', type=str, default='error',
                        help="уровень логирования [debug, warning, error - по умолчанию]")
    parser.add_argument('-db', action='store', type=str, default='database.db',
                        help="файл БД по умолчанию 'database.db'")

    p = parser.parse_args()

    main = Wheather(p.db, p.api_id, p.log)
    if p.interactive:
        main.interactive(p)
    elif p.list:
        main.printCities()
    elif p.search:
        flt = {k: v for items in p.search for k, v in items.items()}
        city=flt.get('city', None)
        country=flt.get('country', None)
        cnt = main.countCities(city=city, country=country)
        if cnt > 0:
            print(f'\nВсего найдено {cnt} городов')
        else:
            print('Ничего не найдено, попробуйте другой фильтр')

        lst = main.cities(city=city, country=country)
        main.printList(lst, {'id': 10, 'saved': 5})
    elif p.download:
        cnt = main.updateWheather()
        if cnt:
            print('Последняя сохраненная погода по выбранным городам:')
            main.wheatherList(favorite=1)
    elif p.id:
        main.cities_count = main.setCities(1, ids=list(p.id))
        print(f'Добавлено {len(p.id)} городов')
    elif p.all:
        print('Вся сохраненная погода:')
        main.wheatherList(export=True)
    elif p.last:
        print('Вся последняя сохраненная погода:')
        main.wheatherList()
    else:
        parser.print_help()
        pass
