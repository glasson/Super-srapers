from bs4 import BeautifulSoup
import requests
from .common import write_data

header = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}


class KeywordParser:
    def __init__(self, keyword_request, dir_path):
        self.dir_path = dir_path
        self.url = self.make_url(keyword_request)
        self.num_of_pages = int(self.number_of_pages(self.get_bs_page(self.url)))

    def start(self):
        for i in range(self.num_of_pages):
            refs = self.get_refs_from_page()
            for ref in refs:
                tender_data = self.get_tender_data(ref)
                write_data(tender_data, self.dir_path)
            self.url = self.get_ref_to_next_page()

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

    def get_tender_data(self, url) -> list:
        tender_data = {}
        tender_content_bs = self.get_bs_page(url)
        tender_data["tender_number"] = tender_content_bs.find(class_="tct-tender-number").text.split()[1]
        tender_data["tender_name"] = tender_content_bs.find(class_="tct-tender-text").text
        tender_data["order"] = self.get_law(tender_content_bs)
        tender_data["tender_type"] = self.get_type(tender_content_bs)
        money = tender_content_bs.find(class_="tender-money").text.replace("\xa0", " ")[:-1]
        if money == "не указан":
            tender_data["start_value"] = "-"
        else:
            tender_data["start_value"] = money

        try:
            time = tender_content_bs.find(class_="tender-time-noline").find_all(title="по московскому времени")
        except AttributeError:
            time = tender_content_bs.find(class_="tender-time-line").find_all(title="по московскому времени")
        tender_data["start_date"] = time[0].text # появление заявки
        tender_data["end_date"] = time[1].text  # ее окончание
        try:
            tender_data["tender_status"] = tender_content_bs.find(class_="tct-tender-text").next_sibling.find_all("div")[1].text
        except AttributeError:
            tender_data["tender_status"] = tender_content_bs.find(class_="tct-tender-text").next_sibling.next_sibling.find_all("div")[1].text
        tender_data["customers"] =  tender_content_bs.find(class_="tc-customer-name").text
        tender_data["docs"] =  "No documents"
        return tender_data

    def get_refs_from_page(self):
        bs = self.get_bs_page(self.url)
        titles = bs.find_all(class_="sp-tb-title", href=True)
        refs = [f"https://synapsenet.ru{title['href']}" for title in titles]
        return refs

    @staticmethod
    def get_bs_page(url):
        request = requests.get(url, headers=header)
        content = request.text
        return BeautifulSoup(content, "lxml")

    def get_ref_to_next_page(self):
        self.url = self.url.split("page=")
        self.url[-1] = str(int(self.url[-1]) + 1)
        return "page=".join(self.url)

    @staticmethod
    def number_of_pages(bs):
        try:
            num = bs.find(id="sbg-navigation").find_all("a")[-1]['href'].split("page=")[-1]
            return num
        except:
            raise Exception("Нет страниц")

    @staticmethod
    def make_url(keyword_request):
        url = "https://synapsenet.ru/search/tenderi-po-regionam?query="
        words = keyword_request.split()
        for word in words:
            url += f"{word}+"
        url = url[:len(url) - 1]
        url += "&page=1"
        return url


def synapsenet(kw_query, dir_path):
    print("Парсим synapsenet.ru")
    parser = KeywordParser(kw_query, dir_path)
    parser.start()


if __name__ == "__main__":
    search_query = input('Введите название тендера: ')
    dir_path = f'data/{search_query}'
    synapsenet(search_query, dir_path)

