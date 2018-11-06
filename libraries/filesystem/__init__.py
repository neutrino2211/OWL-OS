from os import path
from ..errors import OWLPathError, OWLFileModeError

store_path = "storage/"

class FSFile():
    def __init__(self,p,mode="r"):
        p = store_path+p
        if not path.exists(path.dirname(p)):
            raise OWLPathError(p)
        self.path = p
        self.line = 0
        self.mode = mode
        self.is_write = self.mode.find("r")==-1
        self.file = open(p,mode)
        self.content = ""
        if self.mode.find("r") != -1:
            self.content = self.file.read()
            self.lines = self.content.split(chr(0xa))

    def read(self,size=-1):
        return self.file.read() if size==-1 else self.file.read(size)

    def readline(self):
        if self.is_write :
            raise OWLFileModeError(self.mode,"readline")
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