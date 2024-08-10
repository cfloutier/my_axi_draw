


from datetime import timedelta
from enum import Enum
import customtkinter as ctk
import time
import tkinter
from settings import INTERNAL_SETTINGS
from pen_commands import TRACER
from tools.ctk.base_frame import BaseFrame
from tools.ctk.progress_bar import MyProgressBar
from tools.time import td_format

class Status(Enum):
    iddle = 0
    preview = 1
    draw = 2
    paused = 3
    stop = 4

class TracePage(ctk.CTkFrame):
    def __init__(self, master:ctk.CTkFrame):
        super().__init__(master)

        self._status = Status.iddle

        self.buttons_bar = BaseFrame(self)

        self.load_bt = self.buttons_bar.Button("Load svg", command=self.load_svg)

        self.run_bt = self.buttons_bar.Button("Run", command=self.run) 
        self.run_bt.configure(state="disabled")

        self.pause_bt = self.buttons_bar.Button("Pause", command=self.pause) 
        self.pause_bt.configure(state="disabled")

        self.disable_bt = self.buttons_bar.Button("Stop", command=self.stop) 
        # self.disable_bt.configure(state="disabled")

        self.disable_bt = self.buttons_bar.Button("Disable XY", command=self.disable_motors) 
        # self.disable_bt.configure(state="disabled")


        self.status_label = self.buttons_bar.label("iddle")

        self.buttons_bar.pack(side = "left", expand=True, anchor="n")

        self.report = ctk.CTkTextbox(master=self, width=800, height=400)
        self.report.pack(expand=True)

        self.progress = MyProgressBar(self, height=20, width = 800)
        self.progress.pack(expand=True, side = "bottom", pady=5)
        self.progress.set_with_text(0, "")

        self.pack()

    def load_svg(self):

        filename = ctk.filedialog.askopenfilename(initialdir=INTERNAL_SETTINGS.svg_path, 
                                                  defaultextension=".svg", 
                                                  filetypes=(("svg file", "*.svg"), ("All files", "*.*")))
        
        if filename is not None:
            self.report.insert(tkinter.END, "Loading in progress\n")
            INTERNAL_SETTINGS.svg_file = filename
            TRACER.preload(filename)

            self.set_status(Status.preview)
            self.start_pooling()

    def run(self):

        if not INTERNAL_SETTINGS.svg_file:
            return
        
        TRACER.draw(INTERNAL_SETTINGS.svg_file)
        self.set_status(Status.draw)
        self.start_pooling()


    def set_status(self, status :Status):

        self._status = status
        self.status_label.configure(text = status.name)
        

    def pause(self):
        if not TRACER.ad:
            return
        
        TRACER.ad.transmit_pause_request()

    def stop(self):
        if not TRACER.ad:
            return
        
        self.set_status(Status.stop)
        TRACER.ad.transmit_pause_request()

    def disable_motors(self):

        if TRACER.ad:
            print("trace in progress")

        TRACER.disable_motors()

    def start_pooling(self):
        # to let the thread starts
        time.sleep(0.5)
        
        self.update_status()

    def evaluate(self, ad ):
        stats = ad.plot_status.stats
        
        total_travel =  (stats.up_travel_inch + stats.down_travel_inch) * 2.54
        distance_total = TRACER.dist_pen_total
        if distance_total != 0:
            progress = total_travel / distance_total
            total_time_s = TRACER.estimated_duration
            remaining = "-"
            total_str = "-"
            if TRACER.start_time:
                cur_time = time.time() 

                elapsed = cur_time - TRACER.start_time
                remaining = total_time_s - elapsed
                total_str = td_format(timedelta(seconds=total_time_s))
                remaining = td_format(timedelta(seconds=remaining))
        
            # self.progress.set(progress/100)

            if not remaining:
                self.progress.set_with_text(progress/100, f" ending... total {total_str}")
            else:
                self.progress.set_with_text(progress/100, f"{remaining} / {total_str}")

            # print(f"progress : {progress:2.2f} % - remaining : {remaining} / {total_str}")
            
    def update_status(self):

        if TRACER.is_paused:

            if self._status == Status.stop:
                self.report.insert(tkinter.END, TRACER.report)
                self.report.insert(tkinter.END, "Back Home")

                TRACER.back_home()
                self.set_status(Status.iddle)
                return

            self.set_status(Status.paused)

            self.report.insert(tkinter.END,  TRACER.report)
            self.run_bt.configure(state="normal")
            self.pause_bt.configure(state="disabled")
            return

        if not TRACER.ad:
            # the end
            self.report.insert(tkinter.END,  TRACER.report)
            if self._status == Status.preview:
                self.run_bt.configure(state="normal")
                self.pause_bt.configure(state="disabled")

                self.set_status(Status.iddle)

            elif self._status == Status.draw:
                self.pause_bt.configure(state="disabled")
                self.set_status(Status.iddle)
            return
        
        if self._status == Status.draw:
            self.pause_bt.configure(state="normal")

        self.evaluate(TRACER.ad)
        
        self.after(250, self.update_status)

  









