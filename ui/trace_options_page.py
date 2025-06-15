from tools.nested_dict import find_value
from settings import SETTINGS
from tools.ctk.base_frame import BaseFrame
import customtkinter as ctk

reordering_combo_values = {0: "Least", 1: "Basic", 2: "Full", 4: "None"}

reordering_details_values = {
    0: "Only connect adjoining paths (Default)",
    1: "Also reorder paths for speed",
    2: "Full Also allow path reversal",
    4: "Strictly preserve file order",
}


class TraceOptionsPage(BaseFrame):
    def __init__(self, master: ctk.CTkFrame, **kwargs):
        super().__init__(master, label="Trace Settings", **kwargs, width=500)
        master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="n")

        self.reordering = self.combo(
            "Reordering : ",
            values=list(reordering_combo_values.values()),
            command=self.on_order_changed,
            inline=False,
        )

        self.reordering_detail = self.label(text="-")
        self.clip_to_page = self.switch(
            text="Clip plotting area to SVG document size", command=self.apply
        )
        self.auto_rotate = self.switch(
            text="Auto-select portrait vs landscape orientation", command=self.apply
        )

        self.hiding = self.switch(
            text="Auto hide lines behing polygons", command=self.apply
        )

        # read conf
        self.set()

    def set(self):
        self.reordering.set(reordering_combo_values[SETTINGS.reordering])
        self.clip_to_page.set(SETTINGS.clip_to_page)
        self.auto_rotate.set(SETTINGS.auto_rotate)
        self.hiding.set(SETTINGS.hiding)

        self.applyTexts()

    def on_order_changed(self, model_name):

        order_index = find_value(reordering_combo_values, model_name)
        # print(f"order_index = {order_index} ")
        if order_index != SETTINGS.reordering:
            SETTINGS.reordering = order_index
            SETTINGS._save()
            self.applyTexts()

    def applyTexts(self):
        detail = reordering_details_values.get(SETTINGS.reordering, "-")
        self.reordering_detail.configure(text=detail)

    def apply(self, value=None):

        changed = False

        if SETTINGS.clip_to_page != self.clip_to_page.get():
            SETTINGS.clip_to_page = self.clip_to_page.get()
            changed = True

        if SETTINGS.auto_rotate != self.auto_rotate.get():
            SETTINGS.auto_rotate = self.auto_rotate.get()
            changed = True

        if SETTINGS.hiding != self.hiding.get():
            SETTINGS.hiding = self.hiding.get()
            changed = True

        if changed:
            SETTINGS._save()
            self.applyTexts()
