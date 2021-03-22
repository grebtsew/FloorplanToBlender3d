"""
Setup & Start Rest Apis and flask
"""

from shared_variables import shared_variables
from swagger.swagger_flask import Swagger

#import webbrowser
from api.server import Server

if __name__ == "__main__":
    shared = shared_variables()

    server = Server(shared).start()

    swagger = Swagger(shared).start()

# TODO : add flask gui here!