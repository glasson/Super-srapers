import requests
from bs4 import BeautifulSoup
from os import makedirs

from .common import write_data

host = 'https://www.etp-ets.ru/'
url1 = '223/catalog/procedure'
url2 = '44/catalog/procedure'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def get_html(url, params=''):
    return requests.get(url, headers=HEADERS, params=params)


def get_content_url2(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('tbody').find_all('tr')
    purchase = []
    for item in items:
        purchase.append(
            {
                'id_purchase': item.find('td', class_='row-procedure_name').get_text().rsplit(' ', 1)[1].replace('(', '').replace(')', ''),
                'title': item.find('td', class_='row-procedure_name').get_text(),
                'order': '44',
                'type': '',
                'start_price': item.find('td', class_='row-contract_start_price').get_text(),
                'date_publication': item.find('td', class_='row-publication_datetime').get_text(),
                'date_end': item.find('td', class_='row-request_end_give_datetime').get_text(),
                'status': item.find('td', class_='row-status').get_text(),
                'customer': item.find('td', class_='row-customer_name').get_text(strip=True),
                'documentation': item.find('td', class_='row-procedure_name').find('a').get('href').split('?&')[0].replace('procedure', 'documentation')
            }
        )
    return purchase

def get_content_url1(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('tbody').find_all('tr')
    purchase = []
    for item in items:
        purchase.append(
            {
                'id_purchase': item.find('td', class_='row-procedureName').get_text().rsplit(' ', 1)[1].replace('(', '').replace(')', ''),
                'title': item.find('td', class_='row-procedureName').get_text(),
                'order': '223',
                'type': '',
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
    return pages, elements


def save_doc(url_documentation, name, path):
    html = get_html(url_documentation)
    soup = BeautifulSoup(html.text, 'html.parser')
    documentation = soup.find_all('p', class_='upload-filename')
    docs = []
    for doc in documentation:
        docs.append({
            'name': doc.find('a').text,
            'doca': doc.find('a').get('href')
        })
    makedirs(f'{path}/{name}', exist_ok=True)
    for doc in docs:
        try:
            a = get_html(doc['doca']).content
            with open(f'{path}/{name}/{doc["name"]}', 'wb') as file:
                file.write(a)
        except:
            continue


def fabricant(key_word, dir_path):
    print("Парсим etp-ets.ru")
    html1 = get_html(host + url1, params={'q': key_word})
    html2 = get_html(host + url2, params={'q': key_word})

    items = []

    pages, _ = get_pages(html1.text)
    for p in range(1, pages + 1):
        html = get_html(host + url1, params={'q': key_word, 'page': p})
        items.extend(get_content_url1(html.text))

    pages, _ = get_pages(html2.text)
    for p in range(1, pages + 1):
        html = get_html(host + url2, params={'q': key_word, 'page': p})
        items.extend(get_content_url2(html.text))


    for item in items:
        write_data(item, dir_path)
        save_doc(item['documentation'], item['id_purchase'], dir_path)


if __name__ == "__main__":
    search_query = input('Введите название тендера: ')
    dir_path = f'data/{search_query}'
    fabricant(search_query, dir_path)
