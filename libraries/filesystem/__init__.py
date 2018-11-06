from os import path
from ..errors import OWLPathError, OWLFileModeError

store_path = "storage/"

class FSFile():
    def __init__(self,p,mode="r"):
        p = store_path+p
        if not path.exists(path.dirname(p)):
            raise OWLPathError(p)
        self.eof = False
        self.path = p
        self.line = 0
        self.mode = mode
        self.is_write = self.mode.find("r")==-1
        self.file = open(p,mode)
        self.content = ""
        if self.mode.find("r") != -1:
            self.content = self.file.read()
            self.lines = self.content.split(chr(0xa))

    def read(self,size=None):
        size = size or len(self.content)
        return self.content[:size]

    def readline(self):
        if self.is_write :
            raise OWLFileModeError(self.mode,"readline")
        if len(self.lines)-1 == self.line:
            self.eof = True
        elif len(self.lines) == self.line:
            raise IndexError()
        l = self.lines[self.line]
        self.line += 1
        return l

    def readlines(self):
        if self.is_write:
            raise OWLFileModeError(self.mode,"readlines")
        return self.lines

    def write(self,content):
        if not self.is_write:
            raise OWLFileModeError(self.mode,"write")
        self.content = content

    def writeline(self,line):
        if not self.is_write:
            raise OWLFileModeError(self.mode,"writeline")
        self.content += line+"\n"
    
    def writelines(self,lines):
        for l in lines:
            self.writeline(l)

    def close(self):
        if self.is_write :
            self.file.write(self.content)
        self.file.close()