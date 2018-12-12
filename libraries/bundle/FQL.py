#@owldoc

import os
import sys
import zlib
'''@
This file contains all the logic needed t handle FlameZip (.fz)
@'''

'''@
:function `byteify`
Workaround for converting str to bytes due to Encoding issues with using bytes()
@'''
def byteify(s):
    arr = []
    for c in s:
        arr.append(ord(c))
    return bytearray(arr)


'''@
:function `FMap`
This function converts a string like "0010010001" to a list [00,10,01,00,01]
@'''

def FMap(string):
    s = []
    d = ""
    for c in string:
        if len(d) == 2:
            s.append(d)
            d = ""
        d+=c
    s.append(d)
    if len(s) > 1:
        if s[1] == "":
            s = s[1:]
    return s


def FAssign(iterable):
    m = ""
    for i in iterable:
        if i == "00":
            m+="a"
        elif i == "01":
            m+="b"
        elif i == "10":
            m+="c"
        elif i == "11":
            m+="d"
    return m

def FUnassign(iterable):
    m = ""
    for i in iterable:
        if i == "a":
            m+="00"
        elif i == "b":
            m+="01"
        elif i == "c":
            m+="10"
        elif i == "d":
            m+="11"
    return m

def FUnassign2(iterable):
    m = ""
    for i in iterable:
        if i == "e":
            m+="aa"
        elif i == "f":
            m+="ab"
        elif i == "g":
            m+="ac"
        elif i == "h":
            m+="ad"
        elif i == "i":
            m+="ba"
        elif i == "j":
            m+="bb"
        elif i == "k":
            m+="bc"
        elif i == "l":
            m+="bd"
        elif i == "m":
            m+="ca"
        elif i == "n":
            m+="cb"
        elif i == "o":
            m+="cc"
        elif i == "p":
            m+="cd"
        elif i == "q":
            m+="da"
        elif i == "r":
            m+="db"
        elif i == "s":
            m+="dc"
        elif i == "t":
            m+="dd"
    return m

def FAssign2(iterable):
    m = ""
    for i in iterable:
        if i == "aa":
            m+="e"
        elif i == "ab":
            m+="f"
        elif i == "ac":
            m+="g"
        elif i == "ad":
            m+="h"
        elif i == "ba":
            m+="i"
        elif i == "bb":
            m+="j"
        elif i == "bc":
            m+="k"
        elif i == "bd":
            m+="l"
        elif i == "ca":
            m+="m"
        elif i == "cb":
            m+="n"
        elif i == "cc":
            m+="o"
        elif i == "cd":
            m+="p"
        elif i == "da":
            m+="q"
        elif i == "db":
            m+="r"
        elif i == "dc":
            m+="s"
        elif i == "dd":
            m+="t"
    return m

'''@
:class `FlameZipArchive`
Class for creating .fz archives
@'''

class FlameZipArchive():
    '''@
    :function `FlameZipArchive.__init__`
    Creates string which archive contents will be stored
    @'''
    def __init__(self):
        self.archive = ""
    def addToArchive(self,relativepath,content):
        self.archive += content+":"+relativepath+"z"
    def getArchive(self):
        self.archive
    
    '''@
    :function `FlameZipArchive.archiveFile`
    Hash file and return contents
    @'''
    def archiveFile(self,filepath):
        filepath = os.path.normpath(filepath)
        src = open(filepath,"rb")
        readtext = bytearray(src.read())
        bits = tobits(readtext)

        b = ""

        for byte in bits:
            b += str(byte)
        hash1 = FAssign2(FMap(FAssign(FMap(b))))

        return hash1+"?"+filepath
    '''@
    :function `FlameZipArchive.archiveDir`
    Archive all files in a dir and all sub-directories
    @'''
    def archiveDir(self,directory):
        archivedfiles = []
        for f in os.listdir(directory):
            if os.path.isdir(os.path.join(directory,f)):
                archivedfiles.extend(self.archiveDir(os.path.join(directory,f)))
            else:
                archivedfiles.append(self.archiveFile(os.path.join(directory,f)))

        return archivedfiles

def tobits(s):
    result = []
    for c in s:
        bits = bin(c)[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def pack(f):
    arg = f
    if not os.path.isdir(os.path.join(os.path.curdir,arg)):
        sys.stderr.write("Error : {} is not a directory.\n".format(arg))
        sys.exit()
    fz = FlameZipArchive()
    
    s = fz.archiveDir(os.path.join(os.getcwd(),arg))
    a = "*".join(s)

    comp = zlib.compress(byteify(a))
    return comp

def unpack(f):
    rftext = ""
    fz = open(f,"rb")
    rftext = fz.read()
    dec = str(zlib.decompress(rftext))[2:-1]

    l = dec.split("*")
    return l
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage FQL <pack|unpack> <source>")
        sys.exit()
    if sys.argv[1] == "pack":
        comp = pack(sys.argv[2])
        print("Writing {}".format(arg+".fz"))
        dest = open(arg+".fz","wb")
        dest.write(comp)
        dest.close()
    elif sys.argv[1] == "unpack":
        l = unpack(sys.argv[2])
        for d in l:
            df = d.split("?")
            dt = df[0]
            dp = df[1]
            # print dp
            if not os.path.exists(os.path.dirname(dp)):
                os.makedirs(os.path.dirname(dp))
            ff = open(dp,"wb")
            print("Unpacking "+dp)
            fu2 = FUnassign2(dt)
            fu = FUnassign(fu2)
            fb = frombits(fu)
            ff.write(byteify(fb))
            ff.close()
    else:
        print("Usage FQL <pack|unpack> <source>")
        sys.exit()