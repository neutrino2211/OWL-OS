from .errors import OWLObjectInstanceException

init = True

class Config():
    def __init__(self):
        global init
        if not init:
            raise OWLObjectInstanceException("Config should have only one instance")
        init = False
        self._lock = False
    
    def lock(self):
        self._lock = True

    def get_val(self,name):
        if self._lock and name == "config.crypto":
            return None
        with open("/".join(name.split(".")),"rb") as f:
            return f.read()
