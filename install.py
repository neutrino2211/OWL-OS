#@owldoc

'''@
This file is used to setup crucial aspects of the virtual operating system
e.g Crypto
@'''
import random
from os import path, makedirs, walk, remove
from sys import argv

'''@
:class
## InstallTask
Wrapper for all operations to be performed when installing the system
@'''

class InstallTask():
    '''@
    :function
    ## InstallTask.__init__
    Store task name and arguments
    @'''
    '''@
    :variable `InstallTask.name`: Task name used during logging to keep track of currently executing tasks
    @'''
    '''@
    :variable `InstallTask.args`: Arguments passed via the command line (in dict form)
    @'''
    def __init__(self,name,args):
        self.name = name
        self.args = args


    '''@
    :function
    ## InstallTask.confirm_path
    Utility function for all tasks to use when trying to confirm a file exists outside the sandbox
    @'''
    def confirm_path(self,p):
        if not path.exists(path.dirname(p)):
            makedirs(path.dirname(p))

    '''@
    :function
    ## InstallTask.get_arg
    Utility function that type checks and returns arguments for all tasks to use when retrieving an argument
    @'''

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

    '''@
    :function
    ## InstallTask._run
    Entry point wrapper for all tasks
    @'''

    def _run(self):
        self.run(self.args)
    '''@
    :function
    ## InstallTask.log
    Utility function that logs task message and name for easy debugging
    @'''
    def log(self,txt):
        p("Task [%s]: %s"%(self.name,txt))

'''@
:function
## arguments
Converts sys.argv into a dict of arguments to value of the format `--<option>=<value>`
@'''

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

'''@
:function
## sxor
Rudimentry imlementation of xor-ing strings
@'''

def sxor(s1,s2):    
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
def p(args): print(args)

args = arguments(argv[1:])

'''@
:class
## CryptoTask(InstallTask)
Task to setup crypto values e.g key
@'''
class CryptoTask(InstallTask):
    def run(self,args):
        self.confirm_path("./config/crypto")
        r = self.get_arg("crypt-cycles") or 64
        ks = self.get_arg("crypt-key-size") or 32

        self.log("Generating key")
        s = ''.join(chr(random.randint(0,255)) for _ in range(ks))
        for i in range(r):
            s = sxor(s,''.join(chr(random.randint(0,255)) for _ in range(ks)))
        with open("./config/crypto","wb") as f:
            f.write(bytes(s[:ks],'utf-8'))
        self.log("key saved")

'''@
:class
## FSTask(InstallTask)
Task to setup filesystem
@'''

class FSTask(InstallTask):
    def run(self,args):
        self.log("Initializing, filesystem")
        mypath = "./storage"
        for root, dirs, files in walk(mypath):
            for file in files:
                if file != "storagemap.json":
                    remove(path.join(root, file))
        self.confirm_path("./storage/storagemap.json")
        with open("./storage/storagemap.json","w") as f:
            f.write("{}")
        # Imports
        from libraries.bundle import FQL, unbundle
        from libraries import filesystem
        from libraries import Config
        from libraries.crypto import OWLCrypto
        filesystem.make_dirs("/Applications")
        config = Config()
        crypto = OWLCrypto(config.get_val("crypto"))
        config.lock()
        
        self.log("Installing apps")
        apps_file = self.get_arg('apps-file') or "./install/apps.fz"
        apps = FQL.unpack(apps_file)
        for app in apps:
            app_bundle = FQL.frombits(FQL.FUnassign(FQL.FUnassign2(app.split("?")[0])))
            app_id, app_name, main_entry,assets = unbundle.main([unbundle.byteify(app_bundle)])
            self.log("Installing [{}]".format(app_id))
            filesystem.make_dirs("/Applications/"+app_id)
            filesystem.make_dirs("/Applications/"+app_id+"/assets")
            app_index = filesystem.FSFile("/Applications/"+app_id+"/index.html",crypto,mode="w")
            app_index.write(str(main_entry)[2:-1])
            # print(main_entry)
            app_index.close()
            for k in assets:
                key = k[1:]
                asset_path = "/".join(k.split("\\"))
                self.log("Adding [{0}{1}]".format(app_id,asset_path))
                asset_file = filesystem.FSFile("/Applications/"+app_id+"/assets"+asset_path,crypto,mode="w")
                asset_file.write(assets[k])
                asset_file.close()
        self.log("Restoring crypt key..")
        crypto.restore_key()
        self.log("Done")

'''@
:function
## run_tasks
Run tasks given as arguments
@'''

def run_tasks(tasks):
    for t in tasks:
        t._run()

'''@
:function
## main
Entry point for install procedure
@'''
def main(args):
    run_tasks([
        CryptoTask("crypto",args),
        FSTask("FS",args)
    ])

if __name__ == "__main__":
    main(args)