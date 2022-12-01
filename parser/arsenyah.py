import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil

host = 'https://www.etp-ets.ru/'
url1 = '223/catalog/procedure'
url2 = '44/catalog/procedure'
# url3 = 'catalog/procedure'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content_url2(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('tbody').find_all('tr')
    # print(items)
    purchase = []
    for item in items:
        purchase.append(
            {
                'title': item.find('td', class_='row-procedure_name').get_text(),
                'id_purchase': item.find('td', class_='row-procedure_name').get_text().rsplit(' ', 1)[1].replace('(', '').replace(')', ''),
                'url_purchase': item.find('td', class_='row-procedure_name').find('a').get('href').split('?&')[0],
                'start_price': item.find('td', class_='row-contract_start_price').get_text(),
                'customer': item.find('td', class_='row-customer_name').get_text(strip=True),
                'date_publication': item.find('td', class_='row-publication_datetime').get_text(),
                'date_end': item.find('td', class_='row-request_end_give_datetime').get_text(),
                'status': item.find('td', class_='row-status').get_text(),
                'documentation': item.find('td', class_='row-procedure_name').find('a').get('href').split('?&')[0].replace('procedure', 'documentation')
            }
        )
    return purchase

def get_content_url1(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('tbody').find_all('tr')
    # print(items)
    purchase = []
    for item in items:
        purchase.append(
            {
                'title': item.find('td', class_='row-procedureName').get_text(),
                'id_purchase': item.find('td', class_='row-procedureName').get_text().rsplit(' ', 1)[1].replace('(', '').replace(')', ''),
                'url_purchase': item.find('td', class_='row-procedureName').find('a').get('href').split('?&')[0],
                'start_price': item.find('td', class_='row-contractStartPrice').get_text(),
                'customer': item.find('td', class_='row-customerName').get_text(strip=True),
                'date_publication': item.find('td', class_='row-publicationDateTime').get_text(),
                'date_end': item.find('td', class_='row-requestEndGiveDateTime').get_text(),
                'status': item.find('td', class_='row-lotStatusId').get_text(),
                'documentation': item.find('td', class_='row-procedureName').find('a').get('href').split('?&')[0].replace('procedure', 'documentation')
            }
        )
    return purchase


def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='input-group pull-right mte-grid-pageLimiter')
    elements = int(items[0].find('span', class_='input-group-addon').get_text().split(': ')[1])
    pages = 0
    if elements % 10 != 0:
        pages = int(elements / 10) + 1
    else:
        pages = int(elements / 10)
    # print(f'колво элементов: {elements}')
    # print(f'колво страниц: {pages}')
    return pages, elements


def save_doc(url_documentation, path):
    html = get_html(url_documentation)
    soup = BeautifulSoup(html.text, 'html.parser')
    documentation = soup.find_all('p', class_='upload-filename')
    docs = []
    for doc in documentation:
        docs.append({
            'name': doc.find('a').text,
            'doca': doc.find('a').get('href')
        })
    print(docs)
    for doc in docs:
        a = get_html(doc['doca']).content
        with open(f'{path}/{doc["name"]}', 'wb') as file:
            file.write(a)



def save_csv(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование заказа', 'id заказа', 'Ссылка на заказ', 'Начальная цена', 'Заказчик',
                         'Дата публикации', 'Дата закрытия заказа', 'Статус заказа'])
        for item in items:
            writer.writerow([item['title'], item['id_purchase'], item['url_purchase'],
                             item['start_price'], item['customer'],
                             item['date_publication'], item['date_end'], item['status']])

def parser():
    key_word = input('Задайте ключевое слово по которому будут искать все заказы: ')
    html1 = get_html(host + url1, params={'q': key_word})
    html2 = get_html(host + url2, params={'q': key_word})
    if html1.status_code != 200:
        print('error')
        return
    if html2.status_code != 200:
        print('error')
        return
    while(True):
        try:
            os.mkdir(key_word)
            os.mkdir(f'{key_word}/223')
            os.mkdir(f'{key_word}/44')
            break
        except Exception as e:
            print('папка с таким названием уже существует')
            while(True):
                n = input('пересоздать ?(y/n): ')
                if n == 'y':
                    shutil.rmtree(key_word)
                    os.mkdir(key_word)
                    os.mkdir(f'{key_word}/223')
                    os.mkdir(f'{key_word}/44')
                    break
                elif n == 'n':
                    return
                else:
                    print('Неверный ввод, попробуйте ещё раз')
            break
    items223 = []
    items44 = []
    pages, elements = get_pages(html1.text)
    print(f'По вашему запросу нашлось:\n'
          f'{elements} заказов\n'
          f'{pages} страниц с заказами')
    page = 0
    flag1 = 0
    flag2 = 0
    while(True):
        if pages < 1:
            print('по вашему запросу ничего не нашлось')
            flag1 = 1
            break
        page = int(input(f'укажите кол-во страниц для парсинга (1 - {pages}): '))
        if (page > pages) or (page < 1):
            print('Неверный ввод, попробуйте ещё раз')
        else:
            break
    if flag1 == 0:
        for p in range(1, page+1):
            print(f'парсим страницу: {p}')
            html = get_html(host + url1, params={'q': key_word, 'page': p})
            items223.extend(get_content_url1(html.text))

    pages, elements = get_pages(html2.text)
    print(f'По вашему запросу нашлось:\n'
          f'{elements} заказов\n'
          f'{pages} страниц с заказами')
    page = 0
    while (True):
        if pages < 1:
            print('по вашему запросу ничего не нашлось')
            flag2 = 1
            break
        page = int(input(f'укажите кол-во страниц для парсинга (1 - {pages}): '))
        if (page > pages) or (page < 1):
            print('Неверный ввод, попробуйте ещё раз')
        else:
            break
    if flag2 == 0:
        for p in range(1, page + 1):
            print(f'парсим страницу: {p}')
            html = get_html(host + url2, params={'q': key_word, 'page': p})
            items44.extend(get_content_url2(html.text))

    if flag1 == 0:
        CSV = f'{key_word}/223/purchase.csv'
        save_csv(items223, CSV)
        for item in items223:
            name = key_word + '/223/' + item['id_purchase']
            os.mkdir(name)
            save_doc(item['documentation'], name)

    if flag2 == 0:
        CSV = f'{key_word}/44/purchase.csv'
        save_csv(items44, CSV)
        for item in items44:
            name = key_word + '/44/' + item['id_purchase']
            os.mkdir(name)
            save_doc(item['documentation'], name)


    # print(page)
    # print(pages)

parser()
# a = requests.get('https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68520271').content
# with open('Приложение №2 к ЗД_Заявка на участие_Ценовое_предложение.xlsx', 'wb') as file:
#     file.write(a)
# print(url2.split("/")[0])


# html = get_html(url)
# print(html)
# get_pages(html.text)
# print(get_content(html.text))


