"""
The process class represents a thread handling incoming requests
"""
import threading

class Process(threading.Thread):
    def __init__(self, name = None,  shared_variables = None):
        threading.Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables

    def run(self):
        pass