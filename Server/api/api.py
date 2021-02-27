
class Api():
    def __init__(self, client = None,  shared_variables = None):
        self.shared = shared_variables
        self.client = client

        # Store all new connections!
        if client not in self.shared.client_list:
            self.shared.client_list.append(client)

            # TODO store and reset if list of all connections is too large!
            if len(self.shared.client_list) > 999999:
                self.shared.client_list=[]
        else:
            self.client = self.shared.client_list(client)

    def __getattr__(self, attr):
        return "Function undefined "+str(attr)
