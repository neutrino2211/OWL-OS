#@owldoc
'''@
This file contains the important Filesystem classes that store,encrypt,decrypt and link all nodes in the storage folder
@'''
from os import path
import gzip
import json
from typing import List
# from ..crypto import crypto

from ..errors import OWLPathError, OWLFileModeError, OWLException

store_path = "storage/"

def mkdir(p):
    m = {}
    m[p] = {}
    return m

def mkdirs(nodes:list):
    m = {}
    for n in nodes.reverse():
        m[n] = m
    return m

def make_dirs(p):
    if not exists("/".join(p.split("/")[:1])) :
        raise OWLPathError(p)
    m = json.loads(open("./storage/storagemap.json").read())
    counts = m
    parts = p.split('/')
    branch = counts
    for part in parts:
        branch = branch.setdefault(part, {})
    with open("./storage/storagemap.json","w") as f:
        f.write(json.dumps(counts))

def make_file(p,node_name):
    if not exists("/".join(p.split("/")[:1])) :
        raise OWLPathError(p)
    m = json.loads(open("./storage/storagemap.json").read())
    counts = m
    parts = p.split('/')
    branch = counts
    for part in parts[:-1]:
        branch = branch.setdefault(part, {})
    branch = branch.setdefault(parts[-1],node_name)
    with open("./storage/storagemap.json","w") as f:
        f.write(json.dumps(counts))

def exists(p:str) -> bool:
    nodes = p.split("/")
    if nodes[-1] == "":
        return True
    m = json.loads(open("./storage/storagemap.json").read())
    for i in p:
        if i in m.keys():
            m = m[i]
        else:
            return False
    return True

def dir_exists(p:str) -> bool:
    nodes = p.split("/")[:1]
    if nodes[-1] == "":
        return True
    m = json.loads(open("./storage/storagemap.json").read())
    for i in p:
        if i in m.keys():
            m = m[i]
        else:
            return False
    return True

class FSNode:
    '''
    `FSNode:`
        Base class for all filesystem content
    '''
    parent = None
    path = ""
    is_directory: bool = False
    m : dict = json.loads(open("./storage/storagemap.json").read())
    def make_node_name(self) -> str:
        return "node_"+str(len(path.os.listdir(store_path))-1) if not self.node_path_exists() else self.get_node_path()

    def node_path_exists(self) -> bool:
        nodes = self.path.split("/")
        m = self.m
        for _p in nodes:
            if not _p in m.keys():
                return False
            m = m[_p]
        return True
        
    def get_node_path(self):
        if self.path == "":
            return self.m
        nodes = self.path.split("/")
        exists = True
        m = self.m
        for _p in nodes:
            # print(_p,m.keys())
            if _p in m.keys():
                m = m[_p]
            else:
                exists = False
                break
        return m if exists else None
    
    def update_map(self):
        print(m)

class FSFile(FSNode):
    '''
    `FSFile:`
        File-like object supporting the core file operations
    '''
    def __init__(self,p,crypto,mode="r"):
        if not self.node_path_exists() and mode == "r":
            raise OWLPathError(p)
        self.eof = False
        self.path = p
        self.line = 0
        self.mode = mode
        self.lines = []
        self.name = p.split("/")[-1]
        self.is_write = self.mode.find("r")==-1
        np = self.get_node_path()
        ex = dir_exists(self.path)
        if np:
            if type(np) == dict:
                raise OWLException("{} is a directory".format(self.path))
            self.file = open(store_path+np,mode+"b")
        elif mode == "w" and ex:
            np = self.make_node_name()
            make_file(self.path,np)
            self.file = open(store_path+np,mode+"b")
        else:
            raise OWLPathError(p,reason="Non-existent")
            
        self.content = ""
        self.crypto = crypto
        if self.mode.find("r") != -1:
            self.content = gzip.decompress(self.file.read()).decode("ISO-8859-5")
            self.lines = crypto.decrypt(self.content).split(chr(0xa))

    def open(self,mode="r"):
        return self.__init__(self.path,self.crypto,mode)

    def read(self,size=None) -> str:
        size = size or len(self.content)
        return self.crypto.decrypt(self.content[:size]).replace("\\r","\r").replace("\\n","\n")

    def readline(self) -> str:
        if self.is_write :
            raise OWLFileModeError(self.mode,"readline")
        if len(self.lines)-1 == self.line:
            self.eof = True
        elif len(self.lines) <= self.line:
            raise IndexError()
        l = self.crypto.decrypt(self.lines[self.line]).replace("\\r","\r").replace("\\n","\n")
        self.line += 1
        return l

    def readlines(self) -> list:
        if self.is_write:
            raise OWLFileModeError(self.mode,"readlines")
        l = []
        for line in self.lines:
            l.append(self.crypto.decrypt(line).replace("\\r","\r").replace("\\n","\n"))
        return l

    def write(self,content):
        if not self.is_write:
            raise OWLFileModeError(self.mode,"write")
        enc = self.crypto.encrypt(content)
        self.content = enc

    def writeline(self,line):
        if not self.is_write:
            raise OWLFileModeError(self.mode,"writeline")
        self.content += self.crypto.encrypt(line+"\n")
    
    def writelines(self,lines):
        for l in lines:
            self.writeline(l)

    def close(self):
        if self.is_write :
            self.file.write(gzip.compress(bytes(self.content,"ISO-8859-5")))
        self.file.close()
    
    def __str__(self):
        return "{} [f]".format(self.path)

    def __format__(self,_):
        return "{} [f]".format(self.path)

class FSDirectory(FSNode):
    children : List[FSNode] = []
    children_map : dict = {}

    def __str__(self):
        return "{} [d]".format(self.path)

    def __format__(self,_):
        return "{} [d]".format(self.path)

    def __init__(self,p,crypto):
        self.path = p
        self.name = p.split("/")[-1]
        self.is_directory = True
        self.crypto = crypto
    
    def create(self):
        np = self.get_node_path()
        crypto = self.crypto
        if type(np) != dict:
            raise OWLException("{} is not a directory".format(self.path))
        for k in np.keys():
            if k == "" and type(np[k]) == dict:
                for j in np[k].keys():
                    if type(np[k]) == dict:
                        d = FSDirectory("/"+j,self.crypto)
                        d.create()
                        self.children.append(d)
                        d.parent = self
                    else:
                        f = FSFile("/"+j,self.crypto)
                        self.children.append(f)
                        f.parent = self

            elif type(np[k]) == dict:
                d = FSDirectory(self.path+"/"+k,self.crypto)
                d.create()
                self.children.append(d)
                d.parent = self
            else:
                f = FSFile(self.path+"/"+k,self.crypto)
                self.children.append(f)
                f.parent = self
        children = []
        children_map = {}
        for c in self.children:
            if c.parent.path == self.path:
                children.append(c)
                children_map[c.name] = c
        self.children = children
        self.children_map = children_map
        return self #Method chaining

root = None