import ctypes
import math
import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Value
from random import randint
from time import perf_counter

import customtkinter as ctk


def digits_only(s):
    return str.isdigit(s) or s == ''


def sum_process(values: list[int], threads_n: int):
    if threads_n <= 1:
        return sum(values)
    else:
        size = len(values)
        chunk_size = math.ceil(size / threads_n)
        with ThreadPoolExecutor(threads_n) as executor:
            return sum(executor.map(lambda v: sum(v), [values[i:i + chunk_size] for i in range(0, size, chunk_size)]))


def _calculate(cores_n: int, threads_n: int, array_size: int, execution_time: Value, average: Value):
    array = [randint(-1000000, 1000000) for _ in range(array_size)]
    chunk_size = math.ceil(array_size / cores_n)
    sums = []

    start = perf_counter()
    with ProcessPoolExecutor(cores_n) as executor:
        chunk_arrays = [array[i:i + chunk_size] for i in range(0, array_size, chunk_size)]
        for result in executor.map(sum_process, chunk_arrays, [threads_n] * len(chunk_arrays)):
            sums.append(result)

    average.value = int(sum(sums) / array_size)
    execution_time.value = int((perf_counter() - start) * 10 ** 3)


def calculate():
    if not array_entry.get():
        array_entry.insert(0, '0')
    if not thread_entry.get():
        thread_entry.insert(0, '1')

    if int(thread_entry.get()) == 0:
        thread_entry.configure(text_color='red')
        thread_entry.after(100, lambda: thread_entry.configure(text_color='white'))
        return

    def _inner():
        cores_n = cores_number.get()
        threads_n = int(thread_entry.get())
        array_size = int(array_entry.get())

        calculate_btn.configure(state='disabled')
        execution_time = Value(ctypes.c_float, 0)
        average = Value(ctypes.c_int, 0)
        p = multiprocessing.Process(target=_calculate, args=(cores_n, threads_n, array_size, execution_time, average))
        p.start()
        p.join()

        output_box.configure(state='normal')
        output_box.insert('end', f'Number of selected cores: {cores_n}\n')
        output_box.insert('end', f'Array average: {average.value}\n')
        output_box.insert('end', f'Execution time: {execution_time.value}ms\n')
        output_box.configure(state='disabled')

        calculate_btn.configure(state='normal')

    threading.Thread(target=_inner).start()


if __name__ == '__main__':
    ctk.set_appearance_mode('dark')
    root = ctk.CTk()
    root.geometry("600x350")
    root.title("4 lab")
    digits_only = root.register(digits_only)
    cpu_count = multiprocessing.cpu_count()

    root.rowconfigure(list(range(4)), weight=1)
    root.columnconfigure([0, 1], weight=1)
    root.columnconfigure(2, weight=2)

    cores_number = ctk.IntVar(value=1)

    ctk.CTkLabel(root, text='Cores number').grid(row=0, column=0, sticky='e')
    slider_frm = ctk.CTkFrame(root)
    slider_frm.rowconfigure(0, weight=1)
    slider_frm.columnconfigure([0, 1], weight=1)
    ctk.CTkSlider(slider_frm, 130, from_=1, to=cpu_count, variable=cores_number).grid(row=0, column=0)
    ctk.CTkLabel(slider_frm, textvariable=cores_number).grid(row=0, column=1, padx=5)
    slider_frm.grid(row=0, column=1, sticky='w', padx=30)

    ctk.CTkLabel(root, text='Array size').grid(row=1, column=0, sticky='e')
    array_entry = ctk.CTkEntry(root, validate='all', validatecommand=(digits_only, '%P'))
    array_entry.grid(row=1, column=1, sticky='w', padx=30)
    array_entry.insert(0, '5000000')

    ctk.CTkLabel(root, text='Threads number').grid(row=2, column=0, sticky='e', pady=(0, 50))
    thread_entry = ctk.CTkEntry(root, validate='all', validatecommand=(digits_only, '%P'))
    thread_entry.grid(row=2, column=1, sticky='w', padx=30, pady=(0, 50))
    thread_entry.insert(0, '1')

    calculate_btn = ctk.CTkButton(root, text='Calculate', command=calculate)
    calculate_btn.grid(row=3, column=0, columnspan=3, pady=(0, 30))

    output_box = ctk.CTkTextbox(root, state='disabled')
    output_box.grid(row=0, column=2, rowspan=3, sticky='ns', pady=30)

    root.mainloop()
