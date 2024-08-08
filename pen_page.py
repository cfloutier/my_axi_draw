from config import SETTINGS
import customtkinter

import pen_commands as pen

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

class PenSettings(customtkinter.CTkFrame):


    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, width=500, border_width=1, border_color="white")

        self.pen_up_value = customtkinter.IntVar()
        self.pen_down_value = customtkinter.IntVar()
        # self.set_

        label_frame = customtkinter.CTkLabel(self, text="Pen Settings", bg_color="transparent")
        label_frame.place(x = 5, y = -7, anchor="nw")

        self.grid_columnconfigure(0, weight=1)
        row = 0

        self.auto_move = customtkinter.CTkSwitch(self, text="Auto Apply", command=self.on_auto)
        self.auto_move.grid(row=row, column=0, padx=10, pady=(15,5), sticky="w")
        row+=1

        self.pen_up_label = customtkinter.CTkLabel(self, text="pen up : ", justify="left")
        self.pen_up_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        row+=1

        self.pen_up = customtkinter.CTkSlider(self, from_= 0, to=100, variable=self.pen_up_value, command=self.apply)
        self.pen_up.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        row += 1

        self.pen_down_label = customtkinter.CTkLabel(self, text="pen down : ", justify="left")
        self.pen_down_label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        row += 1

        self.pen_down = customtkinter.CTkSlider(self, from_= 0, to=100, variable=self.pen_down_value, command=self.apply)
        self.pen_down.grid(row=row, column=0, padx=10, pady=5, sticky="ew")

        self.prev_up = SETTINGS.pen_pos_up
        self.prev_down = SETTINGS.pen_pos_down

        self.set()
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
        
    def apply(self, value=None):

        SETTINGS.pen_pos_up = self.pen_up_value.get()
        SETTINGS.pen_pos_down = self.pen_down_value.get()

        self.pen_up_label.configure(text=f"pen up : {SETTINGS.pen_pos_up}")
        self.pen_down_label.configure(text=f"pen down : {SETTINGS.pen_pos_down}")

        SETTINGS.save()