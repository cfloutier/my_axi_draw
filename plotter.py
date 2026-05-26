from enum import Enum
import logging
from pathlib import Path
import time
from typing import Union
from globals import my_log
from lxml import etree
from pyaxidraw import axidraw
from settings import SETTINGS, PLOTTER_PARAMS
import threading
from datetime import timedelta

from tools.time import td_format


def build_plot_ad(file_name=None, preview=False) -> axidraw.AxiDraw:
    """build ad interface and apply settings"""

    # to disable connection in debug mode
    # return None

    ad = axidraw.AxiDraw()  # Create class instance
    if file_name:
        ad.plot_setup(file_name)
    else:
        ad.plot_setup()  # Run setup without input file

    SETTINGS.apply(ad)
    PLOTTER_PARAMS.apply(ad)

    if not preview:
        # check connection
        ad.serial_connect()
        ad.query_ebb_voltage()

    for key, value in ad.warnings.warning_dict.items():
        my_log(f"connection warning : {key}:{value}")
        if key == "voltage":
            return None

    return ad


def build_interactive_ad() -> axidraw.AxiDraw:
    """build ad interface and apply settings"""
    ad = axidraw.AxiDraw()  # Create class instance
    ad.interactive()  # Run setup without input file

    SETTINGS.apply(ad)
    PLOTTER_PARAMS.apply(ad)
    ad.update()

    return ad


def execute_plot(ad: axidraw.AxiDraw):
    """just execute the command the ad was prepared for and send errors and output to log after"""

    ad.plot_run()  # Execute the command

    if ad.text_out:
        my_log(ad.text_out)

    if ad.error_out:
        my_log("Error : " + ad.error_out)


class Status(Enum):

    Iddle = 0
    Preview = 1
    Ready = 2
    Drawing = 3
    Pausing = 4
    Paused = 5
    Homing = 6
    Stopping = 7


class Plotter:
    """main class used to send commands to the tracer"""

    def __init__(self) -> None:

        # jamais utilisé
        self.ad = None

        self._status = Status.Iddle

        self.total_pen_lifts = None
        self.estimated_duration = None
        self.report = ""
        self.start_time = 0
        self.dist_pen_total = 0

        # cumultation duration of all pause times
        self.pause_duration = 0
        # up_travel_inch is reset by the lib on each resume; accumulate it manually
        self.pause_up_travel_inch = 0.0
        self.status_listenners = []

    def set_status(self, status: Status):
        if status == self._status:
            return

        self._status = status

        for listenner in self.status_listenners:
            listenner(self._status)

    def toggle_pen(self):

        # trace in progress
        if self.ad:
            return

        ad = build_plot_ad()
        if not ad:
            return

        ad.options.mode = "toggle"
        execute_plot(ad)

    def pen_up(self):
        # trace in progress
        if self.ad:
            return

        ad = build_plot_ad()
        if not ad:
            return

        ad.options.mode = "manual"
        ad.options.manual_cmd = "raise_pen"
        execute_plot(ad)

    def pen_down(self):
        # trace in progress
        if self.ad:
            return

        ad = build_plot_ad()
        if not ad:
            return

        ad.options.mode = "manual"
        ad.options.manual_cmd = "lower_pen"
        execute_plot(ad)

    def disable_motors(self):
        # trace in progress
        if self.ad:
            return

        ad = build_plot_ad()
        if not ad:
            return

        ad.options.mode = "manual"
        ad.options.manual_cmd = "disable_xy"
        execute_plot(ad)

    def back_home(self):
        if not self.ad:
            return

        self.set_status(Status.Homing)

        self.ad.options.mode = "res_home"
        # digest=1 leaves document as _Element, not ElementTree — fix before plot_run
        if not isinstance(self.ad.document, etree._ElementTree):
            self.ad.document = etree.ElementTree(self.ad.document)
        self.ad.plot_run()  # Execute the command

        self.set_status(Status.Ready)

        self.ad = None

    def stop(self):

        if not self.ad:
            return

        if self._status == Status.Paused:
            self.back_home()
        else:
            self.set_status(Status.Stopping)
            self.ad.transmit_pause_request()

    def pause(self):

        if not self.ad:
            return

        self.set_status(Status.Pausing)
        self.ad.transmit_pause_request()

    def draw(self, file_path: Union[Path, str]):

        logging.info(f"draw  {file_path}")

        def run_draw():
            my_log(f"start drawing thread {abs_path}")

            self.report = None

            self.set_status(Status.Drawing)

            if not self.ad:
                # not paused — refresh time estimate with current settings before plotting
                preview_ad = build_plot_ad(abs_path, preview=True)
                if preview_ad:
                    preview_ad.options.preview = True
                    preview_ad.options.report_time = False
                    preview_ad.options.digest = 1  # use/build plob cache for speed
                    preview_ad.plot_run()
                    self.estimated_duration = preview_ad.time_estimate

                self.ad = build_plot_ad(abs_path)
                if self.ad == None:

                    self.report = "\n------------- Error -------------\n"
                    self.set_status(Status.Ready)

                    return

                # starting new run
                self.pause_duration = 0
                self.pause_up_travel_inch = 0.0

                self.ad.options.preview = False
                self.ad.options.report_time = True  # Enable time and distance estimates
                self.ad.options.digest = 1  # cache plob for fast resume
                self.ad.errors.code = 0
            else:
                # resume from pause — save up_travel_inch before the lib resets it on plot_run
                self.pause_up_travel_inch += self.ad.plot_status.stats.up_travel_inch

                self.ad.options.mode = "res_plot"
                self.ad.plot_status.stopped = 0
                self.ad.errors.code = 0
                # digest=1 leaves document as _Element, not ElementTree — fix before plot_run
                if not isinstance(self.ad.document, etree._ElementTree):
                    self.ad.document = etree.ElementTree(self.ad.document)

            # self.ad.options.progress= True
            self.report = None
            execute_start = time.time()  # internal fallback
            self.start_time = (
                0  # sentinel: UI thread sets this on first pen-down movement
            )

            execute_plot(self.ad)

            end_time = time.time()
            # prefer UI-detected start (excludes SVG processing time), fall back to execute_start
            actual_start = self.start_time if self.start_time > 0 else execute_start
            total_time = end_time - actual_start
            print_time = td_format(timedelta(seconds=total_time))

            is_paused = self.ad.plot_status.stopped == 103

            logging.info(f"is_paused {is_paused}")

            if is_paused:
                if self._status == Status.Stopping:
                    result = "Back Home\n"
                    self.back_home()
                else:
                    self.pause_duration += total_time

                    result = (
                        "----------------------- PAUSED -----------------------------\n"
                    )
                    result += f"duration : {print_time}\n"
                    result += f"Press Run to restart \n"
                    result += (
                        "----------------------------------------------------------\n"
                    )

                    self.set_status(Status.Paused)

            else:
                result = "----------------------- ENDED -----------------------------\n"
                result += f"file : {abs_path}\n"
                result += f"duration : {print_time}\n"
                result += "----------------------------------------------------------\n"
                self.ad = None
                self.set_status(Status.Ready)

            self.report = result
            self.start_time = 0

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        abs_path = str(file_path.resolve())

        t = threading.Thread(target=run_draw)
        t.start()

    @property
    def cur_travel(self):
        if not self.ad:
            return 0

        stats = self.ad.plot_status.stats

        return (
            stats.up_travel_inch + stats.down_travel_inch + self.pause_up_travel_inch
        ) * 2.54

    def preload(self, file_path: Union[Path, str]):
        # preload the svg in a thread

        logging.info(f"preload  {file_path}")

        def run_preload():

            try:
                self.ad = build_plot_ad(abs_path, preview=True)
            except RuntimeError as e:
                self.report = f"------------- Error -------------\n{e}\n{abs_path}\n---------------------------------\n"
                self.set_status(Status.Ready)
                return

            self.set_status(Status.Preview)

            if self.ad == None:
                return

            self.ad.options.preview = True
            self.ad.options.report_time = False  # Enable time and distance estimates
            self.ad.options.progress = True

            self.report = None

            self.ad.plot_run()  # plot the document

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

            self.set_status(status=Status.Ready)

            # print (result)

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if self.ad:
            return

        abs_path = str(file_path.resolve())

        t = threading.Thread(target=run_preload)
        t.start()
        # return result


PLOTTER = Plotter()
