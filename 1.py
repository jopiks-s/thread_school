import tkinter as tk

import customtkinter as ctk


def increase():
    global counter_var
    counter_var.set(counter_var.get() + 1)


def decrease():
    global counter_var, log_box
    counter_var.set(counter_var.get() - 1)


def slide(v: float):
    global counter_var
    counter_var.set(int(v * 50))


def log_counter(name, *args):
    global counter_var, log_box, radio_var, checks
    log_box.configure(state='normal')
    if name == 'counter':
        log_box.insert('end', f'Counter: {counter_var.get()}\n')
    elif name == 'radio':
        log_box.insert('end', f'Radio button selected: {radio_var.get()}\n')
    else:
        idx = int(name[-1])
        log_box.insert('end', f'Check button {idx}: {"Check" if checks[idx].get() else "Uncheck"}\n')

    log_box.configure(state='disabled')


ctk.set_appearance_mode('dark')
root = ctk.CTk()
root.geometry("800x300")
root.title("1 lab")

btn_frm = ctk.CTkFrame(root, border_width=1)
counter_ftm = ctk.CTkFrame(root, border_width=0)
info_frm = ctk.CTkFrame(root, border_width=0)

btn_frm.place(relwidth=.45, relheight=.35, relx=.025, rely=.025)
counter_ftm.place(relwidth=.5, relheight=.6, rely=.4)
info_frm.place(relwidth=.5, relheight=1, relx=.5)

btn_frm.rowconfigure([0, 1, 2], weight=1)
btn_frm.columnconfigure([0, 1], weight=1)
radio_var = tk.IntVar(value=0, name='radio')
checks = []
for i in range(3):
    radio = ctk.CTkRadioButton(btn_frm, text=f'Radio {i}', variable=radio_var, value=i)
    radio.grid(row=i, column=0)
for i in range(3):
    def log_decorator(v):
        return lambda name, *args: log_counter(f'check {v}', *args)


    check_var = tk.IntVar(value=0)
    check_var.trace_add('write', log_decorator(i))
    check = ctk.CTkCheckBox(btn_frm, text=f'Check {i}', variable=check_var)
    check.grid(row=i, column=1)
    checks.append(check)

counter_ftm.rowconfigure([0, 1], weight=1)
counter_ftm.columnconfigure([0, 1], weight=1)
ctk.CTkLabel(counter_ftm, text='Counter:').grid(row=0, column=0, sticky='w', padx=40)

counter_var = tk.IntVar(value=0, name='counter')
counter = ctk.CTkLabel(counter_ftm, text='0', textvariable=counter_var)
counter.grid(row=0, column=1, sticky='w', padx=40)

ctk.CTkButton(counter_ftm, text='Decrease', command=decrease).grid(row=1, column=0)
ctk.CTkButton(counter_ftm, text='Increase', command=increase).grid(row=1, column=1)

info_frm.rowconfigure([0, 1, 2], weight=2)
info_frm.columnconfigure([0, 1], weight=1)
log_box = ctk.CTkTextbox(info_frm, state='disabled')
log_box.grid(row=0, column=0, columnspan=2, sticky='we', padx=30)
slider = ctk.CTkSlider(info_frm, command=slide, number_of_steps=50)
slider.grid(row=1, column=0, columnspan=2, sticky='we', padx=30)
ctk.CTkLabel(info_frm, text='1').grid(row=2, column=0, sticky='w', padx=30)
ctk.CTkLabel(info_frm, text='50').grid(row=2, column=1, sticky='e', padx=30)

radio_var.trace_add('write', log_counter)
counter_var.trace_add('write', log_counter)

root.mainloop()
