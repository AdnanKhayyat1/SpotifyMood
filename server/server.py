# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple
import time
from model import Cache
import json
from constants import hostName, serverPort


class MyServer(BaseHTTPRequestHandler):
    
    def __init__(self, request, client_address, server) -> None:
        self.c = Cache()
        super().__init__(request, client_address, server)
    def do_GET(self):
        if self.path.startswith('/pl/'):
            preds = self.c.wrapped_fetch(self.path[4:])
            if not preds:
                self.send_response(404)
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                print(self.path[4:])
                res = json.dumps(preds)
                print(res)
                self.wfile.write(res.encode())
        else:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write('<html><body><h1>This is the server></h1></body></html'.encode())


        

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")