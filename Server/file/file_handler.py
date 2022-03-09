import os
import shutil

"""
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""


class FileHandler:
    def __init__(self):
        pass

    def init_files(self):
        pass

    def remove(self, path):
        """param <path> could either be relative or absolute."""
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)  # remove the file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(path))
