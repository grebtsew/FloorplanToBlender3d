from process.process import Process


"""This class should check if images are too similar!"""
class Resize(Process):
    def __init__(self, data, shared_variables):
        super().__init__(data, shared_variables=shared_variables)

    def run(self):
        pass