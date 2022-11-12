from bs4 import BeautifulSoup
import requests
import csv

header = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}


class RegionsParser:
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
        bs = self.get_bs_page("https://synapsenet.ru/search/tenderi-po-regionam")
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
        tender_content_bs = self.get_bs_page(f"https://synapsenet.ru{tender_url}")
        tender_data.append(tender_content_bs.find(class_="tct-tender-number").text.split()[1])
        try:
            tender_data.append(tender_content_bs.find(class_="tender-sourse-point").next_sibling.text.split()[-1])
        except IndexError:
            tender_data.append('-')
        try:
            tender_data.append(tender_content_bs.find(class_="tender-sourse-point").next_sibling.text.split()[0])
        except IndexError:
            tender_data.append('-')
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
        try:
            tender_content_bs.find(class_="tct-tender-text").next_sibling.find_all("div")[1].text
        except AttributeError:
            tender_content_bs.find(class_="tct-tender-text").next_sibling.next_sibling.find_all("div")[1].text
        tender_data.append(tender_content_bs.find(class_="tct-tender-text").text)  # обьект закупки
        tender_data.append(tender_content_bs.find(class_="tc-customer-name").text)  # заказчик
        return tender_data

    def get_docs(self):
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


class KeywordParser:
    def __init__(self, keyword_request):
        with open("data.csv", "w", newline='') as data_file:
            writer = csv.writer(data_file, delimiter=';')
            writer.writerow(
                ("Номер", "Закон", "Вид", "Начальная цена", "Дата размещения", "Дата окончания тендера", "Статус",
                 "Объект закупки", "Заказчик"))
        data_file.close()
        self.url = self.make_url(keyword_request)
        self.num_of_pages = int(self.number_of_pages(self.get_bs_page(self.url)))

    def start(self):
        counter = 1
        for i in range(self.num_of_pages):
            refs = self.get_refs_from_page()
            for ref in refs:
                tender_data = self.get_tender_data(ref)
                self._write_data(tender_data)
            self.url = self.get_ref_to_next_page()

    def test(self):
        tender_data = []
        url = "https://synapsenet.ru/zakupki/b2b/3141971_4--voronezhskaya-obl-bitum-bnd-70100-mnpz-kapotnya-moskva-v-kolichestve"
        tender_content_bs = self.get_bs_page(url)
        t = self.get_type(tender_content_bs)

    @staticmethod
    def get_law(bs_page):
        try:
            return bs_page.find(class_="tender-sourse-point").next_sibling.text.split()[-1]
        except IndexError:
            elements = str(
                bs_page.find(class_="tender-sourse-point").next_sibling.next_sibling.text.split('•')[0]).split()
            return " ".join(elements)

    @staticmethod
    def get_type(bs_page):
        try:
            return bs_page.find(class_="tender-sourse-point").next_sibling.text.split()[0]
        except IndexError:
            return bs_page.find(class_="tender-sourse-point").next_sibling.next_sibling.text.split('•')[1].split()[0]

    def get_tender_data(self, url):
        tender_data = []
        tender_content_bs = self.get_bs_page(url)
        tender_data.append(tender_content_bs.find(class_="tct-tender-number").text.split()[1])
        tender_data.append(self.get_law(tender_content_bs))
        tender_data.append(self.get_type(tender_content_bs))
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
        try:
            tender_data.append(tender_content_bs.find(class_="tct-tender-text").next_sibling.find_all("div")[1].text)
        except AttributeError:
            tender_data.append(
                tender_content_bs.find(class_="tct-tender-text").next_sibling.next_sibling.find_all("div")[1].text)
        tender_data.append(tender_content_bs.find(class_="tct-tender-text").text) # обьект закупки
        tender_data.append(tender_content_bs.find(class_="tc-customer-name").text)  # заказчик
        return tender_data

    def get_refs_from_page(self):
        bs = self.get_bs_page(self.url)
        titles = bs.find_all(class_="sp-tb-title", href=True)
        refs = [f"https://synapsenet.ru{title['href']}" for title in titles]
        return refs

    @staticmethod
    def get_bs_page(url: str):
        request = requests.get(url, headers=header)
        content = request.text
        with open("page.html", "w", encoding='utf-8') as file:
            file.write(content[1:])
        file.close()
        return BeautifulSoup(content, "lxml")

    def get_ref_to_next_page(self):
        self.url = self.url.split("page=")
        self.url[-1] = str(int(self.url[-1]) + 1)
        return "page=".join(self.url)

    # def get_ref_to_next_page(self, url, cur_page: int):
    #     url = url.split("page=")
    #     url[-1] = f"page={str(cur_page+1)}"
    #     return "".join(url)
    def number_of_pages(self, bs):
        num = bs.find(id="sbg-navigation").find_all("a")[-1]['href'].split("page=")[-1]
        return num

    @staticmethod
    def _write_data(tender_data):
        with open("data.csv", "a", newline='', encoding='windows-1251') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(tender_data)
        file.close()

    @staticmethod
    def make_url(keyword_request):
        url = "https://synapsenet.ru/search/tenderi-po-regionam?query="
        words = keyword_request.split()
        for word in words:
            url += f"{word}+"
        url = url[:len(url) - 1]
        url += "&page=1"
        return url


parser = KeywordParser("дороги москвы")
parser.start()

# Номер тендера
# Регламентирующий закон
# Вид тендера
# Начальная цена
# Дата размещения
# Дата окончания тендера
# статус заявки
# Объект закупки
# Организация заказчик
