
class Api():
    def __init__(self, client = None,  shared_variables = None):
        self.shared = shared_variables
        self.client = client

    def __getattr__(self, attr):
        return "Function undefined "+str(attr)
