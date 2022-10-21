#!/usr/bin/python3

import tkinter as tk

window = tk.Tk()

window.title('My Window')

window.geometry('1000x618')


l = tk.Label(window, text='nihao! this is Tkinter', bg='green', font=('Arial', 12), width=30, height=2)

l.pack()

window.mainloop()
