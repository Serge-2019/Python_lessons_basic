
""" OpenWeatherMap (экспорт)

Сделать скрипт, экспортирующий данные из базы данных погоды,
созданной скриптом openweather.py. Экспорт происходит в формате CSV или JSON.

Скрипт запускается из командной строки и получает на входе:
    export_openweather.py --csv filename [<город>]
    export_openweather.py --json filename [<город>]
    export_openweather.py --html filename [<город>]

При выгрузке в html можно по коду погоды (weather.id) подтянуть
соответствующие картинки отсюда:  http://openweathermap.org/weather-conditions

Экспорт происходит в файл filename.

Опционально можно задать в командной строке город. В этом случае
экспортируются только данные по указанному городу. Если города нет в базе -
выводится соответствующее сообщение.

"""

import csv
import json
import argparse
import pickle
from datetime import datetime
from openweather import Wheather

class Formatter:
    'Базовый форматер'

    def __init__(self, data):
        self.data = cur
        self.head = None

    def __str__(self):
        rows = []
        for row in self.data:
            if not self.head:
                self.head = row.keys()
            fields = [self.field(row[i], self.head[i]) for i in range(len(row))]
            rows.append(self.row(fields))
        return self.header + self.sep.join(rows) + self.footer

    def field(self, field, hdr):
        if hdr == 'dt':
            item = datetime.fromtimestamp(field).strftime('%Y-%m-%d')
        elif hdr == 'wheather':
            item = pickle.loads(field)
        else:
            item = field
        return item

    def row(self, fields):
        return ','.join(fields)

    @property
    def sep(self):
        return '\n'

    @property
    def header(self):
        return ''

    @property
    def footer(self):
        return ''

class CSVFormatter(Formatter):
    'CSV'

    def quote(self, data = []):
        def prp(x):
            x = str(x)
            if x.find('"') >=0:
                x = '"' + x.replace('"', r'\"') + '"'
            if x.find('\n') >= 0:
                x = '"' + x.replace('\n', r'\n') + '"'
            return x
        return ",".join([prp(i) for i in data]) if data and type(data) == list else ''

    def row(self, fields):
        return self.quote(fields[0:len(fields)-1])

    @property
    def header(self):
        return self.quote(['ID', 'Город', 'Страна', 'Температура', 'Дата', 'ID Погоды']) + "\n"



class JSONFormatter(Formatter):
    'JSON'

    def row(self, fields):
        d = {k[0]:k[1] for k in list(zip(self.head, fields))}
        return json.dumps(d)

    @property
    def header(self):
        return "[\n"

    @property
    def footer(self):
        return "\n]"

    @property
    def sep(self):
        return ",\n"

class HTMLFormatter(Formatter):
    'HTML'

    def row(self, fields):
        wh = fields[6]['weather'][0]
        whh = '<img src="http://openweathermap.org/img/w/' + wh['icon']+'.png" alt='+wh['description']+'/><br/>'
        whh += '<b>'+wh['description']+'</b>'
        lst = [whh, fields[1], fields[2], fields[3], fields[4]]
        return '<td>' + '</td><td>'.join(map(str, lst)) + '</td>'

    @property
    def header(self):
        return """<!DOCTYPE html>
        <html lang="en">
        <head>
          <title>Экспорт погоды</title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.0/js/bootstrap.min.js"></script>
        </head>
        <body>

        <div class="container">
          <h2>Экспорт погоды</h2>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>Погода</th>
                <th>Город</th>
                <th>Страна</th>
                <th>Температура</th>
                <th>Дата обновления</th>
              </tr>
            </thead>
            <tbody>
              <tr>"""

    @property
    def footer(self):
        return """</tr>
            </tbody>
          </table>
        </div>
        </body>
        </html>
        """

    @property
    def sep(self):
        return "</tr>\n<tr>"


parser = argparse.ArgumentParser(
    description='"%(prog)s" скрипт для экспорта данных и БД погоды',
    usage='%(prog)s --csv|json|html filename [<city>] [--debug]',
    prefix_chars='--')

parser.add_argument('filename', action='store',
                    help="имя файла для экспорта")
parser.add_argument('city', nargs='?', default=None, help="город погоду которого нужно экспортировать, если не указан то все")
parser.add_argument('--csv', action='count',
                    help="экспорт в формате CSV (по умолчанию)")
parser.add_argument('--json', action='count',
                    help="экспорт в формате JSON")
parser.add_argument('--html', action='count',
                    help="экспорт в формате HTML")
parser.add_argument('--debug', action='count',
                    help="debug режим, вывод сообщений о процессе")

try:
    p = parser.parse_args()
except:
    parser.print_help()
    p = False

if p:
    fmt = CSVFormatter
    if p.json:
        fmt = JSONFormatter
    elif p.html:
        fmt = HTMLFormatter

    main = Wheather(loglevel='DEBUG' if p.debug else 'ERROR')
    cnt, cur = main.exportWheather(p.city)
    if not cnt:
        print('Погода в БД не найдена')
    else:
        ct = f'о городе {p.city} ' if p.city else ''
        print(f'Экспортируем {cnt} записей {ct}в формате {fmt.__doc__} в файл {p.filename}')
        try:
            with open(p.filename, 'w', encoding='UTF-8') as f:
                f.write(str(fmt(cur)))
            print('Файл успешно сохранен')
        except:
            print('Невозможно открыть файл для записи')
            raise

