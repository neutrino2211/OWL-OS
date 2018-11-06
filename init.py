import threading
import webview
import signal
import sys

from libraries import Config
from libraries import filesystem
from libraries.crypto import OWLCrypto

#OWL-OS C++ API
import owlapi

shutdown = False
crypto = None
c = Config()
class JSInterface:
    def debug(self, param):
        print(param)
        return

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
    key = c.get_val("config.crypto")
    crypto = OWLCrypto(key)
    c.lock()
    del key
    owlapi.get_cpu_id()
    api = JSInterface()
    t = threading.Thread(target=sandbox_observer_thread)
    t.start()
    signal.signal(signal.SIGINT,await_sigint)
    webview.create_window("OWL-OS", url="./index.html", js_api=api)