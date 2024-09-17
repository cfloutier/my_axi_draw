


from pathlib import Path

import yaml

from globals import my_log
from pyaxidraw import axidraw
from tools.fs import make_parent_dir



class BaseSettings:

    def _file_path(self, name = None):
        if not name:
            name = "default"

        file_path = Path(__file__).parent / "settings" / (name + ".yml") 

        return file_path

    def load(self, name = None):
        file_path = self._file_path(name)
        if not file_path.exists():
           my_log("file not found")
           return
       
        with open(file_path, 'r', encoding='UTF-8') as stream:
            my_dict = yaml.load(stream, Loader=yaml.SafeLoader)
            if my_dict is None:
                my_log("error reading file")
                return
            
            for key, value in my_dict.items(): 
                setattr(self, key, value)

    def _save(self, name = None):
        file_path = self._file_path(name)

        my_log(f"saving configuration : {file_path.stem}")

        make_parent_dir(file_path)

        with open(file_path, 'w', encoding='UTF-8') as stream:
            yaml.dump(self.__dict__, stream=stream, sort_keys=True)

    def __str__(self) -> str:
        return str(self.__dict__)

class InternalSettings(BaseSettings):
    """ 
    settings used only for this app 
    """

    def __init__(self) -> None:
        # the current loaded file
        self.svg_file = None
        self.profile_name = "default"

        self.svg_path = (Path(__file__).parent / "sources_svg").resolve()
        self.auto_load_svg = None

    def save(self):
        self._save("internal")

    def _file_path(self, name = None):
        return super()._file_path("internal")
    
class PlotterParams(BaseSettings):
    """ 
    plotter size and calibration
    """
    def __init__(self) -> None:

        # must be copied to options 
        self.model = 5      # AxiDraw Model (1-6).
                            # 1: AxiDraw V2 or V3 (Default). 2: AxiDraw V3/A3 or SE/A3.
                            # 3: AxiDraw V3 XLX. 4: AxiDraw MiniKit.
                            # 5: AxiDraw SE/A1.  6: AxiDraw SE/A2.

        # part of the internal params
        self.native_res_factor = 1016.0  # Motor resolution factor, steps per inch. Default: 1016.0
                # Note that resolution is defined along native (not X or Y) axes.
                # Resolution is native_res_factor * sqrt(2) steps/inch in Low Resolution  (Approx 1437 steps/in)
                #       and 2 * native_res_factor * sqrt(2) steps/inch in High Resolution (Approx 2874 steps/in)

        self.clip_to_page = True  # Clip plotting area to SVG document size. Default: True

        self.inch_to_mm = 25.4

        self.switch_xy = True

        # Model 5 in mm !
        self.x_travel_SEA1_mm = 864     # AxiDraw SE/A1: X             Default: 34.02 in (864 mm)
        self.y_travel_SEA1_mm = 594     # AxiDraw SE/A1: Y             Default: 23.39 in (594 mm)

        # Model 6
        self.x_travel_SEA2_mm = 594     # AxiDraw SE/A2: X             Default: 23.39 in (594 mm)
        self.y_travel_SEA2_mm = 432     # AxiDraw SE/A2: Y             Default: 17.01 in (432 mm)

        # Model 2
        self.x_travel_V3A3_mm = 430    # V3/A3 and SE/A3: X           Default: 16.93 in (430 mm)
        self.y_travel_V3A3_mm = 297    # V3/A3 and SE/A3: Y           Default: 11.69 in (297 mm)

    def save(self):
        self._save("plotter")

    def _file_path(self, name = None):
        return super()._file_path("plotter")   

    def apply(self, ad: axidraw.AxiDraw):

        # return

        ad.options.model = self.model

        ad.params.native_res_factor = self.native_res_factor

        if self.switch_xy:
    
            # convert to inches
            ad.params.x_travel_SEA1 = self.y_travel_SEA1_mm / self.inch_to_mm
            ad.params.y_travel_SEA1 = self.x_travel_SEA1_mm / self.inch_to_mm

            ad.params.x_travel_SEA2 = self.y_travel_SEA2_mm / self.inch_to_mm
            ad.params.y_travel_SEA2 = self.x_travel_SEA2_mm / self.inch_to_mm

            ad.params.x_travel_V3A3 = self.y_travel_V3A3_mm / self.inch_to_mm
            ad.params.y_travel_V3A3 = self.x_travel_V3A3_mm / self.inch_to_mm

        else:
            # convert to inches
            ad.params.x_travel_SEA1 = self.x_travel_SEA1_mm / self.inch_to_mm
            ad.params.y_travel_SEA1 = self.y_travel_SEA1_mm / self.inch_to_mm

            ad.params.x_travel_SEA2 = self.x_travel_SEA2_mm / self.inch_to_mm
            ad.params.y_travel_SEA2 = self.y_travel_SEA2_mm / self.inch_to_mm

            ad.params.x_travel_V3A3 = self.x_travel_V3A3_mm / self.inch_to_mm
            ad.params.y_travel_V3A3 = self.y_travel_V3A3_mm / self.inch_to_mm
        
        ad.params.clip_to_page = self.clip_to_page

    def reset(self):
        new_values = PlotterParams()
        for key, value in new_values.__dict__.items(): 
            setattr(self, key, value)

class OverloadedSettings(BaseSettings):
    """ overload of some of the standard settings """

    def __init__(self) -> None:

        self.speed_pendown = 25      # Maximum plotting speed, when pen is down (1-100). Default 25
        self.speed_penup = 75        # Maximum transit speed, when pen is up (1-100). Default 75
        self.accel = 75              # Acceleration rate factor (1-100). Default 75

        self.pen_pos_up = 30         # Height of pen when raised (0-100). Default 60
        self.pen_pos_down = 60       # Height of pen when lowered (0-100). Default 30

        self.pen_rate_raise = 75     # Rate of raising pen (1-100). Default 75
        self.pen_rate_lower = 50     # Rate of lowering pen (1-100). Default 50

        self.const_speed = False     # Use constant velocity mode when pen is down. Default False
        self.report_time = False     # Report time elapsed. Default False

        self.model = 6      # AxiDraw Model (1-6).
                            # 1: AxiDraw V2 or V3 (Default). 2: AxiDraw V3/A3 or SE/A3.
                            # 3: AxiDraw V3 XLX. 4: AxiDraw MiniKit.
                            # 5: AxiDraw SE/A1.  6: AxiDraw SE/A2.

        self.resolution = 1 # Resolution: (1-2):
                            # 1: High resolution (smoother, slightly slower) (Default)
                            # 2: Low resolution (coarser, slightly faster)

        # Effective motor resolution is approx. 1437 or 2874 steps per inch, in the two modes respectively.
        # Note that these resolutions are defined along the native axes of the machine (X+Y) and (X-Y),
        # not along the XY axes of the machine. This parameter chooses 8X or 16X motor microstepping.
        self.auto_rotate = False      # Auto-select portrait vs landscape orientation
                                    # Default: True

        self.reordering = 2          # Plot optimization option (0-4; 3 is deprecated)
                                    # 0: Least; Only connect adjoining paths (Default)
                                    # 1: Basic; Also reorder paths for speed
                                    # 2: Full; Also allow path reversal
                                    # 4: None; Strictly preserve file order

        self.random_start = False    # Randomize start locations of closed paths. Default False

    def reset(self):

        new_values = OverloadedSettings()

        for key, value in new_values.__dict__.items(): 
            setattr(self, key, value)

    def apply(self, ad: axidraw.AxiDraw):

        for key, value in self.__dict__.items(): 
            setattr(ad.options, key, value)

    def _file_path(self, name = None):
        if not name:
            name = INTERNAL_SETTINGS.profile_name

        file_path = Path(__file__).parent / "settings" / (name + ".yml") 

        return file_path
    
    def save(self):
        self._save()


# if __name__ == "__main__":
#     # test U

#     s = OverloadedSettings()
#     print(s)
#     s.save()
#     print(s)

INTERNAL_SETTINGS = InternalSettings()
PLOTTER_PARAMS = PlotterParams()
SETTINGS = OverloadedSettings()

PLOTTER_PARAMS.save()