import argparse
import http.server
import socketserver
import datetime
import pandas


from jinja2 import Environment, FileSystemLoader, select_autoescape


PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

Handler.extensions_map = {
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg':  'image/svg+xml',
        '.css':  'text/css',
        '.js':  'application/x-javascript',
        '': 'application/octet-stream'
    }


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


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--enter', help='Enter database file path', default='wine.xlsx')
    argument = parser.parse_args()
    filepath = argument.enter

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    year_of_foundation = 1920
    current_year = datetime.datetime.now().year
    year_number = current_year - year_of_foundation

    with open(filepath, 'r') as file:

        parsed_excel = pandas.read_excel(io=file.name, na_values=' ', keep_default_na=False, usecols=['Категория',
                                                                                                      'Название',
                                                                                                      'Сорт',
                                                                                                      'Цена',
                                                                                                      'Картинка',
                                                                                                      'Акция'])

    wines = parsed_excel.to_dict(orient='records')

    formatted_wines = {}

    for wine in wines:
        formatted_wines.setdefault(wine['Категория'], []).append(wine)

    year_title = f'Уже {year_number} {define_year_word_ending(year_number)} с вами!'
    rendered_page = template.render(wines=formatted_wines,
                                    year_title=year_title)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    server.serve_forever()