from parsers.Fedorov.engine import LIMIT_ONE_REQ, get_count_tenders, get_list_tenders, add_row, download_docs


def rad(search_query, dir_path):
    print("Парсим lot-online.ru")
    total = get_count_tenders(search_query)

    for offset in range(0, total, LIMIT_ONE_REQ):
        tenders = get_list_tenders(search_query, offset)
        for tender in tenders:
            id, name, docs = add_row(tender, dir_path)
            download_docs(id, docs, dir_path)



if __name__ == '__main__':
    search_query = input('Введите название тендера: ')
    dir_path = f'data/{search_query}'
    rad(search_query, dir_path)
