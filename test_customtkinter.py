from config import SETTINGS
import customtkinter

class PenButtons(customtkinter.CTkFrame):


    def on_click(self):
        print("clic")


    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toggle_bt = customtkinter.CTkButton(self, text="Toggle", command=self.on_click)
        self.toggle_bt.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.up_bt = customtkinter.CTkButton(self, text="Pen Up", command=self.on_click)
        self.up_bt.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.up_bt = customtkinter.CTkButton(self, text="Pen Down", command=self.on_click)
        self.up_bt.grid(row=3, column=0, padx=10, pady=10, sticky="ew")


class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Trace")
        self.add("Pen")

        # add widgets on tabs
        self.label = customtkinter.CTkLabel(master=self.tab("Trace"), text="To DO")
        self.label.grid(row=0, column=0, padx=20, pady=10)

        self.pen_buttons = PenButtons(self.tab("Pen"))
        self.pen_buttons.grid(row=0, column=0, padx=20, pady=10)


        self.set("Pen")

class MainWindow(customtkinter.CTk):



    def __init__(self):

        super().__init__()

        self.title("my app")
        self.geometry("800x600")

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

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