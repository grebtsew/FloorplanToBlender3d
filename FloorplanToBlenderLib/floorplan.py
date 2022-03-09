import json

from . import const
from . import config

"""
Floorplan
This file contains functions for handling the floorplan class.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""


def new_floorplan(config):
    """
    Creates and returns a new floorplan class from config file
    """
    return floorplan(config)


class floorplan:
    """
    This class contains the representation of each floorplan
    The class is needed to simplify the code and it's costumizability
    """

    def __init__(self, conf=None):
        if conf is None:
            # use default
            conf = const.IMAGE_DEFAULT_CONFIG_FILE_NAME
        self.conf = conf
        self.create_variables_from_config(self.conf)

    def __str__(self):
        return str(vars(self))

    def create_variables_from_config(self, conf):
        settings = config.get_all(conf)
        settings_dict = {s: dict(settings.items(s)) for s in settings.sections()}
        for group in settings_dict.items():  # ignore group names
            for item in group[1].items():
                setattr(self, item[0], json.loads(item[1]))

        # Debug
        # print(vars(self))
