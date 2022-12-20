
from parsers import *
from parsers.Fedorov.main1 import rad
from os import makedirs
from datetime import datetime
import csv
from threading import Thread
import tkinter
from _thread import interrupt_main
import sys
import os

# rts, zakupki360, roseltorg, synapsenet, rad, fabricant
PARSERS_LIST = [synapsenet, fabricant, rts, zakupki360, roseltorg, rad]
DOWNLOADING_DOCS = True


def creating_csv(dir_path):
    with open('{}\\purchases.csv'.format(dir_path), "w", encoding="Windows-1251", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(FIELDS_NAME)


def get_amount_tenders(dir_path):
    with open('{}\\purchases.csv'.format(dir_path), "r", encoding="Windows-1251") as file:
        reader = csv.reader(file, delimiter=";")
        return len(list(reader)) - 1


class Window:
    def __init__(self):
        self.window = tkinter.Tk()
        self.label = tkinter.Label(self.window, text="Введите ключевые слова")
        self.entry = tkinter.Entry(self.window)
        self.status_label = tkinter.Label(text="Ожидание\nзапуска", fg='grey')
        self.btn = tkinter.Button(self.window, text="Начать парсинг", command=self.start_parsing, background='#ECE5D5')
        self.stop_btn = tkinter.Button(self.window, text="Прервать парсинг", command=self.stop_parsing, background='#ECE5D5')
        self.set_configurations()

        self.now = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
        self.dir_path = ''

        self.is_threads_started = False
        self.threads_list = []

    def set_configurations(self):

        self.window.iconbitmap('ico.ico')
        self.window.geometry("400x400")
        self.window.title("Агрегатор тендерных площадок")
        self.label.place(relx=0.5, rely=0.30, anchor='center')
        self.entry.place(relx=0.5, rely=0.45, anchor='center')
        self.status_label.place(relx=0.8, rely=0.45, anchor='center')
        self.btn.place(relx=0.5, rely=0.55, anchor='center')
        self.stop_btn.place(relx=0.5, rely=0.65, anchor='center')

    def start_parsing(self):
        self.status_label['fg'] = 'green'
        self.status_label['text'] = "Данные собираются"
        self.status_label.place(relx=0.82, rely=0.45, anchor='center')
        self.dir_path = f'data/{self.get_search_query()}_{self.now}'
        makedirs(self.dir_path, exist_ok=True)
        creating_csv(self.dir_path)
        self.threads_list = self.make_threads()
        for thread in self.threads_list:
            thread.start()
        self.is_threads_started = True

    def get_search_query(self):
        return self.entry.get()

    def get_my_thread_class(self):
        threads = MyThreads(self.dir_path, self.get_search_query())
        return threads

    def stop_parsing(self):
        if self.is_threads_started:
            os._exit(0)

    def make_threads(self):
        threads = []
        for parser in PARSERS_LIST:
            try:
                thread = Thread(target=parser, args=[self.get_search_query(), self.dir_path, DOWNLOADING_DOCS])
                threads.append(thread)
            except:
                continue
        return threads












def main():
    mywindow = Window()
    if mywindow.is_threads_started:
        mywindow.window.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
    mywindow.window.mainloop()




if __name__ == '__main__':
    main()


