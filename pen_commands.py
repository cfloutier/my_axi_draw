
from pathlib import Path
import time
from typing import Union
from globals import my_log
from pyaxidraw import axidraw
from settings import SETTINGS, PLOTTER_PARAMS
import threading
from datetime import timedelta

from tools.time import td_format

def build_plot_ad(file_name = None, preview = False) -> axidraw.AxiDraw:
    """ build ad interface and apply settings """

    # to disable connection in debug mode
    # return None

    ad = axidraw.AxiDraw() # Create class instance
    if file_name:
        ad.plot_setup(file_name)        
    else:
        ad.plot_setup() # Run setup without input file

    SETTINGS.apply(ad)
    PLOTTER_PARAMS.apply(ad)

    if not preview:
        # check connection
        ad.serial_connect()
        ad.query_ebb_voltage()

    for key, value in ad.warnings.warning_dict.items():
        my_log(f"connection warning : {key}:{value}")
        if key == 'voltage':
            return None
        
    return ad

def build_interactive_ad() -> axidraw.AxiDraw:
    """ build ad interface and apply settings """
    ad = axidraw.AxiDraw() # Create class instance
    ad.interactive()        # Run setup without input file

    SETTINGS.apply(ad)
    PLOTTER_PARAMS.apply(ad)
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
        self.is_paused = False
        self.starting = False
       
        # cumultation duration of all pause times
        self.pause_duration = 0
        self.pause_travel_in = 0 # distanbe in inch to correct an ad bug in res_plot 

    def my_plot(self, ad):

        ad.plot_run()          # Execute the command

        if ad.text_out:
            my_log(ad.text_out)
        if ad.error_out:
            my_log("Error : " + ad.error_out)

    def toggle_pen(self):

        # trace in progress
        if self.ad:
            return
        
        ad = build_plot_ad()
        if not ad: 
            return
        
        ad.options.mode = "toggle"
        self.my_plot(ad)


    def pen_up(self):
        # trace in progress
        if self.ad:
            return
        
        ad = build_plot_ad()
        if not ad: 
            return
        
        ad.options.mode = "manual"
        ad.options.manual_cmd  = "raise_pen"
        self.my_plot(ad)

    def pen_down(self):
        # trace in progress
        if self.ad:
            return

        ad = build_plot_ad()
        if not ad: 
            return
        
        ad.options.mode = "manual"
        ad.options.manual_cmd  = "lower_pen"
        self.my_plot(ad)

        
    def disable_motors(self):
        # trace in progress
        if self.ad:
            return

        ad = build_plot_ad()
        if not ad: 
            return
        
        ad.options.mode = "manual"
        ad.options.manual_cmd  = "disable_xy"
        self.my_plot(ad)

    
    def back_home(self):
        if not self.is_paused or not self.ad:
            self.is_paused = False
            self.ad = None
            return
        
        self.ad.options.mode = "res_home"
        self.ad.plot_run()   # Execute the command 

        self.my_plot(self.ad)

        self.ad = None

    def draw(self, file_path: Union[Path, str]):

        def run_draw():
            my_log(f"start drawing thread {abs_path}")

            self.start_time = time.time()
            self.is_paused = False
            self.report = None

            if not self.is_paused and not self.ad:
                self.ad = build_plot_ad(abs_path)
                if self.ad == None:
                    self.starting = False
                    return

                # starting new run
                self.pause_duration = 0
                self.pause_travel_in = 0

                self.ad.options.preview = False
                self.ad.options.report_time = True # Enable time and distance estimates
                self.ad.errors.code = 0
            else:        
                self.ad.options.mode = "res_plot"
                self.ad.plot_status.stopped = 0
                self.ad.errors.code = 0
                self.pause_travel_in += self.ad.plot_status.stats.up_travel_inch          

            self.starting = False


            # self.ad.options.progress= True
            self.report = None

            self.my_plot(self.ad)

            end_time = time.time()
            total_time = end_time-self.start_time
            print_time = td_format(timedelta(seconds=total_time))
            
            is_paused = self.ad.plot_status.stopped == 103

            if is_paused:
                
                self.pause_duration += total_time
                
                print(f"cur_travel : {self.cur_travel} / {self.dist_pen_total} ")
                print(f"pause_travel : {self.pause_travel_in} ")

                result = "----------------------- PAUSED -----------------------------\n"
                result += f"duration : {print_time}\n"
                result += f"Press Run to restart \n"
                result += "----------------------------------------------------------\n"
                self.is_paused = True
            else:
                result = "----------------------- ENDED -----------------------------\n"
                result += f"file : {abs_path}\n"
                result += f"duration : {print_time}\n"
                result += "----------------------------------------------------------\n"
                self.is_paused = False
                self.ad = None

            self.report = result
            
            self.start_time = 0

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if self.ad and not self.is_paused:
            self.ad = None
            return
        
        self.starting = True

        abs_path = str(file_path.resolve())

        t = threading.Thread(target=run_draw)
        t.start()

    @property
    def cur_travel(self):
        if not self.ad:
            return 0
        
        stats = self.ad.plot_status.stats

        # print(f"{stats.up_travel_inch} up + {self.pause_travel_in} saved + {stats.down_travel_inch} dn")
        return (stats.up_travel_inch + self.pause_travel_in + stats.down_travel_inch) * 2.54 

    def preload(self, file_path: Union[Path, str]):
        # preload the svg in a thread

        def run_preload():
            # my_log("preload" + str(abs_path))

            self.ad = build_plot_ad(abs_path, preview=True)
            if self.ad == None:
                return
            # ad.plot_setup(abs_path)    # Parse the input file

            self.ad.options.preview = True
            self.ad.options.report_time = False # Enable time and distance estimates
            self.ad.options.progress= True
            
            self.report = None

            self.ad.plot_run()   # plot the document

            print_time = td_format(timedelta(seconds=self.ad.time_estimate))
            dist_pen_down = self.ad.distance_pendown
            self.dist_pen_total = self.ad.distance_total * 100
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





