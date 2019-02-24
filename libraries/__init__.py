#@owldoc

'''@
This file contains the Config class which helps set and retrieve install and runtime configurations
@'''

from .errors import OWLObjectInstanceException
from os import path

init = True

class Config():
    def __init__(self):
        global init
        if not init:
            raise OWLObjectInstanceException("Config should have only one instance")
        init = False
        self.__lock = False
    
    def lock(self):
        self.__lock = True

    def get_val(self,name):
        w = ["config"]
        w.extend(name.split("."))
        p = "/".join(w)
        if self.__lock and name == "crypto":
            return None
        with open(p,"rb") as f:
            r = f.read()
            return r
    
    def set_val(self,name,val):
        if name == "crypto":
            return None
        w = ["config"]
        w.extend(name.split("."))
        p = "/".join(w)
        if not path.exists(p):
            path.os.makedirs(path.dirname(p))
        with open(p,"w") as f:
            f.write(str(val))
