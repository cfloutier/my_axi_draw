import tkinter
import customtkinter as ctk
from tools.ctk.separator import Separator 

class Switch(ctk.CTkSwitch):

    def set(self, value: bool):

        if value:
            self.select()
        else:
            self.deselect()
        
class BaseFrame(ctk.CTkFrame):
    """ a base class for frames using vertical grid"""

    def __init__(self, master, label = None, **kwargs):
        super().__init__(master, **kwargs)
        pass
    
        self.row = 0
        self.col = 0

        self._padx = 5
        self._pady = 5

        if label:
            self.first_pad_y = (15, self._pady)
            label_frame = ctk.CTkLabel(self, text=label)
            self.configure(border_width=1, border_color="white")
            label_frame.place(x = 5, y = -7, anchor="nw")
        else:
            self.first_pad_y = self._pady

        # only one column here
        self.grid_columnconfigure(1, weight=1)

    def next_line(self):
        self.row += 1
        self.col = 0

    @property
    def padx(self):
        return self._padx 

    @property
    def pady(self):
        if self.row == 0:
            return self.first_pad_y
        
        return self._pady

    def switch(self, text, command):
        sw = Switch(self, text=text, command=command)
        sw.grid(row=self.row, column=0, padx=self.padx, pady=self.pady, sticky="w")
        self.next_line()
        
        return sw
    
    def Button(self, text, command, inline = False, width=150):   
        sw = ctk.CTkButton(self, text=text, command=command, width=width)
        if inline:
            sw.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky="w")
            self.col += 1
        else:
            self.col = 0
            sw.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky="w")
            self.row += 1

        return sw

    def Combo(self, label, values, command, inline = False):
        label_ = ctk.CTkLabel(self, text=label, justify="left")
        label_.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky="w")
        self.col += 1
        combo = ctk.CTkComboBox(self, values=values, command=command)
        combo.grid(row=self.row, column=self.col, padx=self.padx, pady=self.pady, sticky="w")
        if not inline:
            self.next_line()
        else:
            self.col += 1

        return combo

    
    def label(self, text):

        sw = ctk.CTkLabel(self, text=text, justify="left")
        sw.grid(row=self.row, column=0, columnspan=2,  padx=self.padx, pady=self.pady, sticky="w")
        self.next_line()
        

        return sw
    
    def slider(self, from_, to, variable = None, command = None):

        slider_ = ctk.CTkSlider(self, from_= from_, to=to)

        if variable:
            slider_.configure(variable=variable)

        if command:
            slider_.configure(command=command)

        slider_.grid(row=self.row, column=0, columnspan=2, padx=self.padx, pady=5, sticky="ew")
        self.next_line()
        

        return slider_
    
    def separator(self):

        sep = Separator(self, length = 200)
        sep.grid(row=self.row, column=0, columnspan=2, padx=30, pady=10, sticky="ew")
        self.next_line()
        
        return sep
