#!/usr/bin/env python3
# -*- config: utf-8 -*-

from tkinter import *
import queue
import threading
import time


class QueueThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self) -> None:
        print(f'Старт потока {self.name}')
        process_queue()
        print(f'Завершение потока {self.name}')


def process_queue():
    while True:
        try:
            x = ps_queue.get(block=False)
        except queue.Empty:
            return
        else:
            print_factors(x, quantum, a)

        time.sleep(1)


def print_factors(x, quantum, a):
    if a[x] - quantum > 0:
        a[x] -= quantum
        ps_queue.put(x)
        time.sleep(1.0)
        term.insert(END, f'Процесс PID:{x} не успел завершить свою работу и направлен в очередь\n')
    else:
        term.insert(END, f'Процесс PID:{x} полностью закончил свою работу. Ему понадобилось \
        {int(idx[x] / quantum)} кван.\n')


def entry_get(event):
    global idx,  ps_queue, a
    command = en1.get()
    term.insert(END, f'# {command} \n')
    en1.delete(0, 'end')
    if command == 'exit':
        root.destroy()
    elif command.startswith('add '):
        parts = command.split(' ', maxsplit=2)
        pid = int(parts[1])
        ps_time = float(parts[2])
        idx[pid] = ps_time
        a[pid] = ps_time
        ps_queue.put(pid)
    elif command == 'clear':
        term.delete(0.0, END)
    elif command == 'start':
        thread1 = QueueThread('A')
        thread2 = QueueThread('B')
        thread1.start()
        thread2.start()
    elif command == 'list':
        term.insert(END, f'Список чисел для выделения множителей \n')
        for i in idx:
            term.insert(END, f'{i} \n')
    elif command == 'help':
        term.insert(END, f'"add ЧИСЛО" - добавляет новый процесс и привязывает к нему квант времени. \n')
        term.insert(END, f'"list" - выводит список процессов. \n')
        term.insert(END, f'"clear" - очищает терминал. \n')
        term.insert(END, f'"help" - выводт список команд с кратким описанием. \n')
        term.insert(END, f'"start" - запускает процессы  . \n')
        term.insert(END, f'"exit" - закрывает программу. \n')
    else:
        term.insert(END, f'{command} -- неизвестная комманда, используйте "help". \n')


if __name__ == '__main__':
    idx = {1: 10.0, 2: 9.0, 3: 19.0, 4: 21.0}
    a = dict.copy(idx)
    ps_queue = queue.Queue()
    for x in idx:
        ps_queue.put(x)
    quantum = float(3)
    root = Tk()

    root.geometry('600x400')
    root.title("Подсистема управления процессами с циклическим алгоритмом планирования")
    root.resizable(False, False)

    lb1 = Label(text='Командная срока', width=0)
    lb2 = Label(text='Терминал', width=0)
    en1 = Entry(width=73)
    term = Text(bg='white', width=69, height=19)

    en1.bind('<Return>', entry_get)

    lb1.grid(row=0, column=0, sticky=W, pady=10, padx=5)
    lb2.grid(row=1, column=0, sticky=S)
    en1.grid(row=0, column=1, sticky=W)
    term.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    root.mainloop()
