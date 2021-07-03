#@owldoc
'''@
This file contains the operating system main ui thread and the fs server @ :10000
@'''
import threading
import webview
import socket
import signal
import sys

from urllib import parse
from libraries import Config
from libraries import filesystem
from libraries import gecko_byte_code
from libraries.crypto import OWLCrypto
from http.server import BaseHTTPRequestHandler, HTTPServer

if filesystem.path.os.name != "nt":
    import owlapi
else:
    # TODO make windows specific native modules
    pass

sock = None
shutdown = False
crypto = None
c = Config()
class JSInterface:
    def __init__(self, key):
        self._key = key
    def debug(self, param):
        print(param)
        return

    def gecko(self, param):
        gecko_byte_code.loop(param,webview)

    def toggle_fullscreen(self,param):
        webview.toggle_fullscreen()

    def key(self, param):
        k = self._key.decode("ISO-8859-5")
        return k

def await_sigint(sig, frame):
    graceful_exit()
    

def sandbox_observer_thread():
    global sock
    class Server(BaseHTTPRequestHandler):
 
        # GET
        def do_GET(self):
            parsed_path = parse.urlparse(self.path)
            host = self.headers.get("Host")
            if host != "localhost:10000" and host != "127.0.0.1:10000":
                return
            paths = parsed_path.path.split("/")
            self.send_response(200)
            self.end_headers()
            node = filesystem.root
            for p in paths[1:]:
                if p in node.children_map.keys():
                    node = node.children_map[p]
            # print(node.children[1], paths)
            message = node.read()
            self.wfile.write(message.encode('utf-8'))
            return 200

    sock = HTTPServer(('127.0.0.1',10000),Server)
    sock.serve_forever()
def graceful_exit():
    global sock
    if crypto:
        crypto.restore_key()
    shutdown = True
    sock.shutdown()
    sock.server_close()
    print("Socket closed")

def init():
    global crypto
    key = c.get_val("crypto")
    crypto = OWLCrypto(key)
    c.lock()
    crypto.export()
    # inf = owlapi.get_sys_info()
    # hello_file = filesystem.FSFile("/README.txt",crypto)
    # print(hello_file.read())
    # c.set_val("cpu.clock_speed",inf["clock_speed"])
    print("Mounting FS")
    filesystem.root = filesystem.FSDirectory("",crypto).create()
    print("Done")
    # try:
    #     print(filesystem.root.children[0].path)
    # except Exception as e:
    #     import traceback
    #     print(traceback.print_exception(*sys.exc_info()))
    api = JSInterface(key)
    del key
    t = threading.Thread(target=sandbox_observer_thread)
    t.start()
    signal.signal(signal.SIGINT,await_sigint)
    window = webview.create_window("OWL-OS", url="./index.html", js_api=api)
    # window.toggle_fullscreen()
    webview.start(gui='gtk', debug=True)