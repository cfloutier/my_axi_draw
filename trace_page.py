


from datetime import timedelta
import customtkinter as ctk
import time
import tkinter
from settings import INTERNAL_SETTINGS
from pen_commands import TRACER
from tools.ctk.base_frame import BaseFrame
from tools.ctk.progress_bar import MyProgressBar
from tools.time import td_format

class TracePage(ctk.CTkFrame):

    def load_svg(self):

        filename = ctk.filedialog.askopenfilename(initialdir=INTERNAL_SETTINGS.svg_path, 
                                                  defaultextension=".svg", 
                                                  filetypes=(("svg file", "*.svg"), ("All files", "*.*")))
        
        if filename is not None:
            self.report.insert(tkinter.END, "Loading in progress\n")
            INTERNAL_SETTINGS.svg_file = filename
            TRACER.preload(filename)

            # to let the thread starts
            time.sleep(0.5)
            
            self.update_status()

    def run(self):

        if not INTERNAL_SETTINGS.svg_file:
            return
        
        TRACER.draw(INTERNAL_SETTINGS.svg_file)

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
        if not TRACER.ad:
            # the end
            self.report.insert(tkinter.END,  TRACER.report)
            self.run_bt.configure(state="normal")
            return
        
        self.evaluate(TRACER.ad)
        
        self.after(250, self.update_status)

    def __init__(self, master:ctk.CTkFrame):
        super().__init__(master)

        self.buttons_bar = BaseFrame(self)

        self.load_bt = self.buttons_bar.Button("Load svg", command=self.load_svg)

        self.run_bt = self.buttons_bar.Button("Run", command=self.run) 
        self.run_bt.configure(state="disabled")

        self.buttons_bar.pack(side = "left", expand=True, anchor="n")

        self.report = ctk.CTkTextbox(master=self, width=800, height=500)
        self.report.pack(expand=True)

        self.progress = MyProgressBar(self, height=20, width = 800)
        self.progress.pack(expand=True, side = "bottom", pady=5)
        self.progress.set_with_text(0, "")

        self.pack()









