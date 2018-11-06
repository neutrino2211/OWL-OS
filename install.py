import random
from os import path, makedirs
from sys import argv

class InstallTask():
    def __init__(self,name,args):
        self.name = name
        self.args = args

    def confirm_path(self,p):
        if not path.exists(p):
            makedirs(path.dirname(p))

    def get_arg(self,a):
        r = None
        try:
            r = self.args[a]
        except KeyError:
            pass
        try:
            r = int(self.args[a])
        except Exception:
            pass
        return r

    def _run(self):
        self.run(self.args)
    
    def log(self,txt):
        p("Task [%s]: %s"%(self.name,txt))

def arguments(argv):
    d = {}
    for a in argv:
        if a.startswith("--"):
            if a.index("=") != -1:
                aa = a.split("=")
                d[aa[0][2:]] = aa[1]
            else:
                d[aa[0][2:]] = True
    return d

def sxor(s1,s2):    
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
def p(args): print(args)

args = arguments(argv[1:])

class CryptoTask(InstallTask):
    def run(self,args):
        self.confirm_path("./config/crypto")
        r = self.get_arg("crypt-cycles") or 64

        self.log("Generating key")
        s = ''.join(chr(random.randint(0,255)) for _ in range(64))
        for i in range(r):
            s = sxor(s,''.join(chr(random.randint(0,255)) for _ in range(64)))
        with open("./config/crypto","wb") as f:
            f.write(s)
        self.log("key saved")

def run_tasks(tasks):
    for t in tasks:
        t._run()

run_tasks([
    CryptoTask("crypto",args)
])