from bs4 import BeautifulSoup
import requests
import csv

region_page_url = "https://synapsenet.ru/search/tenderi-po-regionam"
header = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}


class Parser:
    def __init__(self):
        self.regions_refs = []
        self.regions_names = []
        with open("data.csv", "w", newline='') as data_file:
            writer = csv.writer(data_file, delimiter=';')
            writer.writerow(
                ("Номер", "Закон", "Вид", "Начальная цена", "Дата размещения", "Дата окончания тендера", "Статус",
                 "Объект закупки", "Заказчик"))
            data_file.close()

    def get_regions_refs(self):
        bs = self.get_bs_page(region_page_url)
        self.regions_refs = bs.find(id="sp-region-script").find_all("a")
        for item in self.regions_refs:
            self.regions_names.append(item.attrs.get('href').split('/')[-1])

    def get_and_write_tenders(self):
        iterator = 0
        for region in self.regions_names:  # а в этом, обработать ссылки со страницы которые достал внутренний
            for page in range(1, 201):  # в этом цикле собрать ссылки
                url = "https://synapsenet.ru/search/regions/{0}?page={1}".format(region, page)
                bs = self.get_bs_page(url)
                tags = bs.find_all(class_="sp-tb-title", href=True)
                page_tender_urls = [a['href'] for a in tags]

                for tender_url in page_tender_urls:
                    tender_data = self._get_elements_from_page(tender_url)
                    self._write_data(tender_data)
                    iterator += 1
                    print(f"Записано {iterator}")

    # tender_content_bs.find(class_="tender-card-right", id = "documents-script")
    # #блок с документами + проверка на их наличие
    # здесь принять документаицю (написать функции для документации) и собрать в архив с номером тендера tender_data[0]
    def _get_elements_from_page(self, tender_url):
        tender_data = []
        tender_content_bs = self.get_bs_page(f"https://synapsenet.ru/{tender_url}")
        tender_data.append(tender_content_bs.find(class_="tct-tender-number").text.split()[1])
        tender_data.append(tender_content_bs.find(class_="tender-sourse-point").next_sibling.text.split()[-1])
        tender_data.append(tender_content_bs.find(class_="tender-sourse-point").next_sibling.text.split()[0])
        money = tender_content_bs.find(class_="tender-money").text.replace("\xa0", " ")[:-1]
        if money == "не указан":
            tender_data.append("-")
        else:
            tender_data.append(money)

        try:
            time = tender_content_bs.find(class_="tender-time-noline").find_all(title="по московскому времени")
        except AttributeError:
            time = tender_content_bs.find(class_="tender-time-line").find_all(title="по московскому времени")
        tender_data.append(time[0].text)  # появление заявки
        tender_data.append(time[1].text)  # ее окончание
        tender_content_bs.find(class_="tct-tender-text").next_sibling.find_all("div")[1].text
        try:  # обьект закупки
            tender_data.append(tender_content_bs.find(class_="tender-positions-table").find("td").text)
        except AttributeError:
            tender_content_bs.find(class_="tct-tender-text")
        tender_data.append(tender_content_bs.find(class_="tc-customer-name").text)  # заказчик
        return tender_data

    def get_docs(self):
        # tender_content_bs.find(class_="tender-card-right", id = "documents-script")
        # #блок с документами + проверка на их наличие
        # здесь принять документаицю (написать функции для документации) и собрать в архив с номером тендера tender_data[0]
        ...

    @staticmethod
    def _write_data(tender_data):
        with open("data.csv", "a", newline='', encoding='windows-1251') as data_file:
            writer = csv.writer(data_file, delimiter=';')
            writer.writerow(tender_data)

    @staticmethod
    def get_bs_page(url: str):
        request = requests.get(url, headers=header)
        content = request.text
        with open("page.html", "w", encoding='utf-8') as file:
            file.write(content[1:])
        file.close()
        return BeautifulSoup(content, "lxml")


parser = Parser()
parser.get_regions_refs()
parser.get_and_write_tenders()
