from config import SETTINGS
import customtkinter
from pen_page import PenPage


class MyTabView(customtkinter.CTkTabview):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.trace_tab = self.add("Trace")
        self.pen_tab = self.add("Pen", )

        # add widgets on tabs
        self.label = customtkinter.CTkLabel(master=self.trace_tab, text="To DO")
        self.label.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        self.pen_page = PenPage(self.pen_tab)
        
        self.set("Pen")

class MainWindow(customtkinter.CTk):

    def __init__(self):

        super().__init__()

        self.title("My Axi Draw - Paperflou Tools")
        self.geometry("800x600")

        # self.grid_columnconfigure(index=0,)

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=5, pady=5, sticky="news")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # self.checkbox_frame = customtkinter.CTkFrame(self)
        # self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        # self.checkbox_1 = customtkinter.CTkCheckBox(self.checkbox_frame, text="checkbox 1")
        # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        # self.checkbox_2 = customtkinter.CTkCheckBox(self.checkbox_frame, text="checkbox 2")
        # self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        
        

def main():   
    # load default settings
    SETTINGS.load()
    app = MainWindow()
    
    app.mainloop()

if __name__ == "__main__":
    main()