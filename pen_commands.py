
from pathlib import Path
import time
from typing import Union
from pyaxidraw import axidraw
from settings import SETTINGS
import threading
from datetime import timedelta

from tools.time import td_format

def build_plot_ad(file_name = None) -> axidraw.AxiDraw:
    """ build ad interface and apply settings """

    # to disable connection in debug mode
    # return None

    ad = axidraw.AxiDraw() # Create class instance
    if file_name:
        ad.plot_setup(file_name)        # Run setup without input file
    else:
        ad.plot_setup()

    SETTINGS.apply(ad)

    return ad

def build_interactive_ad() -> axidraw.AxiDraw:
    """ build ad interface and apply settings """
    ad = axidraw.AxiDraw() # Create class instance
    ad.interactive()        # Run setup without input file

    SETTINGS.apply(ad)
    ad.update()

    return ad  

class TracerCommands:
    """ main class used to send commands to the tracer """
    def __init__(self) -> None:

        self.ad = None
        self.total_pen_lifts = None
        self.estimated_duration = None
        self.report = ""
        self.start_time = 0
        self.dist_pen_total = 0

    def toggle_pen(self):

        # trace in progress
        if self.ad:
            return
        
        ad = build_plot_ad()
        if not ad: 
            return
        
        ad.options.mode = "toggle"
        ad.plot_run()          # Execute the command

    def pen_up(self):
        # trace in progress
        if self.ad:
            return
        
        ad = build_plot_ad()
        if not ad: 
            return
        
        ad.options.mode = "manual"
        ad.options.manual_cmd  = "raise_pen"
        ad.plot_run()          # Execute the command

    def pen_down(self):
        # trace in progress
        if self.ad:
            return

        ad = build_plot_ad()
        if not ad: 
            return
        
        ad.options.mode = "manual"
        ad.options.manual_cmd  = "lower_pen"
        ad.plot_run()   # Execute the command

    def draw(self, file_path: Union[Path, str]):

        def run_draw():
            print(f"drawing {abs_path}")

            self.start_time = time.time()

            self.ad = build_plot_ad(abs_path)
            self.ad.options.preview = False
            self.ad.options.report_time = True # Enable time and distance estimates
            # self.ad.options.progress= True
            self.report = None
        
            self.ad.plot_run()   # plot the document

            end_time = time.time()

            print_time = td_format(timedelta(seconds=end_time-self.start_time))
            result = "----------------------- PRINT -----------------------------\n"
            result += f"file : {abs_path}\n"
            result += f"duration : {print_time}\n"
            result += "----------------------------------------------------------\n"

            self.report = result
            self.ad = None
            self.start_time = 0

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if self.ad:
            return

        abs_path = str(file_path.resolve())

        t = threading.Thread(target=run_draw)
        t.start()


    def preload(self, file_path: Union[Path, str]):
        # preload the svg in a thread

        def run_preload():
            print(abs_path)
            self.ad = build_plot_ad(abs_path)
            # ad.plot_setup(abs_path)    # Parse the input file

            self.ad.options.preview = True
            self.ad.options.report_time = False # Enable time and distance estimates
            self.ad.options.progress= True
            
            self.report = None

            self.ad.plot_run()   # plot the document

            print_time = td_format(timedelta(seconds=self.ad.time_estimate))
            dist_pen_down = self.ad.distance_pendown
            self.dist_pen_total = self.ad.distance_total
            pen_lifts = self.ad.pen_lifts
            time_elapsed = self.ad.time_elapsed

            result = "----------------------- PREVIEW -----------------------------\n"
            result += f"file : {abs_path}\n"
            result += f"estimated duration : {print_time}\n"
            result += f"distance down : {dist_pen_down:.2f} m \n"
            result += f"distance total : {self.dist_pen_total:.2f} m \n"
            result += f"pen lifts : {pen_lifts}\n"
            result += f"time elapsed for preview : {time_elapsed:.2f} s\n"
            result += "------------------------------------------------------------\n"

            self.total_pen_lifts = pen_lifts
            self.estimated_duration = self.ad.time_estimate
            self.report = result

            self.ad = None

            # print (result)

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if self.ad:
            return

        abs_path = str(file_path.resolve())

        t = threading.Thread(target=run_preload)
        t.start()
        # return result


TRACER = TracerCommands()





