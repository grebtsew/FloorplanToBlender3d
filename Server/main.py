"""
Setup & Start Rest Apis and flask
"""

from shared_variables import shared_variables
#from flask_handler import start_flask_application

#import webbrowser
from api.server import Server

if __name__ == "__main__":
    shared = shared_variables()

    server = Server(shared).start()

    #threading.Timer(1, functools.partial( webbrowser.open, url )).start()
    #start_flask_application(shared)