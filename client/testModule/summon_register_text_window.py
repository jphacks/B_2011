import sys
import os
sys.path.append(os.path.abspath(".."))

import tkinter as tk
exam_id = None
examinee_id = None

def input_ids():
    tki = tk.Tk()
    tki.title("register")

    global exam_id, examinee_id
    def bind_ids():
        global exam_id, examinee_id
        exam_id = txt1.get()
        examinee_id = txt2.get()
        tki.destroy()
    #tki.iconbitmap(default='./vega.ico')

    screen_width = tki.winfo_screenwidth()
    screen_height = tki.winfo_screenheight()
    spawn_x = (screen_width // 2) - 300
    spawn_y = (screen_height // 2) - 200

    tki.resizable(0,0) # disable resize
    tki.geometry("600x400+" + str(spawn_x) + "+" + str(spawn_y))

    # Label 1
    label1 = tk.Label(
        tki,
        text='ユーザーIDと試験IDを入力してください。'
        )
    label1.pack()

    label2 = tk.Label(text='ユーザーID')
    label2.place(x=140, y=120)

    txt1 = tk.Entry(width=35)
    txt1.place(x=230, y=120)

    label3 = tk.Label(text='試験ID')
    label3.place(x=140, y=170)

    txt2 = tk.Entry(width=35)
    txt2.place(x=230, y=170)
    # button
    button1 = tk.Button(
        tki,
        text='OK',
        command=bind_ids
        )
    button1.place(x=260, y=300)

    tki.mainloop()
	
    #末尾のtabを削除
    return exam_id.strip(), examinee_id.strip()
	
