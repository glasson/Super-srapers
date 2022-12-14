import csv


def write_data(data, dir_path):
    with open(f'{dir_path}/purchases.csv', 'a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data.values())
