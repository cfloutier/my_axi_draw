from datetime import timedelta
from enum import Enum
import customtkinter as ctk
import time
import tkinter
from globals import my_log
from settings import INTERNAL_SETTINGS
from plotter import PLOTTER, Status
from tools.ctk.base_frame import BaseFrame
from tools.ctk.progress_bar import ProgressBar
from tools.time import td_format


class TracePage(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame):
        super().__init__(master)

        self.buttons_bar = BaseFrame(self)

        self.load_bt = self.buttons_bar.Button("Load svg", command=self.load_svg)
        self.load_bt = self.buttons_bar.Button("Reload", command=self.reload_last)

        self.run_bt = self.buttons_bar.Button("Run", command=self.run)
        self.pause_bt = self.buttons_bar.Button("Pause", command=PLOTTER.pause)
        self.stop_bt = self.buttons_bar.Button("Stop", command=PLOTTER.stop)
        self.disable_bt = self.buttons_bar.Button(
            "Disable XY", command=self.disable_motors
        )

        self.status_label = self.buttons_bar.label("iddle")

        self.buttons_bar.grid(
            row=0, column=0, rowspan=2, sticky="ne", pady=5, padx=(5, 10)
        )
        self.report = ctk.CTkTextbox(master=self, width=20)
        self.report.grid(row=0, column=1, sticky="news")

        # self.report.pack(side="left", fill="both", expand=True, anchor="nsew")

        self.progress = ProgressBar(self, height=20)
        # self.progress.pack(expand=True, side = "bottom", pady=5)
        self.progress.grid(row=1, column=1, sticky="new", pady=5)
        self.progress.set_with_text(0, "")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=10)

        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=0)

        self.pack(side="left", fill="both", expand=True)

        PLOTTER.status_listenners.append(self.on_status)

        if INTERNAL_SETTINGS.auto_load_svg:
            self.load_svg(INTERNAL_SETTINGS.auto_load_svg)

        self.update_status()

    def load_svg(self, filename=None):
        if not filename:
            filename = ctk.filedialog.askopenfilename(
                initialdir=INTERNAL_SETTINGS.svg_path,
                defaultextension=".svg",
                filetypes=(("svg file", "*.svg"), ("All files", "*.*")),
            )

        if filename:
            self.report.insert(tkinter.END, "Loading in progress\n")
            INTERNAL_SETTINGS.svg_file = filename
            PLOTTER.preload(filename)

    def reload_last(self):
        if INTERNAL_SETTINGS.svg_file:
            self.load_svg(INTERNAL_SETTINGS.svg_file)

    def run(self):

        if not INTERNAL_SETTINGS.svg_file:
            return

        PLOTTER.draw(INTERNAL_SETTINGS.svg_file)

    def on_status(self, status: Status):

        # print(f"set_status {status}")

        self.status_label.configure(text=status.name)

        if (
            status == Status.Pausing
            or status == Status.Stopping
            or status == Status.Homing
            or status == Status.Preview
        ):

            # Disable all buttons
            self.load_bt.configure(state="disabled")
            self.pause_bt.configure(state="disabled")
            self.run_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")
            self.disable_bt.configure(state="disabled")

        elif status == Status.Ready:

            self.load_bt.configure(state="normal")

            self.run_bt.configure(state="normal", text="Run")

            self.pause_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")

            self.disable_bt.configure(state="normal")

        elif status == Status.Drawing:

            self.load_bt.configure(state="disabled")
            self.run_bt.configure(state="disabled")

            self.pause_bt.configure(state="normal")
            self.stop_bt.configure(state="normal")
            self.disable_bt.configure(state="disabled")

        elif status == Status.Paused:
            self.load_bt.configure(state="normal")

            self.run_bt.configure(state="normal", text="Continue")

            self.pause_bt.configure(state="disabled")
            self.stop_bt.configure(state="normal")

            self.disable_bt.configure(state="normal")

    def disable_motors(self):

        if PLOTTER.ad:
            my_log("trace in progress")

        PLOTTER.disable_motors()

    def compute_progress(self, ad):

        if not ad:
            return

        total_travel = PLOTTER.cur_travel
        distance_total = PLOTTER.dist_pen_total

        # print(f"{total_travel} / {distance_total}")

        if distance_total != 0:
            progress = total_travel / distance_total

            total_time_s = PLOTTER.estimated_duration
            remaining = "-"
            total_str = "-"
            if PLOTTER.start_time:
                cur_time = time.time()

                elapsed = cur_time - PLOTTER.start_time
                remaining = total_time_s - (elapsed + PLOTTER.pause_duration)
                total_str = td_format(timedelta(seconds=total_time_s))

                remaining = td_format(timedelta(seconds=remaining))

            # self.progress.set(progress/100)

            if not remaining:
                remaining = total_time_s - elapsed - PLOTTER.pause_duration
                remaining = td_format(timedelta(seconds=remaining))

                self.progress.set_with_text(
                    progress, f"{progress*100:2.1f}% - ending... total {total_str}"
                )
            else:
                self.progress.set_with_text(
                    progress, f"{progress*100:2.1f}% - {remaining} / {total_str}"
                )

    def update_status(self):

        if PLOTTER.report:
            self.report.insert(tkinter.END, PLOTTER.report)
            PLOTTER.report = None

        self.compute_progress(PLOTTER.ad)
        self.after(250, self.update_status)

    def log(self, txt):
        self.report.insert(tkinter.END, txt + "\n")
