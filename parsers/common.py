import csv


FIELDS_DATA = {
    'tender_number': 'Номер тендера',
    'object': 'Объект',
    'order': 'Закон',
    'tender_type': 'Вид',
    'start_value': 'Начальная сумма',
    'start_date': 'Дата размещений',
    'end_date': 'Дата окончания',
    'tender_status': 'Статус заявки',
    'customers': 'Организация',
    'documents': 'Документы'
}

FIELDS = list(FIELDS_DATA.keys())
FIELDS_NAME = list(FIELDS_DATA.values())


def write_data(data, dir_path):
    with open(f'{dir_path}/purchases.csv', 'a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(list(data.values()))
