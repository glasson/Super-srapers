import csv
import time
from random import choice
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

querystring = {"sale": "0", "query_fiel": "Поставка", "status^%^5B^%^5D": ["5", "0"], "currency": "all", "page": 1}
desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

payload = ""


def change_useragent():
    return {
        "authority": "www.roseltorg.ru",
        "accept": "*/*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "cookie": "utmz_main_domain=111127430.1670778218.1.1.utmcsr^%^3D^%^28direct^%^29^%^7Cutmccn^%^3D^%^28direct^%^29^%^7Cutmcmd^%^3D^%^28none^%^29; _ym_uid=1667392902912253966; _ym_d=1667392902; _ga=GA1.2.965244.1670778218; __utmz=111127430.1670778218.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=(none); mindboxDeviceUUID=3ea71f71-fd76-422a-99ae-3c19903eaffb; directCrm-session=^%^7B^%^22deviceGuid^%^22^%^3A^%^223ea71f71-fd76-422a-99ae-3c19903eaffb^%^22^%^7D; flocktory-uuid=04f1b92a-3ff4-41ab-8d84-51725fc5084a-8; _ymab_param=ql2H3pRbBko1aJ9GhLTTURdzsvE8p^%^2Bp8JPXeYlsL^%^2FDsR6uEmhwNOPAEpZ3qQKwa0U7XUDCG3GKM7CVA^%^2Fv80UiCLJyOc^%^3D; popmechanic_sbjs_migrations=popmechanic_1418474375998^%^3D1^%^7C^%^7C^%^7C1471519752600^%^3D1^%^7C^%^7C^%^7C1471519752605^%^3D1; cert_c=6; 11a0d84ae2472a9dff73ec72bf9debbe=f36070891548321379c59197868ceea5; __utma=111127430.965244.1670778218.1670865789.1671017837.5; __utmc=111127430; __utmt_UA-139161005-1=1; _gid=GA1.2.1915009722.1671017837; utmz_main_domain=111127430.1670778218.1.1.utmcsr^%^3D^%^28direct^%^29^%^7Cutmccn^%^3D^%^28direct^%^29^%^7Cutmcmd^%^3D^%^28none^%^29; _ym_visorc=w; _ym_isad=1; googtrans=null; googtrans=null; __utmb=111127430.3.10.1671017837",
        "pragma": "no-cache",
        "referer": "https://www.roseltorg.ru/procedures/search?sale=0&query_field=^%^D1^%^80^%^D0^%^B0^%^D0^%^B7^%^D1^%^80^%^D0^%^B0^%^D0^%^B1^%^D0^%^BE^%^D1^%^82^%^D0^%^BA^%^D0^%^B0&status^%^5B^%^5D=5&status^%^5B^%^5D=0&currency=all",
        "sec-ch-ua": "^\^Not?A_Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^108^^, ^\^Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": choice(desktop_agents),
        "x-requested-with": "XMLHttpRequest"
    }


def write_data(data, time_str):
    with open('{}.csv'.format(time_str), 'a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data.values())
        file.close()


def creating_csv(time_str):
    with open('{}.csv'.format(time_str), "w", encoding="utf-8", newline='') as data_file:
        writer = csv.writer(data_file, delimiter=';')
        writer.writerow(
            ("Название", "Номер", "Закон", "Вид", "Начальная цена", "Дата размещения", "Дата окончания тендера",
             "Статус",
             "Объект закупки", "Заказчик"))
    data_file.close()


def parsing_data(soup, time_str):
    try:
        tender_name = soup.find("table",
                                class_="data-table data-table--header description__data-table description__data-table--header").find(
            "p", class_="data-table__info").text
    except AttributeError:
        tender_name = "ParseError"
    try:
        tender_number = soup.find("div", class_="description__heading").find("h1",
                                                                         class_='description__main-header main-header').text.replace(
        "Процедура:", "").strip()
    except AttributeError:
        tender_number = "ParseError"
    try:
        start_date = soup.find("div", class_='steps__description').text
    except AttributeError:
        start_date = "ParseError"
    try:
        end_date = soup.find("time", class_="lot-item__time").text.strip().replace("до", "")
    except AttributeError:
        end_date = "ParseError"
    try:
        end_date = re.split(r'[(]\d', end_date)[0].strip()
    except AttributeError:
        end_date = "ParseError"
    try:
        start_value = soup.find("div", class_="lot-item__sum").find("meta")["content"]
    except AttributeError:
        start_value = "ParseError"
    try:
        tender_status = soup.findAll("div", class_="steps__help")
        statuses = []
        for status in tender_status:
            status = status.find("h4", class_="steps__helptitle").text
            statuses.append(status)
        tender_status = statuses[1]
    except AttributeError:
        tender_status = "ParseError"
    try:
        tender_type = soup.findAll("p", class_="data-table__info")[5].text
    except AttributeError:
        tender_type = "ParseError"
    try:
        customers = soup.findAll("p", class_="data-table__info")[1].text
    except AttributeError:
        customers = "ParseError"
    data = {
        "tender_name": tender_name.replace("\n", ""),
        "tender_number": tender_number.replace("\n", ""),
        "order": "Нет информации",
        "tender_type": tender_type.replace("\n", ""),
        "start_value": start_value.replace("\n", ""),
        "start_date": start_date.replace("\n", ""),
        "end_date": end_date.replace("\n", ""),
        "tender_status": tender_status.replace("\n", ""),
        "purchase_object": tender_name.replace("\n", ""),
        "customers": customers.replace("\n", "")
    }
    write_data(data, time_str)

def main():
    pages = get_links()
    time_str = time.strftime("%Y%m%d-%H%M%S")
    creating_csv(time_str)
    for page in pages:
        url = f"https://www.roseltorg.ru{page}"
        r = requests.get(url, headers=change_useragent())
        soup = BeautifulSoup(r.text, "lxml")
        parsing_data(soup, time_str)


def test():
    pages = get_links()
    url = f"https://www.roseltorg.ru{pages[0]}"
    time_str = time.strftime("%Y%m%d-%H%M%S")
    print(url)
    r = requests.get(url, headers=change_useragent())
    soup = BeautifulSoup(r.text, "lxml")
    parsing_data(soup, time_str)


def get_links():
    url = "https://www.roseltorg.ru/procedures/search_ajax"
    pages = []
    page = 0
    for page in range(2):
        query_string = {"sale": "0", "query_field": "Разработка", "status^%^5B^%^5D": ["21", "0"], "currency": "all",
                        "page": page}
        response = requests.request("GET", url, data=payload, headers=change_useragent(), params=query_string)
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.findAll("a", class_="search-results__link")
        for link in links:
            pages.append(link.get("href"))
    return pages


if __name__ == "__main__":
    main()
