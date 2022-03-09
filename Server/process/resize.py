from process.process import Process

"""
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""

"""This class should resize image for better performance, if needed"""
# TODO: implement this


class Resize(Process):
    def __init__(self, data, shared_variables):
        super().__init__(data, shared_variables=shared_variables)

    def run(self):
        pass
