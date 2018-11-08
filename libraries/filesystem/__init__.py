from os import path
import gzip
from ..errors import OWLPathError, OWLFileModeError

store_path = "storage/"

class FSFile:
    def __init__(self,p,crypto,mode="r"):
        p = store_path+p
        if not path.exists(path.dirname(p)):
            raise OWLPathError(p)
        self.eof = False
        self.path = p
        self.line = 0
        self.mode = mode
        self.is_write = self.mode.find("r")==-1
        self.file = open(p,mode+"b")
        self.content = ""
        self.crypto = crypto
        if self.mode.find("r") != -1:
            self.content = gzip.decompress(self.file.read()).decode("ISO-8859-5")
        self.lines = crypto.decrypt(self.content).split(chr(0xa))

    def read(self,size=None):
        size = size or len(self.content)
        return self.crypto.decrypt(self.content[:size])

    def readline(self):
        if self.is_write :
            raise OWLFileModeError(self.mode,"readline")
        if len(self.lines)-1 == self.line:
            self.eof = True
        elif len(self.lines) == self.line:
            raise IndexError()
        l = self.crypto.decrypt(self.lines[self.line])
        self.line += 1
        return l

    def readlines(self):
        if self.is_write:
            raise OWLFileModeError(self.mode,"readlines")
        l = []
        for line in self.lines:
            l.append(self.crypto.decrypt(line))
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