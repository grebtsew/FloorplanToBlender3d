"""
Start Generate functions
Move swagger.json to correct folder
Edit index.html in neccessary
Start Swagger gui
"""
"""
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""
import os
import re
import time
import shutil
import webbrowser
from multiprocessing import Process
from http.server import HTTPServer, SimpleHTTPRequestHandler
from os.path import basename

from swagger.json_generator import generate_swagger_json


class Swagger:
    def __init__(self, shared_variables=None):
        self.shared = shared_variables
        self.PORT = self.shared.swaggerPort
        self.HOST = self.shared.swaggerHost
        self.swagger_path = "./swagger/swagger-json/swagger.json"

    def start(self):
        # Build swagger.json
        generate_swagger_json()
        # Start api
        browser = OpenApiBrowser(
            port=self.PORT, host=self.HOST, json_path=self.swagger_path
        )
        browser.start()


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)


class OpenApiBrowser(object):
    """
    Browser a local API specification (JSON file) with default browser.
    """

    def __init__(self, port, host, json_path, verbose=True):
        self.PORT = port
        self.HOST = host
        self.json_path = json_path
        self.verbose = verbose

    def run_webui_server(self, root_path):
        """
        Run simple HTTP server from some root path.
        """
        os.chdir(root_path)
        server_address = (self.HOST, int(self.PORT))
        handler = CORSRequestHandler
        httpd = HTTPServer(server_address, handler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

    def open_browser(self, url):
        """
        Open given URL with default browser (to be called from a different process).
        """
        webbrowser.open_new(url)

    def inject_spec_file(self, dist_path):
        """
        Copy Swagger/OpenAPI specification JSON file into Swagger-UI folder.
        """
        if self.verbose:
            print("copying {} to {}".format(self.json_path, dist_path + "/"))
        shutil.copy(self.json_path, dist_path + "/")

    def modify_start_url(self, index_path):
        """
        Modify the default URL in index.html to point to given specification file.
        """
        if self.verbose:
            print("replacing start URL in {} ".format(index_path))
        html = open(index_path).read()
        default_url = "http://petstore.swagger.io/v2/swagger.json"
        new_url = "http://0.0.0.0:" + str(self.PORT) + "/" + basename(self.json_path)
        html1 = re.sub(default_url, new_url, html)
        print(len(html1))

        with open(index_path, "wb") as f:
            f.write(bytes(html1, encoding="utf-8"))

    def run_webui_process(self, address, path):
        """
        Run a webserver showing the Swagger-UI at some path.
        """
        if self.verbose:
            print("starting webserver on {}".format(address))
        p1 = Process(target=self.run_webui_server, args=(path,))
        p1.start()
        return p1

    def open_webui(self, address):
        """
        Open the Swagger-UI in a webbrowser.
        """
        if self.verbose:
            print("opening webbrowser on {}".format(address))
        p2 = Process(target=self.open_browser, args=(address,))
        p2.start()
        return p2

    def wait_until_interrupted(self, p1, p2):
        """
        Wait until next KeyboardInterrupt, then exit the completed processes.
        """
        try:
            p1.join()
            p2.join()
        except KeyboardInterrupt:
            pass
        if self.verbose:
            print()
            print("terminating webserver")
            print("(Swagger-UI should still work, but not reloading the page!)")

    def start(self):
        """
        Do all the necessary work.
        """
        self.inject_spec_file("./swagger/swagger-ui")
        self.modify_start_url("./swagger/swagger-ui" + "/index.html")

        # set-up two processes to run in parallel, one for running a webserver,
        # the other for opening a webbrowser showing what the first is serving
        address = (
            "http://" + self.HOST + ":" + str(self.PORT)
        )  # might not want to do this in docker!
        p1 = self.run_webui_process(address, "./swagger/swagger-ui")
        time.sleep(0.5)
        p2 = self.open_webui(address)
        self.wait_until_interrupted(p1, p2)
