from config import SETTINGS
import customtkinter

import pen_commands as pen
from tools.ctk.separator import CTkWindowSeparator

class PenPage():
    def __init__(self, frame:customtkinter.CTkFrame):
        
        self.frame = frame
        frame.grid_columnconfigure(1, weight=5)
        frame.grid_rowconfigure(1, weight=2)

        self.pen_buttons = PenButtons(frame)
        self.pen_buttons.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        self.pen_settings = PenSettings(frame)
        self.pen_settings.grid(row=1, column=1, padx=20, pady=10, sticky="new")


class PenButtons(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toggle_bt = customtkinter.CTkButton(self, text="Toggle", command = pen.toggle_pen)
        self.toggle_bt.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.up_bt = customtkinter.CTkButton(self, text="Pen Up", command= pen.pen_up)
        self.up_bt.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.up_bt = customtkinter.CTkButton(self, text="Pen Down", command=pen.pen_down)
        self.up_bt.grid(row=3, column=0, padx=10, pady=10, sticky="ew")


class BaseFrame(customtkinter.CTkFrame):
    """ a base class for frames using vertical grid"""

    def __init__(self, master, label, **kwargs):
        super().__init__(master, **kwargs)
        pass
    
        self.row = 0

        if label:
            label_frame = customtkinter.CTkLabel(self, text=label)
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

        sw = customtkinter.CTkSwitch(self, text=text, command=command)
        sw.grid(row=self.row, column=0, padx=self.padx, pady=self.pady, sticky="w")
        self.row += 1

        return sw
    
    def label(self, text):

        sw = customtkinter.CTkLabel(self, text=text, justify="left")
        sw.grid(row=self.row, column=0, padx=self.padx, pady=self.pady, sticky="w")
        self.row += 1

        return sw
    
    def slider(self, from_, to, variable = None, command = None):

        slider_ = customtkinter.CTkSlider(self, from_= from_, to=to)


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

class PenSettings(BaseFrame):


    def __init__(self, master, **kwargs):
        super().__init__(master, label="Pen Settings", **kwargs, width=500)

        self.pen_up_value = customtkinter.IntVar()
        self.pen_down_value = customtkinter.IntVar()
        # self.set_

        self.auto_move = self.switch(text="Auto Apply", command=self.on_auto)
        self.pen_up_label = self.label(text="pen up : ")

        self.pen_up = self.slider(from_= 0, to=100, variable=self.pen_up_value, command=self.apply)
        self.pen_down_label = self.label(text="pen down : ")

        self.pen_down = self.slider(from_= 0, to=100, variable=self.pen_down_value, command=self.apply)
      
        self.separator()

        self.prev_up = SETTINGS.pen_pos_up
        self.prev_down = SETTINGS.pen_pos_down

        # read conf
        self.set()
        # set text and config
        self.apply()

    def on_auto(self):

        if (self.auto_move.get()):
            self.set_height()
        # pass

    def set_height(self):

        if not self.auto_move.get():
            return
        
        if self.prev_up != SETTINGS.pen_pos_up:
            self.prev_up = SETTINGS.pen_pos_up
            pen.pen_up()

        if self.prev_down != SETTINGS.pen_pos_down:
            self.prev_down = SETTINGS.pen_pos_down
            pen.pen_down()

        self.after(500, self.set_height)

    def set(self):
        self.pen_up_value.set(SETTINGS.pen_pos_up)
        self.pen_down_value.set(SETTINGS.pen_pos_down)

    def applyTexts(self):

        self.pen_up_label.configure(text=f"pen up : {SETTINGS.pen_pos_up}")
        self.pen_down_label.configure(text=f"pen down : {SETTINGS.pen_pos_down}")
        
    def apply(self, value=None):

        changed = False

        if SETTINGS.pen_pos_up != self.pen_up_value.get():
            SETTINGS.pen_pos_up = self.pen_up_value.get()
            changed = True

        if SETTINGS.pen_pos_down != self.pen_down_value.get():
            SETTINGS.pen_pos_down = self.pen_down_value.get()
            changed = True

        if changed:
            self.applyTexts()
            SETTINGS.save()