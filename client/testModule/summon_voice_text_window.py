import sys
import os
sys.path.append(os.path.abspath(".."))
from helperModule import helper

import tkinter as tk

def record():
    tki = tk.Tk()
    tki.title("Voice test")
    tki.iconbitmap(default='./vega.ico')

    # calculate spawn position and window size

    screen_width = tki.winfo_screenwidth()
    screen_height = tki.winfo_screenheight()
    spawn_x = (screen_width // 2) - 300
    spawn_y = (screen_height // 2) - 200

    tki.resizable(0,0) # disable resize
    tki.geometry("600x400+" + str(spawn_x) + "+" + str(spawn_y))

    # Label 1
    label1 = tk.Label(
        tki,
        text='Please read the following sentence aloud.'
        )
    label1.pack()

    # Label 2
    label2 = tk.Label(
        tki,
        text='The quick brown fox jumps over the lazy dog.'
        )
    label2.pack(expand=True)

    # button
    button1 = tk.Button(
        tki,
        text='OK',
        command=lambda: tki.destroy()
        )
    button1.pack()

    tki.mainloop()