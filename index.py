import threading
import webview
import signal
import sys

#OWL-OS C++ API
import owlapi

class JSInterface:
    def debug(self, param):
        print(param)
        owlapi.helloworld()
        return

def await_sigint(sig, frame):
    webview.destroy_window()
    sys.exit(0)

def sandbox_observer_thread():
    print(".")

api = JSInterface()
t = threading.Thread(target=sandbox_observer_thread)
t.start()
signal.signal(signal.SIGINT,await_sigint)
webview.create_window("Ureno", url="./index.html", js_api=api)