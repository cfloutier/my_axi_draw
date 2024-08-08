#!/usr/bin/env python
import time
from pyaxidraw import axidraw
from config import SETTINGS, build_plot_ad
import pen_commands as pen

import tkinter as tk
from tkinter import ttk

def set():
    print("Hello World")

class PenControl(tk.LabelFrame):
    
    def __init__(self, parent ):
        tk.LabelFrame.__init__(self, parent, text="Pen Tools")

        h_bt=3
        w_bt=20

        button = tk.Button(self, text = "Toggle", command = pen.toggle_pen, width=w_bt, height=h_bt)
        button.pack(fill="x", padx=10, pady=5)
        button = tk.Button(self, text = "Pen Up", command = pen.pen_up, width=w_bt, height=h_bt)
        button.pack(fill="x", padx=10, pady=5)
        button = tk.Button(self, text = "Pen Down", command = pen.pen_down, width=w_bt, height=h_bt)
        button.pack(fill="x", padx=10, pady=5)

class PenSettingsUI(tk.LabelFrame):

    def __init__(self, parent ):
        tk.LabelFrame.__init__(self, parent, bg="red", text="Pen Settings", height=500)

        self.pen_up_v = tk.IntVar()
        self.pen_down_v = tk.IntVar()

        h_bt=3
        w_bt=20

        self.grid_rowconfigure(0, minsize=500, weight=1)
        self.grid_rowconfigure(0, minsize=500, weight=1)

        scale_u = tk.Scale(self, label = "Pen Up Height", from_=0, to=100)
        
        scale_u.grid( padx=5, pady=5, column=0, row=0 )

        scale_d = tk.Scale(self, label = "Pen Down Height", from_=0, to=100)
        scale_d.grid( padx=5, pady=5, column=1, row=0, )


        # button.pack(fill="x", padx=10, pady=5)
        # button = tk.Button(self, text = "Pen Up", command = pen_up, width=w_bt, height=h_bt)
        # button.pack(fill="x", padx=10, pady=5)
        # button = tk.Button(self, text = "Pen Down", command = pen_down, width=w_bt, height=h_bt)
        # button.pack(fill="x", padx=10, pady=5)

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.minsize(800,600)

        # Adding a title to the window
        self.wm_title("My Axi Draw - Paperflou tools")
        self.geometry="400x600"

        # creating a frame and assigning it to container
        pen_control  = PenControl(self)

        # specifying the region where the frame is packed in root
        pen_control.pack( fill="none", side="left")

        pen_settings = PenSettingsUI(self)
        pen_settings.pack( fill="both", side="right", anchor="ne")


def main():   
    # load default settings
    SETTINGS.load()
    app = MainWindow()
    
    app.mainloop()

if __name__ == "__main__":
    main()