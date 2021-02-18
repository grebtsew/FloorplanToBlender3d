"""
Setup & Start Rest Apis and flask
"""

from shared_variables import shared_variables
from flask_handler import start_flask_application
from file_handler import ConfigHandler
import webbrowser

[HOST, PORT] = ConfigHandler().get_all("Website") 
url = "http://"+HOST+":{0}".format(PORT)


if __name__ == "__main__":
    shared = shared_variables()

    server = Server(shared)

    threading.Timer(1, functools.partial( webbrowser.open, url )).start()
    start_flask_application(shared)