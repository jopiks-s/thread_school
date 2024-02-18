import tkinter as tk
from random import random

import customtkinter as ctk


class LoopProgressBar(ctk.CTkProgressBar):
    def __init__(self, *args, **kwargs):
        self.last_direction = True
        super().__init__(*args, **kwargs)

    def start(self):
        if not self._loop_running:
            self._loop_running = True
            self._internal_loop(self.last_direction)

    def _internal_loop(self, up: bool = True):
        if self._loop_running:
            if self._mode == "determinate":
                self.last_direction = up
                addition = self._determinate_speed / 50 * (1 if up else -1)
                self.set(self._determinate_value + addition)
                self._draw()
                if up and self._determinate_value >= 1:
                    self._loop_after_id = self.after(20, self._internal_loop, False)
                elif not up and self._determinate_value <= 0:
                    self._loop_after_id = self.after(20, self._internal_loop)
                else:
                    self._loop_after_id = self.after(20, self._internal_loop, up)
            else:
                self._indeterminate_value += self._indeterminate_speed
                self._draw()
                self._loop_after_id = self.after(20, self._internal_loop)


def calculate_area(area_var: tk.DoubleVar, progress_var: tk.DoubleVar):
    def _inner(*args):
        area_var.set(round(progress_var.get() * 130 * 40, 2))

    return _inner


def sum_areas(*args):
    global areas, sum_area_var
    sum_area = round(sum([area.get() for area in areas]), 2)
    sum_area_var.set(sum_area)

ctk.set_appearance_mode('dark')
root = ctk.CTk()
root.geometry("600x300")
root.title("2 lab")

root.rowconfigure([0, 1, 3], weight=1)
root.rowconfigure(2, weight=4)
root.columnconfigure(list(range(4)), weight=1)

sum_area_var = tk.DoubleVar(value=0)
areas = []
for i in range(4):
    area_var = tk.DoubleVar(value=0)
    areas.append(area_var)
    ctk.CTkLabel(root, textvariable=area_var, text_color='#39cfed').grid(row=0, column=i, sticky='s')
    ctk.CTkLabel(root, text=f'Thread {i + 1}', text_color='grey').grid(row=1, column=i, sticky='n')
    progress_var = tk.DoubleVar(value=0)
    area = LoopProgressBar(root, 40, 130, orientation='vertical', corner_radius=0, variable=progress_var,
                           determinate_speed=0.2 + random())
    progress_var.trace_add('write', calculate_area(area_var, progress_var))
    area_var.trace_add('write', sum_areas)
    area.start()
    area.grid(row=2, column=i, sticky='n')

ctk.CTkLabel(root, text='Thread 5', text_color='gray').grid(row=3, column=0, pady=(0, 20))
ctk.CTkLabel(root, text='Total area: ').grid(row=3, column=1, pady=(0, 20))

ctk.CTkLabel(root, textvariable=sum_area_var, text_color='red').grid(row=3, column=2, columnspan=2, pady=(0, 20),
                                                                     sticky='w')

root.mainloop()
