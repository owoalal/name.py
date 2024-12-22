import os
import re
import sys
import tkinter as tk
from tkinter import *



R = {"path": [r"C:\Users\mhd\Downloads\imagepython", r"C:\Users\mhd\Downloads\sound1", r"C:\Users\mhd\Downloads\rest"]}


windows = tk.Tk()
windows.title("file organiser")
windows.geometry("1000x600")
windows.config(bg=None , cursor="arrow" , relief="sunken" , borderwidth=10 ,)
windows.resizable(width=False, height=False)

windows.mainloop()





while True:
    def imagefile():
        if not os.path.exists(R ["path"][0]):
            os.mkdir(R ["path"][0])
        else:
            print(f"folder already exist:", R ["path"][0])


    def soundfile():
        if not os.path.exists(R ["path"][1]):
            os.mkdir(R ["path"][1])
        else:
            print(f"folder already exist:", R ["path"][1])



    def restfile():
        if not os.path.exists(R ["path"][2]):
            os.mkdir(R ["path"][2] )
        else:
            print(f"folder already exist:", R ["path"][2])

    break

