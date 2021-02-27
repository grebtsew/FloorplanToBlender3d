"""
The process class represents a thread handling stuff in new threads
"""
import threading

class Process(threading.Thread):
    def __init__(self, data,  shared_variables = None):
        threading.Thread.__init__(self)
        
        self.shared = shared_variables
        self.data = data

        _pid = None
        while self.shared.pid_exist(_pid) or _pid is None: 
            _pid = self.shared.pid_generator()

        self.pid = _pid

        # initiate process object that should be used!
        self.process = dict()
        self.process["pid"] = self.pid
        self.process["status"] = "Initiated"
        self.process["task"]= None
        self.process["in"]= None
        self.process["out"]= None
        self.process["comments"]= []
        self.process["state"]= 0
        self.process["cstate"]=0
        self.shared.all_processes.append(self.process)
    
    def update(self,field, value):
        """Update process status with less repetative code
        Always use this only once last if several fields are to be updated
        This will basicly sync with gui and other parts of the system"""
        self.process[field] = value
        index = self.shared.all_processes.index(self.process)
        self.shared.all_processes[index] = self.process