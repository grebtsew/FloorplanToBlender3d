from process.process import Process


"""This class should evaluate image preformance and preferences"""
class Evaluate(Process):
    def __init__(self, data, shared_variables):
        super().__init__(data, shared_variables=shared_variables)

    def run(self):
        pass