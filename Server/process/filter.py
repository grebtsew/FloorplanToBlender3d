from process.process import Process


"""This class should remove noise and make better for performance"""
class Filter(Process):
    def __init__(self, data, shared_variables):
        super().__init__(data, shared_variables=shared_variables)

    def run(self):
        pass