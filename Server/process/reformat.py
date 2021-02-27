from process.process import Process


"""This class should reformat one object supported in blender, into another format"""
class Reformat(Process):
    def __init__(self, data, shared_variables):
        super().__init__(data, shared_variables=shared_variables)
    