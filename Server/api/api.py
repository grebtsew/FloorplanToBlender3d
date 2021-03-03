

def client_exist(client, client_list):
    for c in client_list:
        if c["address"] == client[0] and c["port"] == client[1]:
            return True
    return False

def client_index(client, client_list):
    i = 0
    for c in client_list:
        if c["address"] == client[0] and c["port"] == client[1]:
            return i
        i += 1
    return i

class Api():
    def __init__(self, client = None,  shared_variables = None):
        self.shared = shared_variables
        self.client = client

        # Store all new connections!
        if not client_exist(client, self.shared.client_list):
            c = dict()
            c["address"]=client[0]
            c["port"]=client[1]
            c["errors"]=client[2]
            self.shared.client_list.append(c)

            # TODO store and reset if list of all connections is too large!
            if len(self.shared.client_list) > 99999:
                self.shared.client_list=[]
        else:
            self.client = self.shared.client_list[client_index(self.client,self.shared.client_list)]

    def help(self, *args):
        return [func for func in dir(self) if callable(getattr(self, func))]

    def __getattr__(self, attr):
        return "Function undefined "+str(attr)
