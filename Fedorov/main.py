from engine import LIMIT_ONE_REQ, get_count_tenders, get_list_tenders, create_dir_tenders, add_row, download_docs


def main():
    search_query = input('Введите название тендера: ')

    total = get_count_tenders(search_query)
    writer, sheet_file, dir_path = create_dir_tenders(search_query)
    print(f'Найдено тендеров: {total}\n')
    count = 0

    print('Тендеры:')
    for offset in range(0, total, LIMIT_ONE_REQ):
        tenders = get_list_tenders(search_query, offset)
        for tender in tenders:
            count += 1
            id, name, docs = add_row(tender, writer)
            download_docs(id, docs, dir_path)
            print(f'{count}. {name} (№{id})')

    sheet_file.close()

    print('\nУспешно обработано тендеров: {}/{}'.format(count, total))


if __name__ == '__main__':
    main()
