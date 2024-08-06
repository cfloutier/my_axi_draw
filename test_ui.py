#!/usr/bin/env python
import time
from pyaxidraw import axidraw

def toggle_pen():
    ad = axidraw.AxiDraw() # Create class instance
    ad.plot_setup()        # Run setup without input file
    ad.options.mode = "toggle"
    ad.plot_run()          # Execute the command

def up():
    ad = axidraw.AxiDraw() # Create class instance
    ad.plot_setup()        # Run setup without input file
    ad.options.mode = "toggle"
    ad.plot_run()          # Execute the command

import tkinter as tk
from tkinter import ttk

def set():
    print("Hello World")

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Adding a title to the window
        self.wm_title("My Axi Draw - Paperflou tools")

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=400, width=600)

        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        button = tk.Button(self, text = "Toggle", command = toggle_pen)
        button.pack()

def main():   

    testObj = MainWindow()
    testObj.mainloop()

if __name__ == "__main__":
    main()