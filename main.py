from parsers import *
from os import makedirs
from datetime import datetime
import csv

# rts, zakupki360, roseltorg, synapsenet, rad
# fabricant
parsers_list = [rts, zakupki360, roseltorg, synapsenet, rad]


def creating_csv(dir_path):
    with open('{}\\purchases.csv'.format(dir_path), "w", encoding="utf-8", newline='') as data_file:
        writer = csv.writer(data_file, delimiter=';')
        writer.writerow(
            ("Номер", "Объект закупки", "Закон", "Вид", "Начальная цена", "Дата размещения", "Дата окончания тендера",
             "Статус", "Заказчик", "Документация"))


def main():
    search_query = input('Введите ключевое слово: ')

    now = datetime.now().strftime("%d%m%Y%H%M%S")
    dir_path = f'data/{search_query}_{now}'
    makedirs(dir_path, exist_ok=True)

    creating_csv(dir_path)

    for parser in parsers_list:
        try:
            parser(search_query, dir_path)
        except:
            continue


if __name__ == '__main__':
    main()


