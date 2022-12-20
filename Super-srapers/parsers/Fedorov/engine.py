from os import makedirs, path
from requests import post, get
from copy import deepcopy
import re

LIMIT_ONE_REQ = 10
BASE_URL = '/data'


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


