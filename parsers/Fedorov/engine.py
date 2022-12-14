from os import makedirs, path
from csv import DictWriter
from requests import post, get
from copy import deepcopy
import re

LIMIT_ONE_REQ = 5
BASE_URL = '/data'

FIELDS_DATA = {
    'tender_number': 'Номер тендера',
    'object': 'Объект тендера',
    'type': 'Регулирующий закон / вид тура',
    'status': 'Статус заявки',
    'start_sum': 'Начальная сумма',
    'publication_date': 'Дата размещений',
    'end_date': 'Дата окончания',
    'organization': 'Организация',
    'documents': 'Документы'
}

FIELDS = list(FIELDS_DATA.keys())


def get_const_req_body(name):
    return {
        "manager": "sphinx",
        "entity": "Procedure",
        "alias": "procedure, count(distinct procedure.id) as countAll",
        "fields": ["procedure.countAll"],
        "conditions": {
            "procedure.id": ["gt", 0],
            "*": ["match", name]
        },
        "rules": ["Procedure.Registry"],
        "limit": 1
    }


def get_info_req_body(name, offset):
    return {
        "manager": "sphinx",
        "entity": "Procedure",
        "alias": "procedure",
        "fields": [
            "procedure.number",
            "procedure.purchaseNumber",
            "procedure.purchaseObjectInfo",
            "procedure.status",
            "procedure.substatus",
            "procedure.publicationDateTime",
            "procedure.endDateTime",
            "procedure.placerFullName",
            "procedure.maxSum",
            "procedure.typeName"
        ],
        "conditions": {
            "procedure.id": ["gt", 0],
            "*": ["match", name]
        },
        "rules": [
            "Procedure.Registry",
            "Procedure.Info",
            "Procedure.CommonData"
        ],
        "sort": {
            "procedure.regulatedStatusOrder": "DESC",
            "procedure.regulatedDateTime": "ASC",
            "procedure.publicationDateTime": "DESC"
        },
        "limit": LIMIT_ONE_REQ,
        "offset": offset
    }


def get_docs_req_body(id):
    return {
        "manager": "procedures",
        "entity": "Purchase",
        "alias": "procedure",
        "fields": [
            "procedure.documents"
        ],
        "conditions": {
            "procedure.id": id
        },
        "rules": [
            "Purchase.Documentation"
        ]
    }


def execute_request(req_body, url='list'):
    req_link = 'https://gz.lot-online.ru/etp_back/api/' + url
    r = post(req_link, json=req_body)
    return r.json()


def get_count_tenders(name):
    req_body = get_const_req_body(name)

    result = execute_request(req_body)
    if int(result['status']) != 0:
        return 0

    result = result['data']['entities']
    if len(result) == 0:
        return 0

    count_tenders = int(result[0]['procedure']['countAll'])
    return count_tenders


def get_docs_tender(id):
    docs_tender = []
    req_body = get_docs_req_body(id)

    result = execute_request(req_body, 'get')
    if int(result['status']) != 0:
        return docs_tender

    for item in result['data']['entities']:
        for document in item['procedure']['documents']:
            document_data = {
                'title': document['title'],
                'extension': document['extension'],
                'url': document['uri']
            }
            docs_tender.append(document_data)

    return docs_tender


def get_list_tenders(name, offset):
    list_tenders = []
    req_body = get_info_req_body(name, offset)

    result = execute_request(req_body)
    if int(result['status']) != 0:
        return list_tenders

    for item in result['data']['entities']:
        tender = item['procedure']
        tender_data = {
            'tender_number': tender['purchaseNumber'],
            'object': tender['purchaseObjectInfo'],
            'type': tender['typeName'],
            'status': tender['substatus'] or tender['status'],
            'start_sum': float(tender['maxSum'].replace(' ', '')),
            'publication_date': tender['publicationDateTime'],
            'end_date': tender['endDateTime'],
            'organization': tender['placerFullName'],
            'documents': get_docs_tender(tender['number'])
        }
        list_tenders.append(tender_data)

    return list_tenders


def add_row(data, writer):
    values = deepcopy(data)
    documents = list(map(lambda doc: "{}: {}".format(doc['title'], doc['url']), values['documents']))

    for key in values.keys():
        values[key] = values[key] or ''

    values['documents'] = ', '.join(documents)
    writer.writerow(values)

    return values['tender_number'], values['object'], data['documents']


def download_docs(id, docs, dir_path):
    if len(docs) == 0:
        return
    docs_dir = f'{dir_path}/{id.split(".")[0]}'

    for doc in docs:
        try:
            name_file = f"{doc['title'].split('.')[0]}.{doc['extension']}"
            name_file = re.sub('/:*?"<>|', '', name_file)
            bin_file = get(doc['url'])
            makedirs(docs_dir, exist_ok=True)
            with open(f'{docs_dir}\\{name_file}', "wb") as file:
                file.write(bin_file.content)
        except:
            continue
