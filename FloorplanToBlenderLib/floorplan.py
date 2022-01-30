from . import const
from . import config
"""
Floorplan
This file contains functions for handling the floorplan class.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""

def new_floorplan(config):
    """
    Creates and returns a new floorplan class from config file
    """
    return floorplan(config)

class floorplan():
    """
    This class contains the representation of each floorplan
    The class is needed to simplify the code and it's costumizability
    """

    def __init__(self, conf=None):
        if conf is None:
            # use default
            conf = const.IMAGE_DEFAULT_CONFIG_FILE_NAME
        
        settings = config.get_all(conf)
        locals().update(settings) # generate variables from settings

    def __str__(self):
        print(vars(self))