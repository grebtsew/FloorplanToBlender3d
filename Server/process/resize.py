from process.process import Process


"""This class should resize image for better performance, if needed"""
class Resize(Process):
    def __init__(self, data, shared_variables):
        super().__init__(data, shared_variables=shared_variables)

    def run(self):
        pass