from settings import SETTINGS, INTERNAL_SETTINGS
import customtkinter as ctk
from pen_page import PenPage
from speed_page import SpeedPage
from settings_page import SettingsFrame

app = None

class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.trace_tab = self.add("Trace")
        self.pen_tab = self.add("Pen")
        self.speed_tab = self.add("Speed")

        # add widgets on tabs
        self.label = ctk.CTkLabel(master=self.trace_tab, text="To DO")
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        self.pen_page = PenPage(self.pen_tab)
        self.speed_page = SpeedPage(self.speed_tab)
        
        self.set("Settings")

class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        global app
        app = self

        self.title("My Axi Draw - Paperflou Tools")
        self.geometry("800x600")

        # self.grid_columnconfigure(index=0,)

        
        # center is full page
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        # add the tab view
        # self.tab_view.grid(row=0, column=0, padx=5, pady=5, sticky="news")
        

        # add the setting page
        self.settings_page = SettingsFrame(app, self)
        self.settings_page.pack(side="top", fill="x")

        self.tab_view = TabView(master=self)
        self.tab_view.pack(fill="x", padx=20)

        # self.checkbox_frame = ctk.CTkFrame(self)
        # self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        # self.checkbox_1 = ctk.CTkCheckBox(self.checkbox_frame, text="checkbox 1")
        # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        # self.checkbox_2 = ctk.CTkCheckBox(self.checkbox_frame, text="checkbox 2")
        # self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

    def load_settings(self):
        self.tab_view.pen_page.pen_settings.set()
        self.tab_view.speed_page.set()


def main():   
    # load default settings
    
    INTERNAL_SETTINGS.load()
    SETTINGS.load()

    MainWindow()
    app.load_settings()
    
    app.mainloop()

if __name__ == "__main__":
    main()