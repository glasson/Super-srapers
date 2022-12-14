from parsers import *
from os import makedirs
from datetime import datetime
import csv

# rts, zakupki360, roseltorg, synapsenet, rad, fabricant
PARSERS_LIST = [rts, zakupki360, roseltorg, synapsenet, rad, fabricant]
DOWNLOADING_DOCS = False


def creating_csv(dir_path):
    with open('{}\\purchases.csv'.format(dir_path), "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(FIELDS_NAME)


def get_amount_tenders(dir_path):
    with open('{}\\purchases.csv'.format(dir_path), "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        return len(list(reader)) - 1


def main():
    search_query = input('Введите ключевое слово: ')
    print("\nТендеры:")

    now = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    dir_path = f'data/{search_query}_{now}'
    makedirs(dir_path, exist_ok=True)

    creating_csv(dir_path)

    for parser in PARSERS_LIST:
        try:
            parser(search_query, dir_path, DOWNLOADING_DOCS)
        except:
            continue

    print("\nВсего тендеров:", get_amount_tenders(dir_path))


if __name__ == '__main__':
    main()


