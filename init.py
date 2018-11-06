import threading
import webview
import signal
import sys

from libraries.video_stream import get_frame,close_stream
from libraries import Config
from libraries import filesystem
from libraries.crypto import OWLCrypto

#OWL-OS C++ API
import owlapi

crypto = None
c = Config()
class JSInterface:
    def debug(self, param):
        print(param)
        return
    def stream_video(self,param):
        while True:
            try:
                frame = get_frame()
                # print("OWL."+param+"(\"{}\")".format(frame[2:-1]))
                webview.evaluate_js("OWL."+param+"(\"{}\")".format(frame))
            except Exception:
                print("STREAM_CLOSED")
                break
    def close_video_stream(self,param):
        close_stream()

    def toggle_fullscreen(self,param):
        webview.toggle_fullscreen()

def await_sigint(sig, frame):
    graceful_exit()
    

def sandbox_observer_thread():
    print(".")

def graceful_exit():
    if crypto:
        crypto.restore_key()
    close_stream()
    if webview.window_exists():
        webview.destroy_window()

def init():
    global crypto
    key = c.get_val("config.crypto")
    c.lock()
    crypto = OWLCrypto(key)
    del key
    owlapi.get_cpu_id()
    api = JSInterface()
    t = threading.Thread(target=sandbox_observer_thread)
    t.start()
    signal.signal(signal.SIGINT,await_sigint)
    webview.create_window("OWL-OS", url="./index.html", js_api=api)