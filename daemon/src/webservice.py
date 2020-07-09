import cgi
import json
import re
import threading
from argparse import ArgumentParser
from cgi import parse_header
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from openalpr import Alpr

HTTP_CODE_BAD_REQUEST = 400

alpr = Alpr(country="gb", config_file="/etc/openalpr/openalpr.conf", runtime_dir="/usr/share/openalpr/runtime_data")


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        jsontxt = "{}"
        if None != re.search('/api/v1/identify', self.path):
            ctype, pdict = parse_header(self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = self.headers.get_content_type()
            if ctype == 'multipart/form-data':
                postvars = cgi.parse_multipart(self.rfile, pdict)

                image_ = postvars['image'][0]

                data = alpr.recognize_array(image_)
                jsontxt = json.dumps(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(jsontxt.encode(encoding='utf_8'))
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer:
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)

    def start(self):
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def stop(self):
        self.server.shutdown()
        self.waitForThread()


if __name__ == "__main__":
    parser = ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server', default=8080)
    parser.add_argument('ip', help='HTTP Server IP', default="127.0.0.1")
    args = parser.parse_args()

    server = SimpleHttpServer(args.ip, args.port)
    print('HTTP Server Running...........')
    server.start()
    server.waitForThread()
