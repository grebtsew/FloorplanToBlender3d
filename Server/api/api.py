import json

"""
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""


def client_exist(client, client_list):
    for c in client_list:
        if c["address"] == client["address"] and c["port"] == client["port"]:
            return True
    return False


def client_index(client, client_list):
    i = 0
    for c in client_list:
        if c["address"] == client["address"] and c["port"] == client["port"]:
            return i
        i += 1
    return i


def undefined(*args):
    return "Function not defined!"


def stringifydictvalues(d):
    """Recursive function that stringifies all values in dicts!"""
    for k, v in d.items():
        if isinstance(v, dict):
            stringifydictvalues(v)
        else:
            v = str(v)
            d.update({k: v})
    return d


class Api:
    def __init__(self, client, shared_variables):
        self.shared = shared_variables
        self.client = client
        self.dispatched_calls = {"help": self.help}

        # Store all new connections!
        if not client_exist(self.client, self.shared.client_list):
            client["Errors"] = 0
            self.shared.client_list.append(client)

            # TODO store and reset if list of all connections is too large!
            if len(self.shared.client_list) > 99999:
                self.shared.client_list = []
        else:
            self.client = self.shared.client_list[
                client_index(self.client, self.shared.client_list)
            ]

    def help(self, *args, **kwargs) -> str:
        """This is a crucial function that returns data for generating swagger.json"""
        method_list = [
            func
            for func in dir(self)
            if callable(getattr(self, func)) and "__" not in func
        ]
        method_args_list = []

        for method in method_list:
            res = dict()

            argc = getattr(self, method).__code__.co_argcount
            argv = getattr(self, method).__code__.co_varnames[:argc]
            filter_argv = [
                func for func in argv if not func.startswith("_") and func != "self"
            ]
            argc = len(filter_argv)

            res["method"] = method
            res["type"] = type(self).__name__

            query = []
            data = []
            if res["type"] == "Get":
                query = filter_argv
            elif res["type"] == "Post":
                data = filter_argv
            elif res["type"] == "Put":
                if "file" in filter_argv:
                    data.append("file")
                    query = filter_argv.copy()
                    query.remove("file")
                else:
                    query = filter_argv

            res["query"] = query  # create query
            res["data"] = data  # create json
            res["annotations"] = stringifydictvalues(
                getattr(self, method).__annotations__
            )
            res["argc"] = argc
            res["argv"] = filter_argv
            res["docs"] = getattr(self, method).__doc__
            method_args_list.append(res)
        return json.dumps(method_args_list)

    def __getattr__(self, attr):
        if attr in self.dispatched_calls:
            return self.dispatched_calls[attr]
        else:
            return undefined
