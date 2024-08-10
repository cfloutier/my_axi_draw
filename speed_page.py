
from settings import SETTINGS
from tools.ctk.base_frame import BaseFrame
import customtkinter as ctk

class SpeedPage(BaseFrame):
    def __init__(self, master: ctk.CTkFrame, **kwargs):
        super().__init__(master, label="Speed Settings", **kwargs, width=500)
        master.grid_columnconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky="new")

        self.speed_pendown_l = self.label(text="-")
        self.speed_pendown = self.slider(from_= 1, to=100, command=self.apply)

        self.speed_penup_l = self.label(text="-")
        self.speed_penup = self.slider(from_= 1, to=100, command=self.apply)

        self.accel_l = self.label(text="-")
        self.accel = self.slider(from_= 1, to=100, command=self.apply)

        self.pen_rate_raise_l = self.label(text="-")
        self.pen_rate_raise = self.slider(from_= 1, to=100, command=self.apply)

        self.pen_rate_lower_l = self.label(text="-")
        self.pen_rate_lower = self.slider(from_= 1, to=100, command=self.apply)

        self.const_speed = self.switch(text="Use constant velocity mode when pen is down", command=self.apply)

        # read conf
        self.set()
        # set text and config
        self.applyTexts()


    def set(self):
        self.speed_pendown.set(SETTINGS.speed_pendown)
        self.speed_penup.set(SETTINGS.speed_penup)

        self.accel.set(SETTINGS.accel)        
        self.pen_rate_raise.set(SETTINGS.pen_rate_raise)
        self.pen_rate_lower.set(SETTINGS.pen_rate_lower)        
        self.const_speed.set(SETTINGS.const_speed)     

    def applyTexts(self):

        self.speed_pendown_l.configure(text=f"Maximum plotting speed : {int(SETTINGS.speed_pendown)} (25)")
        self.speed_penup_l.configure(text=f"Maximum transit speed : {int(SETTINGS.speed_penup)} (75)")

        self.accel_l.configure(text=f"Acceleration rate factor : {int(SETTINGS.accel)} (75)")
        self.pen_rate_raise_l.configure(text=f"Rate of raising pen : {int(SETTINGS.pen_rate_raise)} (75)")
        self.pen_rate_lower_l.configure(text=f"Rate of lowering pen : {int(SETTINGS.pen_rate_lower)} (50)")

    
    def apply(self, value=None):

        changed = False

        if SETTINGS.speed_pendown != self.speed_pendown.get():
            SETTINGS.speed_pendown = self.speed_pendown.get()
            changed = True

        if SETTINGS.speed_penup != self.speed_penup.get():
            SETTINGS.speed_penup = self.speed_penup.get()
            changed = True

        if SETTINGS.accel != self.accel.get():
            SETTINGS.accel = self.accel.get()
            changed = True

        if SETTINGS.pen_rate_raise != self.pen_rate_raise.get():
            SETTINGS.pen_rate_raise = self.pen_rate_raise.get()
            changed = True

        if SETTINGS.pen_rate_lower != self.pen_rate_lower.get():
            SETTINGS.pen_rate_lower = self.pen_rate_lower.get()
            changed = True

        if SETTINGS.const_speed != self.const_speed.get():
            SETTINGS.const_speed = self.const_speed.get()
            changed = True

        if changed:
            self.applyTexts()
            SETTINGS._save()

