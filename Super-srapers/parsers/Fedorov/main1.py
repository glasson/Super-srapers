from engine import LIMIT_ONE_REQ, get_count_tenders, get_list_tenders, add_row, download_docs


def rad(search_query, dir_path, is_download = False):
    print("Парсим lot-online.ru")
    total = get_count_tenders(search_query)
    count = 0

    for offset in range(0, total, LIMIT_ONE_REQ):
        tenders = get_list_tenders(search_query, offset)
        for tender in tenders:
            count += 1
            id, name, docs = add_row(tender, dir_path)
            print(f'{count}. {name} (№{id})')
            if is_download:
                download_docs(id, docs, dir_path)



if __name__ == '__main__':
    print(1)
