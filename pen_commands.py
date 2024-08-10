
from pyaxidraw import axidraw
from settings import SETTINGS

def build_plot_ad() -> axidraw.AxiDraw:
    """ build ad interface and apply settings """

    # to disable connection in debug mode
    # return None

    ad = axidraw.AxiDraw() # Create class instance
    ad.plot_setup()        # Run setup without input file

    SETTINGS.apply(ad)

    return ad

def build_interactive_ad() -> axidraw.AxiDraw:
    """ build ad interface and apply settings """
    ad = axidraw.AxiDraw() # Create class instance
    ad.interactive()        # Run setup without input file

    SETTINGS.apply(ad)
    ad.update()

    return ad   
def toggle_pen():
    ad = build_plot_ad()
    if not ad: 
        return
    
    ad.options.mode = "toggle"
    ad.plot_run()          # Execute the command

def pen_up():
    ad = build_plot_ad()
    if not ad: 
        return
    
    ad.options.mode = "manual"
    ad.options.manual_cmd  = "raise_pen"
    ad.plot_run()          # Execute the command

def pen_down():
    ad = build_plot_ad()
    if not ad: 
        return
    
    ad.options.mode = "manual"
    ad.options.manual_cmd  = "lower_pen"
    ad.plot_run()          # Execute the command