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
        settings_dict = {s:dict(settings.items(s)) for s in settings.sections()}
        for group in settings_dict.items(): # ignore group names
            for item in group[1].items():
                #cor_dict = dict([(item[0],item[1])])
                #self.locals().update(cor_dict) # generate variables from settings
                exec (item[0] + '=' + item[1])

        # Debug
        print(self.out_format, "test")
        #print("All variables in class: ",vars(self)) # print all variables
        #print("All local variables", locals())

    def __str__(self):
        print(vars(self))