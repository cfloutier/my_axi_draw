import logging
import customtkinter as ctk


class Int_Edit:
    def __init__(
        self,
        parent: ctk.CTkFrame,
        value: float | int = 0,
        int_mode=True,
        on_change=None,
    ):

        self.parent = parent

        self.on_change = on_change
        self.int_mode = int_mode

        self.number_value: int | float = value

        if self.int_mode:
            self.number_value = int(value)
        else:
            self.number_value = float(value)

        self.str_value = ctk.StringVar(parent, str(self.number_value))
        self.edit_box = ctk.CTkEntry(parent, width=200, textvariable=self.str_value)

        self.str_value.trace_add("write", self.on_entry_change)

        # self.edit_box.bind(command=self.on_change)

    def on_entry_change(self, *args):

        if not self.str_value.get():
            return

        try:

            if self.int_mode:
                self.number_value = int(self.str_value.get())
            else:
                self.number_value = float(self.str_value.get())

            if self.on_change:
                self.on_change(self.number_value)

            self.edit_box.configure(text_color="white")
        except:
            # refuse, reset with int value
            # self.str_value.set(str(self.int_value))
            logging.warning("invalid value " + self.str_value.get())
            self.edit_box.configure(text_color="darkred")
            pass

    def get(self) -> int:
        return self.number_value

    def set(self, value: int):

        if value == self.number_value:
            return

        self.number_value = value
        self.str_value.set(value)
        if self.on_change:
            self.on_change(self.number_value)
