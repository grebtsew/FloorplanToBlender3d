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

def undefined(*args):
        return "Function not defined!"

class Api():
    def __init__(self, client,  shared_variables):
        self.shared = shared_variables
        self.client = client
        self.dispatched_calls = {
            "help":      self.help
        }

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
        method_list = [func for func in dir(self) if callable(getattr(self, func)) and "__" not in func]
        method_args_list = []
        for method in method_list:
            # TODO, remove self and api_ref
            # TODO, add function comments as new field!
            argc = getattr(self, method).__code__.co_argcount
            argv = getattr(self, method).__code__.co_varnames[:argc]
            tmp = (method,argc,argv)
            method_args_list.append(tmp)
        return str(method_args_list)

    def __getattr__(self, attr):
        if attr in self.dispatched_calls:
            return self.dispatched_calls[attr]
        else:
            return undefined