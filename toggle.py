#!/usr/bin/env python
import time
from pyaxidraw import axidraw

def toggle_pen():
    ad = axidraw.AxiDraw() # Create class instance
    ad.plot_setup()        # Run setup without input file
    ad.options.mode = "toggle"
    ad.plot_run()          # Execute the command

def up():
    ad = axidraw.AxiDraw() # Create class instance
    ad.plot_setup()        # Run setup without input file
    ad.options.mode = "toggle"



def main():    
    time.sleep(0.5)
    ad = axidraw.AxiDraw() # Create class instance
    ad.plot_setup()        # Run setup without input file
    ad.options.mode = "toggle"
    ad.plot_run()          # Execute the command

if __name__ == "__main__":
    main()