import threading
import webview
import signal
import sys

from libraries import Config
from libraries import filesystem
from libraries.crypto import OWLCrypto
from libraries import gecko_byte_code

import owlapi

shutdown = False
crypto = None
c = Config()
class JSInterface:
    def debug(self, param):
        print(param)
        return

    def gecko(self, param):
        gecko_byte_code.loop(param,webview)

    def toggle_fullscreen(self,param):
        webview.toggle_fullscreen()

def await_sigint(sig, frame):
    graceful_exit()
    

def sandbox_observer_thread():
    print(".")

def graceful_exit():
    if crypto:
        crypto.restore_key()
    if webview.window_exists():
        webview.destroy_window()
    shutdown = True

def init():
    global crypto
    key = c.get_val("crypto")
    crypto = OWLCrypto(key)
    c.lock()
    del key
    inf = owlapi.get_sys_info()
    c.set_val("cpu.clock_speed",inf["clock_speed"])
    try:
        f = filesystem.FSFile("test.txt",crypto,mode="w")
        string = '''
        Hello guys hopefully it encodes
        newlines and 
            tabs.
        '''
        f.write(string)
        f.close()

        f = filesystem.FSFile("test.txt",crypto)
        print(f.read())
        f.close()
    except Exception as e:
        import traceback
        traceback.print_exception(*sys.exc_info())
    api = JSInterface()
    t = threading.Thread(target=sandbox_observer_thread)
    t.start()
    signal.signal(signal.SIGINT,await_sigint)
    webview.create_window("OWL-OS", url="./index.html", js_api=api)