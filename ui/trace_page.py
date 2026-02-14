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

        width_larger_bt = 200
        width_sep = 10

        self.load_bt = self.buttons_bar.button(
            "Load svg", command=self.load_svg, width=width_larger_bt
        )
        self.load_bt = self.buttons_bar.button(
            "Reload", command=self.reload_last, width=width_larger_bt
        )

        self.buttons_bar.separator(width_sep)

        self.disable_bt = self.buttons_bar.button(
            "Disable XY", command=self.disable_motors, width=width_larger_bt
        )

        self.buttons_bar.separator(width_sep)

        self.auto_pause = self.buttons_bar.switch("Auto Pause", None)
        self.auto_pause.set(False)
        self.auto_pause_duration = self.buttons_bar.number_edit(
            "Duration (min) : ", 10, False, inline=False
        )
        self.auto_pause_time = None

        self.buttons_bar.separator(width_sep)

        self.run_bar = BaseFrame(self.buttons_bar)
        self.run_bar.grid(
            row=self.buttons_bar.row,
            column=self.buttons_bar.col,
            sticky="w",
        )

        self.buttons_bar.row += 1
        width_bt = 70
        height_bt = 50

        self.buttons_bar.configure(height=150)
        self.run_bt = self.run_bar.button(
            "Run", command=self.run, inline=True, width=width_bt, height=height_bt
        )
        self.pause_bt = self.run_bar.button(
            "Pause",
            command=PLOTTER.pause,
            inline=True,
            width=width_bt,
            height=height_bt,
        )
        self.stop_bt = self.run_bar.button(
            "Stop", command=PLOTTER.stop, inline=True, width=width_bt, height=height_bt
        )

        self.buttons_bar.separator(width_sep)

        self.status_label = self.buttons_bar.label("iddle")

        self.buttons_bar.grid(row=0, column=0, sticky="nes", pady=5, padx=(5, 10))
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

    def _report(self, txt):

        yscroll = self.report.yview()[1] == 1
        print(yscroll)

        self.report.insert(tkinter.END, txt)
        if yscroll:
            self.report.see("end")

    def load_svg(self, filename=None):
        if not filename:
            filename = ctk.filedialog.askopenfilename(
                initialdir=INTERNAL_SETTINGS.svg_path,
                defaultextension=".svg",
                filetypes=(("svg file", "*.svg"), ("All files", "*.*")),
            )

        if filename:
            self._report("Loading in progress\n")
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

        print(f"set_status {status}")

        self.status_label.configure(text=status.name)

        if status == Status.Preview:

            # Disable all buttons
            self.load_bt.configure(state="disabled")
            self.pause_bt.configure(state="disabled")
            self.run_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")
            self.disable_bt.configure(state="disabled")

        elif (
            status == Status.Pausing
            or status == Status.Stopping
            or status == Status.Homing
        ):
            # Disable all buttons
            self.load_bt.configure(state="normal")
            self.pause_bt.configure(state="normal")
            self.run_bt.configure(state="normal")
            self.stop_bt.configure(state="normal")
            self.disable_bt.configure(state="normal")

        elif status == Status.Ready:

            self.load_bt.configure(state="normal")
            self.run_bt.configure(state="normal", text="Run")
            self.pause_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")
            self.disable_bt.configure(state="normal")

            self.progress.set_with_text(100, "")

        elif status == Status.Drawing:

            self.load_bt.configure(state="disabled")
            self.run_bt.configure(state="disabled")
            self.pause_bt.configure(state="normal")
            self.stop_bt.configure(state="normal")
            self.disable_bt.configure(state="disabled")

            if self.auto_pause.get():
                # auto pause is on
                self.start_pause_timer()

        elif status == Status.Paused:
            self.load_bt.configure(state="normal")

            self.run_bt.configure(state="normal", text="Continue")
            self.pause_bt.configure(state="disabled")
            self.stop_bt.configure(state="normal")
            self.disable_bt.configure(state="normal")

            self.stop_pause_timer()

    def start_pause_timer(self):
        duration_seconds = self.auto_pause_duration.get() * 60
        self.auto_pause_time = time.time() + duration_seconds

    def stop_pause_timer(self):
        self.auto_pause_time = None

    def disable_motors(self):

        if PLOTTER.ad:
            my_log("trace in progress")
            return

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

            content = ""

            if not remaining:
                remaining = total_time_s - elapsed - PLOTTER.pause_duration
                remaining = td_format(timedelta(seconds=remaining))
                content = f"{progress*100:2.1f}% - ending... total {total_str}"
            else:
                content = f"{progress*100:2.1f}% - {remaining} / {total_str}"

            remaining_time_pause = None
            if self.auto_pause_time is not None:
                remaining_time_pause = self.auto_pause_time - time.time()
                content += "- pause in " + td_format(
                    timedelta(seconds=remaining_time_pause)
                )

            self.progress.set_with_text(progress, content)

    def update_status(self):

        try:
            if PLOTTER.report:
                self._report(PLOTTER.report)
                PLOTTER.report = None

            self.check_pause_timer()
            self.compute_progress(PLOTTER.ad)
        except Exception as ex:
            txt_ex = "------------------\nException occured\n"
            txt_ex += str(ex) + "\n-----------------\n"
            self._report(txt_ex)
        finally:
            self.after(500, self.update_status)

    def check_pause_timer(self):

        if self.auto_pause_time is not None:
            remaining_time_pause = self.auto_pause_time - time.time()
            if remaining_time_pause < 0:
                PLOTTER.pause()

    def log(self, txt):
        self._report(txt + "\n")
