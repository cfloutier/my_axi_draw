from pathlib import Path
from settings import PLOTTER_PARAMS, SHORTCUTS
from tools.ctk.base_frame import BaseFrame
import customtkinter as ctk

from tools.nested_dict import find_value
from tools.svg_editor import create_page


models_combo_values = {
    1: "AxiDraw V2 or V3",
    2: "AxiDraw V3/A3 or SE/A3",
    3: "AxiDraw V3 XLX",
    4: "AxiDraw MiniKit",
    5: "AxiDraw SE/A1",
    6: "AxiDraw SE/A2",
}

pages = {
    "A6": (105, 148.5),
    "A5": (148.5, 210),
    "A4": (210, 297),
    "A3": (297, 420),
    "A2": (420, 594),
}


class CalibrationPage(ctk.CTkFrame):
    """frame with the pen settings"""

    def __init__(self, master: ctk.CTkFrame, **kwargs):
        super().__init__(master)

        # super().__init__(master, label="Speed Settings", **kwargs, width=500)

        self.calibration_frame = BaseFrame(self, label="Calibration")
        self.calibration_frame.grid(row=0, column=0, sticky="nes", pady=5, padx=(5, 10))
        # master.grid_columnconfigure(0, weight=1)

        # self.calibration_frame.grid(row=0, column=0, sticky="new")

        self.model_combo = self.calibration_frame.combo(
            "AxiDraw Model : ",
            values=list(models_combo_values.values()),
            command=self.on_model_changed,
            inline=False,
        )

        self.model_combo.set(models_combo_values[PLOTTER_PARAMS.model])

        self.res_factor_edit = self.calibration_frame.number_edit(
            label="native res factor",
            value=PLOTTER_PARAMS.native_res_factor,
            int_mode=False,
            on_change=self.on_res_changed,
        )

        self.test_page = BaseFrame(self, label="Test_Page")
        self.test_page.grid(row=0, column=1, sticky="news", pady=5, padx=(10, 5))

        self.test_page.label("Test calibration by drawing a frame")
        self.pages_combo = self.test_page.combo(
            "Pages : ",
            values=list(pages.keys()),
            command=self.on_page_change,
        )
        self.pages_combo.set("A4")

        self.page_x_size = self.test_page.number_edit(
            label="page x size (mm)", value=210, int_mode=False
        )
        self.page_y_size = self.test_page.number_edit(
            label="page y size (mm)", value=297, int_mode=False
        )

        self.corner_size_label = self.test_page.label(text="corner size (mm)")

        self.corner_size = ctk.IntVar(self, 50)
        self.corner_size_slider = self.test_page.slider(
            from_=0, to=200, variable=self.corner_size, command=self.applyTexts
        )

        self.test_page.Button("Trace Page", self.trace_page)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=10)

        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=0)
        # self.test = self.label("value = ?")

        self.pack(side="left", fill="both", anchor="ne", expand=True)

        self.applyTexts()

    def applyTexts(self, value=None):

        self.corner_size_label.configure(
            text=f"Corner Size : {self.corner_size.get()} mm"
        )

    def on_page_change(self, value):

        if not value in pages:
            return

        sizes = pages[value]
        self.page_x_size.set(sizes[0])
        self.page_y_size.set(sizes[1])

    def on_res_changed(self, value):

        PLOTTER_PARAMS.native_res_factor = value
        PLOTTER_PARAMS._save()

    def on_model_changed(self, model_name):

        model_index = find_value(models_combo_values, model_name)
        if model_index:
            PLOTTER_PARAMS.model = model_index
            PLOTTER_PARAMS._save()

    def trace_page(self):

        size = (self.page_x_size.get(), self.page_y_size.get())
        svg_template_path = Path(__file__).parent.parent / "svg_templates"
        create_page(svg_template_path / "temp.svg", size, self.corner_size.get())

        SHORTCUTS.trace.load_svg(svg_template_path / "temp.svg")
        SHORTCUTS.trace.run()
