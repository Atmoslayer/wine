import datetime
import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


def define_year_word_ending(year_number):

    if year_number >= 100:
        year_number = year_number % 100

    if year_number in range(11, 15):
        year_word = 'лет'

    elif year_number % 10 == 1:
        year_word = 'год'
    elif year_number % 10 in range(2, 5):
        year_word = 'года'
    else:
        year_word = 'лет'

    return year_word


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

year_of_foundation = datetime.datetime(year=1920, month=1, day=1, hour=0).year
current_year = datetime.datetime.now().year
year_number = current_year - year_of_foundation

excel_data = pandas.read_excel('wine3.xlsx', na_values=' ', keep_default_na=False,
                                   usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'])
wines = excel_data.to_dict(orient='records')

formatted_wines = {}

for wine in wines:
    formatted_wines.setdefault(wine['Категория'], []).append(wine)

rendered_page = template.render(wines=formatted_wines, year_info=f'Уже {year_number} {define_year_word_ending(year_number)} с вами!')


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

