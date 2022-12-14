import requests
from random import choice
from .common import write_data

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

headers = {
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://stavzmo.rts-tender.ru",
    "Pragma": "no-cache",
    "Referer": "https://stavzmo.rts-tender.ru/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": choice(desktop_agents),
    "XXX-TenantId-Header": "106",
    "sec-ch-ua": "^\^Not?A_Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^108^^, ^\^Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}


def parsing_data(response_json, dir_path):
    for data in response_json['invdata']:
        data = {
            "tender_number": data['TradeNumber'],
            "tender_name": data['TradeName'],
            "order": data['ZmoFzTypeString'],
            "tender_type": "No data",
            "start_value": data['InitialPrice'],
            "start_date": data['PublicationDate'],
            "end_date": data[
                'FillingApplicationEndDate'],
            "tender_status": data['TradeStateName'],
            "customers": data['CustomerFullName'],
            "docs": "No data"
        }
        write_data(data, dir_path)


def increase_page(value, trade_name):
    value += 1
    return {"CustomerAddress": "",
            "CustomerFullNameOrInn": "",
            "FilterFillingApplicationEndDateTo": None,
            "IsExpire": False,
            "IsImmediate": False,
            "OnlyTradesWithMyApplications": False,
            "ParticipantHasApplicationsOnTrade": "",
            "TradeSearchType": 50,
            "UseCustomerInn": False,
            "UseCustomerName": True,
            "UsedClassificatorType": 5,
            "ZmoFinanceSourceBudget": True,
            "ZmoFinanceSourceFederalBudget": False,
            "ZmoFinanceSourceMixedBudget": True,
            "ZmoFinanceSourceMunicipalBudget": False,
            "ZmoFinanceSourceOutOfBudget": True,
            "ZmoFinanceSourceRegionalBudget": False,
            "ZmoFzType": 0,
            "classificatorCodes": [],
            "filterDateFrom": None,
            "filterDateTo": None,
            "filterFillingApplicationEndDateFrom": None,
            "filterPriceMax": "",
            "filterPriceMin": "",
            "filterTradeEasuzNumber": "",
            "itemsPerPage": 5000,
            "page": value,
            "showOnlyOwnTrades": True,
            "tradeName": trade_name,
            "tradeState": ""}


def rts(trade_name, dir_path):
    print("Парсим rts-tender.ru")
    url = "https://zmo-new-webapi.rts-tender.ru/api/Trade/GetTradesForAnonymous"
    response = requests.request("POST", url, json=increase_page(0, trade_name), headers=headers)
    total_pages = response.json()['totalpages']
    parsing_data(response.json(), dir_path)
    total_pages = response.json()['totalpages']
    for i in range(1, total_pages + 1):
        payload = {"CustomerAddress": "", "CustomerFullNameOrInn": "", "FilterFillingApplicationEndDateTo": None,
                   "IsExpire": False, "IsImmediate": False, "OnlyTradesWithMyApplications": False,
                   "ParticipantHasApplicationsOnTrade": "", "TradeSearchType": 50, "UseCustomerInn": False,
                   "UseCustomerName": True, "UsedClassificatorType": 5, "ZmoFinanceSourceBudget": True,
                   "ZmoFinanceSourceFederalBudget": False, "ZmoFinanceSourceMixedBudget": True,
                   "ZmoFinanceSourceMunicipalBudget": False, "ZmoFinanceSourceOutOfBudget": True,
                   "ZmoFinanceSourceRegionalBudget": False, "ZmoFzType": 0, "classificatorCodes": [],
                   "filterDateFrom": None, "filterDateTo": None, "filterFillingApplicationEndDateFrom": None,
                   "filterPriceMax": "", "filterPriceMin": "", "filterTradeEasuzNumber": "", "itemsPerPage": 10,
                   "page": f"{i}",
                   "showOnlyOwnTrades": True, "tradeName": trade_name, "tradeState": ""}
        response = requests.request("POST", url, json=payload)
        parsing_data(response.json())


if __name__ == "__main__":
    search_query = input('Введите название тендера: ')
    dir_path = f'data/{search_query}'
    rts(search_query, dir_path)
