from threading import Thread
from functools import partial
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
import cgi

from http.server import BaseHTTPRequestHandler, HTTPServer

from api.post import Post
from api.put import Put
from api.get import Get

class S(BaseHTTPRequestHandler):

    def __init__(self, shared, *args, **kwargs):
        self.shared = shared
        super().__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200, "OK")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'POST, PUT, OPTIONS, HEAD, GET')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_response()

    def do_OPTIONS(self):
        self._set_response()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        client = (self.client_address,self.address_string())
        try:
            function = parse_qs(parsed_path.query)['func'][0]
        except Exception as e:
            message = "RECIEVED GET REQUEST WITH BAD QUERY: "+str(e)
            print(message)
        finally:
            message = getattr(Get(client=client,shared_variables=self.shared), function)(self, parsed_path)
        self._set_response()
        self.wfile.write(bytes(message, encoding="utf-8"))


    def do_PUT(self):
        
        ctype, pdict = cgi.parse_header(self.headers.getheader('Content-Type'))
        print(ctype, pdict)
        if ctype == 'multipart/form-data':
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            try:
                data = json.loads(put_data.decode('utf-8'))
                function = data['func']
                message = getattr(Put(client=client,shared_variables=self.shared), function)(self, data)

            except ValueError as e:
                message = "RECIEVED POST REQUEST WITH BAD JSON: "+str(e)
                print(message)

        else:
            message = "RECIEVED PUT REQUEST WITH BAD CTYPE: "+str(ctype)
            print(message)
        self._set_response()
        self.wfile.write(bytes(message, encoding="utf-8"))


    def do_POST(self):
        if self.headers['Content-Length']:
            response = ""
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            client = (self.client_address,self.headers)
            # decode incoming data 
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                function = data['func']
                response = getattr(Post(client=client,shared_variables=self.shared), function)(self, data)
                
            except ValueError as e:
                response = "RECIEVED POST REQUEST WITH BAD JSON: "+str(e)
                print(response)

        self._set_response()
        self.wfile.write(bytes(response, encoding="utf-8"))
        

class Server(Thread):
    def __init__(self, shared):
        super().__init__()
        self.shared = shared

    def run(self):
        server_address = (self.shared.restapiHost, int(self.shared.restapiPort))
        httpd = HTTPServer(server_address, partial(S, self.shared))
        try:
            print("REST API SERVER up and serving at ", self.shared.restapiHost, self.shared.restapiPort)
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()