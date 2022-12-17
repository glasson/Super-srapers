from parsers import *
from parsers.Fedorov.main1 import rad
from os import makedirs
from datetime import datetime
import csv
from  threading import Thread
import tkinter


# rts, zakupki360, roseltorg, synapsenet, rad, fabricant
PARSERS_LIST = [fabricant, synapsenet, rts, zakupki360, roseltorg, rad]
DOWNLOADING_DOCS = True


def creating_csv(dir_path):
    with open('{}\\purchases.csv'.format(dir_path), "w", encoding="utf-16", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(FIELDS_NAME)


def get_amount_tenders(dir_path):
    with open('{}\\purchases.csv'.format(dir_path), "r", encoding="utf-16") as file:
        reader = csv.reader(file, delimiter=";")
        return len(list(reader)) - 1

def start_parsing(search_query, threads):
    global is_threads_started

    if is_threads_started:
        ...
        # завершить треды

    for thread in threads:
        thread.start()
    is_threads_started = True
    # добавить вызов потоков и флаг

def delete_threads():
    ...

def make_threads(dir_path, search_query):
    threads = []
    for parser in PARSERS_LIST:
        try:
            thread = Thread(target=parser, args=[search_query, dir_path, DOWNLOADING_DOCS])
            threads.append(thread)
        except:
            continue
    return threads


def make_window():
    window = tkinter.Tk()
    window.iconbitmap('ico.ico')
    window.geometry("300x300")
    window.title("Парсер")
    return window

def make_widgets(window):
    label = tkinter.Label(window, text="Введите ключевые слова")
    label.place(relx=0.5, rely=0.3, anchor='center')
    entry = tkinter.Entry(window)
    entry.place(relx=0.5, rely=0.4, anchor='center')
    btn = tkinter.Button(window, text="Начать парсинг", command=lambda: start_parsing(entry.get()))
    btn.place(relx=0.5, rely=0.5, anchor='center')




def main():
    search_query: str
    is_threads_started = False

    window = make_window()
    make_widgets(window)

    now = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    dir_path = f'data/{search_query}_{now}'
    makedirs(dir_path, exist_ok=True)
    creating_csv(dir_path)
    threads = make_threads(dir_path, search_query)

    window.mainloop()




if __name__ == '__main__':
    main()


