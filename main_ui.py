from settings import SETTINGS, INTERNAL_SETTINGS
import globals

import tkinter as tk
import customtkinter as ctk
from pen_page import PenPage
from speed_page import SpeedPage
from settings_frame import SettingsFrame
from trace_page import TracePage

class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.trace_tab = self.add("Trace")
        self.pen_tab = self.add("Pen")
        self.speed_tab = self.add("Speed")

        # add widgets on tabs
        self.trace_page = TracePage(self.trace_tab)

        self.pen_page = PenPage(self.pen_tab)
        self.speed_page = SpeedPage(self.speed_tab)
        
        self.set("Trace")

class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("My Axi Draw - Paperflou Tools")
        self.geometry("800x600")

        self.last_log = None

        # add the setting frame (one line)
        self.settings_frame = SettingsFrame(self)
        self.settings_frame.pack(side="top", fill="both")

        self.tab_view = TabView(master=self, height=900)
        self.tab_view.pack(side="top", fill="both", padx=1, pady=1)

    def refresh_ui(self):
        self.tab_view.pen_page.pen_settings.set()
        self.tab_view.speed_page.set()


    def log(self, txt):
        if self.last_log == txt:
            return
        
        self.last_log = txt
        self.tab_view.trace_page.log(txt)
        print("log: " + txt)

def main():
    # load default settings
    # from PIL import ImageTk

    INTERNAL_SETTINGS.load()
    SETTINGS.load()

    globals.main_app = MainWindow()
    globals.main_app.refresh_ui()

    photo = tk.PhotoImage(file = 'icon.png')
    globals.main_app.wm_iconphoto(False, photo)
    globals.main_app.wm_iconbitmap()
    
    # globals.main_app.after(300, lambda: globals.main_app.wm_iconphoto(False, photo))

    globals.main_app.mainloop()

if __name__ == "__main__":
    main()