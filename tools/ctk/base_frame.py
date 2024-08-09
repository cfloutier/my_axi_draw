import customtkinter as ctk
from tools.ctk.separator import CTkWindowSeparator 

class BaseFrame(ctk.CTkFrame):
    """ a base class for frames using vertical grid"""

    def __init__(self, master, label, **kwargs):
        super().__init__(master, **kwargs)
        pass
    
        self.row = 0

        if label:
            label_frame = ctk.CTkLabel(self, text=label)
            self.configure(border_width=1, border_color="white")
            label_frame.place(x = 5, y = -7, anchor="nw")

        # only one column here
        self.grid_columnconfigure(0, weight=1)

    @property
    def padx(self):
        return 5 

    @property
    def pady(self):
        if self.row == 0:
            return (15,5)
        return 5 

    def switch(self, text, command):

        sw = ctk.CTkSwitch(self, text=text, command=command)
        sw.grid(row=self.row, column=0, padx=self.padx, pady=self.pady, sticky="w")
        self.row += 1

        return sw
    
    def label(self, text):

        sw = ctk.CTkLabel(self, text=text, justify="left")
        sw.grid(row=self.row, column=0, padx=self.padx, pady=self.pady, sticky="w")
        self.row += 1

        return sw
    
    def slider(self, from_, to, variable = None, command = None):

        slider_ = ctk.CTkSlider(self, from_= from_, to=to)


        if variable:
            slider_.configure(variable=variable)

        if command:
            slider_.configure(command=command)

        slider_.grid(row=self.row, column=0, padx=10, pady=5, sticky="ew")
        self.row += 1

        return slider_
    
    def separator(self):

        sep = CTkWindowSeparator(self, length = 200)
        sep.grid(row=self.row, column=0, padx=10, pady=5, sticky="ew")
        self.row += 1

        return sep
