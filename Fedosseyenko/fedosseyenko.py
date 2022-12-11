import csv
import time

import requests
from bs4 import BeautifulSoup

headers = {'Accept-Language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
           "accept": "*/*",
           "accept-encoding": "gzip, deflate, br",
           "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
           "cache-control": "no-cache",
           "Connection": "keep-alive",
           'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}


def write_data(data, timestr):
    with open('{}.csv'.format(timestr), 'a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data.values())
        file.close()


def creating_csv(timestr):
    with open('{}.csv'.format(timestr), "w", encoding="utf-8", newline='') as data_file:
        writer = csv.writer(data_file, delimiter=';')
        writer.writerow(
            ("Название", "Номер", "Закон", "Вид", "Начальная цена", "Дата размещения", "Дата окончания тендера",
             "Статус",
             "Объект закупки", "Заказчик"))
    data_file.close()


def parsing_table(soup):
    data = []
    data_objects = []
    try:
        table = soup.find("table")
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        data.pop(0)
        for item in data:
            for objects in item:
                data_objects.append(objects)
                break
        return data_objects
    except AttributeError:
        return "No data"



def parsing_data(soup, timestr):
    order = "Order undefined"
    delim = ','
    data_parse = []
    tender_status = soup.find("div", class_='status')
    tender_name = soup.find("h1", class_='dossier__title').text
    start_date = soup.find("div", class_='dossier__column data').get_text().replace("Размещено:", "")
    end_date = soup.find("meta", itemprop='endDate')["content"]
    if end_date.isspace():
        end_date = 'undefined'
    customers = soup.find("a", class_='dossier__column data link')  # Заказчик
    info_data = soup.find("div", class_='dossier__info').find("div", class_='dossier__info-column').find_next("div",
                                                                                                              class_='dossier__info-column').findAll(
        "div", class_="data info__data")
    start_value = soup.find("div", class_='data info__data').text
    for info in info_data:  # Номер закупки / Способ размещения / Площадка
        info = info.text
        data_parse.append(info)
    info = soup.find('div', class_='data info__data ng-star-inserted').find("span")
    if info.text.__contains__("(223-ФЗ)"):
        order = "223-ФЗ"
    elif info.text.__contains__("(44-ФЗ)"):
        order = "44-ФЗ"
    purchase_object = delim.join(parsing_table(soup))
    data = {
        "tender_name": tender_name,
        "tender_number": data_parse[0],
        "order": order,
        "tender_type": data_parse[1],
        "start_value": start_value.replace('\xa0', '').strip(),
        "start_date": start_date,
        "end_date": end_date,
        "tender_status": tender_status.text,
        "purchase_object": purchase_object.strip(),
        "customers": customers.text
    }
    write_data(data, timestr)


def parse():
    count = 0
    timestr = time.strftime("%Y%m%d-%H%M%S")
    creating_csv(timestr)
    for i in range(1, 3):
        page = "&page={}".format(i)
        query = '{}{}'.format(input("Введите запрос\n"), page)
        links = get_links(query)
        for link in links:
            count += 1
            url = "https://zakupki360.ru{}".format(link)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            parsing_data(soup, timestr)
            print("Запарсено страниц: {}".format(count))


def get_links(query):
    url = "https://zakupki360.ru/search?query={}".format(query)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    links_content = soup.find("div", class_="card-container ng-star-inserted").findAll("div",
                                                                                       class_="content__content")
    links = []
    for link in links_content:
        link = link.find_next("a", class_="app-passive-link")
        links.append(link["href"])
    return links

def main():
    parse()


if __name__ == "__main__":
    main()
