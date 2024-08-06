#!/usr/bin/env python
import time
from pyaxidraw import axidraw
from config import SETTINGS
    
def toggle_pen():
    ad = build_plot_ad()
    ad.options.mode = "toggle"
    ad.plot_run()          # Execute the command

def pen_up():
    ad = build_plot_ad()
    ad.options.mode = "manual"
    ad.options.manual_cmd  = "raise_pen"
    ad.plot_run()          # Execute the command

def pen_down():
    ad = build_plot_ad()
    ad.options.mode = "manual"
    ad.options.manual_cmd  = "lower_pen"

    # print(ad.options.__dict__)

    ad.plot_run()          # Execute the command

import tkinter as tk
from tkinter import ttk

def set():
    print("Hello World")

class PenControl(tk.LabelFrame):
    
    def __init__(self, parent ):
        tk.LabelFrame.__init__(self, parent, bg="red", text="Pen Tools")

        h_bt=3
        w_bt=20

        button = tk.Button(self, text = "Toggle", command = toggle_pen, width=w_bt, height=h_bt)
        button.pack(fill="x", padx=10, pady=5)
        button = tk.Button(self, text = "Pen Up", command = pen_up, width=w_bt, height=h_bt)
        button.pack(fill="x", padx=10, pady=5)
        button = tk.Button(self, text = "Pen Down", command = pen_down, width=w_bt, height=h_bt)
        button.pack(fill="x", padx=10, pady=5)


class PenSettingsUI(tk.LabelFrame):

    def __init__(self, parent ):
        tk.LabelFrame.__init__(self, parent, bg="red", text="Pen Settings")

        self.pen_up_v = tk.IntVar()
        self.pen_down_v = tk.IntVar()

        h_bt=3
        w_bt=20

        scale_u = tk.Scale(self, text = "Pen Up Height", from_=0, to=100)
        scale_d = tk.Scale(self, text = "Pen Down Height", from_=0, to=100)



        button.pack(fill="x", padx=10, pady=5)
        button = tk.Button(self, text = "Pen Up", command = pen_up, width=w_bt, height=h_bt)
        button.pack(fill="x", padx=10, pady=5)
        button = tk.Button(self, text = "Pen Down", command = pen_down, width=w_bt, height=h_bt)
        button.pack(fill="x", padx=10, pady=5)

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        # Adding a title to the window
        self.wm_title("My Axi Draw - Paperflou tools")
        self.geometry="400x600"


        # creating a frame and assigning it to container
        container = PenControl(self)

        # specifying the region where the frame is packed in root
        container.pack( fill="both")

def main():   
    # load default settings
    SETTINGS.load()
    app = MainWindow()
    
    app.mainloop()

if __name__ == "__main__":
    main()