from settings import SETTINGS
import customtkinter as ctk

from pen_commands import TRACER
from tools.ctk.base_frame import BaseFrame

class PenPage():
    def __init__(self, frame:ctk.CTkFrame):
        
        self.frame = frame
        frame.grid_columnconfigure(1, weight=5)
        frame.grid_rowconfigure(1, weight=2)

        self.pen_buttons = PenButtons(frame)
        self.pen_buttons.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        self.pen_settings = PenSettings(frame)
        self.pen_settings.grid(row=1, column=1, padx=20, pady=10, sticky="new")

        # self.pen_settings = SpeedPage(frame)
        # self.pen_settings.grid(row=2, column=1, padx=20, pady=10, sticky="new")

class PenButtons(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.toggle_bt = ctk.CTkButton(self, text="Toggle", command = TRACER.toggle_pen)
        self.toggle_bt.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.up_bt = ctk.CTkButton(self, text="Pen Up", command= TRACER.pen_up)
        self.up_bt.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.up_bt = ctk.CTkButton(self, text="Pen Down", command=TRACER.pen_down)
        self.up_bt.grid(row=3, column=0, padx=10, pady=10, sticky="ew")


class PenSettings(BaseFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, label="Pen Settings", **kwargs, width=500)

        self.pen_up_value = ctk.IntVar()
        self.pen_down_value = ctk.IntVar()
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
        self.applyTexts()

    def on_auto(self):

        if (self.auto_move.get()):
            self.set_height()
        # pass

    def set_height(self):

        if not self.auto_move.get():
            return
        
        if self.prev_up != SETTINGS.pen_pos_up:
            self.prev_up = SETTINGS.pen_pos_up
            TRACER.pen_up()

        if self.prev_down != SETTINGS.pen_pos_down:
            self.prev_down = SETTINGS.pen_pos_down
            TRACER.pen_down()

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
            SETTINGS._save()