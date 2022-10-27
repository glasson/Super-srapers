from engine import LIMIT_ONE_REQ, get_count_tenders, get_list_tenders, create_csv, add_row


def main():
    search_query = input('Введите название тендера: ')

    total = get_count_tenders(search_query)
    writer, file = create_csv(search_query)
    print(f'Найдено тендеров: {total}\n')
    count = 0

    print('Тендеры:')
    for offset in range(0, total, LIMIT_ONE_REQ):
        tenders = get_list_tenders(search_query, offset)
        for tender in tenders:
            count += 1
            id, name = add_row(tender, writer)
            print(f'{count}. {name} (№{id})')

    file.close()

    print('\nУспешно обработано тендеров: {}/{}'.format(count, total))


if __name__ == '__main__':
    main()
