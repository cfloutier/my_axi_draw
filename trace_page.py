


from datetime import timedelta
from enum import Enum
import customtkinter as ctk
import time
import tkinter
from globals import my_log
from settings import INTERNAL_SETTINGS
from pen_commands import TRACER
from tools.ctk.base_frame import BaseFrame
from tools.ctk.progress_bar import MyProgressBar
from tools.time import td_format

class Status(Enum):
    Iddle = 0
    Preview = 1
    Ready = 2
    Drawing = 3
    Pausing = 4
    Paused = 5
    Stopping = 6

class TracePage(ctk.CTkFrame):
    def __init__(self, master:ctk.CTkFrame):
        super().__init__(master)

        self._status = Status.Iddle
        # self.configure(bg_color="red")

        self.buttons_bar = BaseFrame(self)

        self.load_bt = self.buttons_bar.Button("Load svg", command=self.load_svg)

        self.run_bt = self.buttons_bar.Button("Run", command=self.run) 
        self.pause_bt = self.buttons_bar.Button("Pause", command=self.pause) 
        self.stop_bt = self.buttons_bar.Button("Stop", command=self.stop) 
        self.disable_bt = self.buttons_bar.Button("Disable XY", command=self.disable_motors) 
        
        self.status_label = self.buttons_bar.label("iddle")

        self.buttons_bar.grid(row = 0, column=0, rowspan = 2, sticky="ne", pady=5, padx=(5,10))
        self.report = ctk.CTkTextbox(master=self, width = 20)
        self.report.grid(row = 0, column=1, sticky="news")

        # self.report.pack(side="left", fill="both", expand=True, anchor="nsew")

        self.progress = MyProgressBar(self, height=20)
        # self.progress.pack(expand=True, side = "bottom", pady=5)
        self.progress.grid(row = 1, column=1, sticky="new", pady=5)
        self.progress.set_with_text(0, "")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=10)
       
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=0)

        self.pack(side="left", fill="both", expand=True)

        self.set_status(Status.Iddle)

        if INTERNAL_SETTINGS.auto_load_svg:
            self.load_svg(INTERNAL_SETTINGS.auto_load_svg)

    def load_svg(self, filename = None):

        if not filename:
            filename = ctk.filedialog.askopenfilename(initialdir=INTERNAL_SETTINGS.svg_path, 
                                                  defaultextension=".svg", 
                                                  filetypes=(("svg file", "*.svg"), ("All files", "*.*")))
        
        if filename:
            self.report.insert(tkinter.END, "Loading in progress\n")
            INTERNAL_SETTINGS.svg_file = filename
            TRACER.preload(filename)

            self.set_status(Status.Preview)
            self.start_pooling()

    def run(self):

        if not INTERNAL_SETTINGS.svg_file:
            return
        
        TRACER.draw(INTERNAL_SETTINGS.svg_file)
        self.set_status(Status.Drawing)
        self.start_pooling()


    def set_status(self, status :Status):

        print(f"set_status {status}")

        self._status = status
        self.status_label.configure(text = status.name)

        if status == Status.Iddle:
            self.load_bt.configure(state="normal")

            self.pause_bt.configure(state="disabled")       
            self.run_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")

            self.disable_bt.configure(state="normal")
        elif status == Status.Preview:

            self.load_bt.configure(state="disabled")

            self.pause_bt.configure(state="disabled")
            self.run_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")

            self.disable_bt.configure(state="normal")
        elif status == Status.Ready:

            self.load_bt.configure(state="normal")

            self.run_bt.configure(state="normal")
            self.pause_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")
            
            self.disable_bt.configure(state="normal")

        
        elif status == Status.Drawing:

            self.load_bt.configure(state="disabled")

            self.run_bt.configure(state="disabled")
            self.pause_bt.configure(state="normal")
            self.stop_bt.configure(state="normal")

            self.disable_bt.configure(state="disabled")

        elif status == Status.Pausing or status ==  Status.Stopping:
            self.load_bt.configure(state="disabled")

            self.run_bt.configure(state="disabled")
            self.pause_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")
            self.disable_bt.configure(state="disabled")
        
        elif status == Status.Paused:
            self.load_bt.configure(state="normal")

            self.run_bt.configure(state="normal")

            self.pause_bt.configure(state="disabled")
            self.stop_bt.configure(state="disabled")

            self.disable_bt.configure(state="normal")

    def pause(self):
        if not TRACER.ad:
            return
        
        self.set_status(Status.Pausing)
        
        TRACER.ad.transmit_pause_request()

    def stop(self):
        if not TRACER.ad:
            return
        
        self.set_status(Status.Stopping)
        TRACER.ad.transmit_pause_request()

    def disable_motors(self):

        if TRACER.ad:
            my_log("trace in progress")

        TRACER.disable_motors()

    def start_pooling(self):
        # to let the thread starts
        time.sleep(0.5)
        
        self.update_status()

    def compute_progress(self, ad ):

        if not ad:
            return
        
        total_travel = TRACER.cur_travel 
        distance_total = TRACER.dist_pen_total

        print(f"{total_travel} / {distance_total}")

        if distance_total != 0:
            progress = total_travel / distance_total

            total_time_s = TRACER.estimated_duration
            remaining = "-"
            total_str = "-"
            if TRACER.start_time:
                cur_time = time.time() 

                elapsed = cur_time - TRACER.start_time
                remaining = total_time_s - (elapsed + TRACER.pause_duration)
                total_str = td_format(timedelta(seconds=total_time_s))

                remaining = td_format(timedelta(seconds=remaining))
        
            # self.progress.set(progress/100)

            if not remaining:
                remaining = total_time_s - elapsed - TRACER.pause_duration
                remaining = td_format(timedelta(seconds=remaining))

                self.progress.set_with_text(progress, f"{progress*100:2.1f}% - ending... total {total_str}")
            else:
                self.progress.set_with_text(progress, f"{progress*100:2.1f}% - {remaining} / {total_str}")

            # print(f"progress : {progress:2.2f} % - remaining : {remaining} / {total_str}")
            
    def update_status(self):

        if TRACER.is_paused:

            if self._status == Status.Stopping:
                self.report.insert(tkinter.END, TRACER.report)
                self.report.insert(tkinter.END, "Back Home")

                TRACER.back_home()
                self.progress.set_with_text(0, f"Stopped")
                self.set_status(Status.Ready)
                return

            self.set_status(Status.Paused)
            if TRACER.report:
                self.report.insert(tkinter.END, TRACER.report)

            return

        if not TRACER.starting and not TRACER.ad:
            # the end
            if TRACER.report:
                self.report.insert(tkinter.END,  TRACER.report)
            if self._status == Status.Preview or self._status == Status.Drawing:
                self.set_status(Status.Ready)

            self.progress.set_with_text(100, f"")
            return
        
        self.compute_progress(TRACER.ad)  
        self.after(250, self.update_status)

    def log(self, txt):
        self.report.insert(tkinter.END, txt+"\n")









