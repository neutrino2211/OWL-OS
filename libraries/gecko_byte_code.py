#@owldoc

'''@
This is the gecko mini code interpreter
@'''

import sys

class VirtualFile():
    def __init__(self,code):
        self.code = code
    def read(self):
        return "\n".join(self.code)
    def readlines(self):
        return self.code.split("\n")
class Interpreter():
    def __init__(self,file,routine_name="",start_line=0,wv=None):
        if file != "":
            self.code = open(file)
        if wv:
            self.wv = wv
        self.name = file if file != "" else routine_name
        self.maxm = 0
        self.line = start_line+1
        self.flags = {}
        self.memory = []
        self.variables = {}
        self.functions = {}
        self.subroutine = False
        self.subroutines = {}
        self.memory_spaces = {
            "M1": [],
            "M2": [],
            "M3": [],
            "M4": [],
            "M5": [],
            "M6": [],
            "M7": [],
            "M8": []
        }
        self.return_pointer = 0
        self.subroutinecode = []
        self.instruction_pointer = 0
    def loop(self):
        lines = self.code.readlines()
        ln = len(lines)
        # print(lines)
        while self.instruction_pointer < ln:
            line = lines[self.instruction_pointer]
            if not line.startswith("#") :
                b = self.breakStatement(line)
                # print(lines)
                self.execute(b)
            self.line = self.line+1
            self.instruction_pointer += 1
            # print(line,end="")
        # print()

    def breakStatement(self,statement):
        # print(statement)
        r = []
        e = True
        t = ""
        s = statement.strip()
        # print(statement)
        for c in s:
            if c == "'":
                e = not e
                t += c
            elif c == " " and e:
                if t != "":
                    r.append(t)
                    t = ""
            else:
                t += c
        r.append(t)
        return r
    def execute(self,arr):
        # print(arr)
        if arr[0] != "" :
            # print("Gotcha")
            try:
                if not self.subroutine:
                    self.functions[arr[0]](self,arr[1:])
                else:
                    # print("~"+arr[0]+"~")
                    if arr[0] == "end":
                        # print("End")
                        self.functions[arr[0]](self,arr[1:])
                    else:
                        self.subroutinecode.append(" ".join(arr))
            except KeyError as e:
                print("Error at line "+str(self.line)+" : "+arr[0]+" is not a valid code [{routine}]".format(routine=self.name))
                sys.exit()


    def loadFunction(self,name,f):
        self.functions[name] = f
        # pass
    def convertInt(self,i):
        r = 0
        try:
            r = int(i,10)
        except Exception as e:
            r = int(1,16)
        return r

    def resolveValue(self,a):
        try:
            try:
                return int(a,10)
            except Exception as e:
                return int(a,16)
        except Exception as e:
            pass
        if type(a) == int:
            return a
        elif a.startswith("@"):
            return self.variables[a[1:]]
        elif a.startswith("%"):
            return self.memory_spaces[a[1:]]
        elif a.startswith("'"):
            return a[1:-1]
        elif a.startswith("$"):
            return self.flags[a[1:]]
        elif a.startswith("^"):
            return type(self.resolveValue(a[1:]))
        elif a.startswith("{") and a.endswith("}"):
            return len(self.resolveValue(a[1:-1].strip()))
        elif a.startswith("[") and a.endswith("]"):
            inner = a[1:-1].strip()
            arr = inner.split("#")[0]
            index = inner.split("#")[1]
            # print("IN={0}, ARR={1}, RES1={2}, RES={3}".format(index,arr,self.resolveValue(arr),self.resolveValue(index)))
            return self.resolveValue(arr)[self.resolveValue(index)]

    def isDefinedSpace(self,v):
        # print(v)
        if len(v) == 0:
            return False
        for val in v:
            if val != 0:
                return False
        return True

def start(i,arg):
    i.maxm = int(arg[0])
    # print(i.maxm)
    for m in range(i.maxm):
        i.memory.append(0)

def db(i,arg):
    i.variables[arg[0]] = i.resolveValue(arg[1].strip())

def flag(i,arg):
    i.flags[arg[0]] = arg[1]

def mov(i,arg):
    if arg[0].startswith("%"):
        a1 = i.resolveValue(arg[1])
        # print("[mov] {}".format(a1))
        i.memory_spaces[arg[0][1:]] = a1
    else:
        a1 = i.resolveValue(arg[1])
    
        i.variables[arg[0][1:]] = a1

def put(i,arg):
    size = 0
    try:
        size = int(arg[1],10)
    except Exception as e:
        size = int(arg[1],16)
    # print(size,i.maxm,arg[1])
    if size < i.maxm:
        i.memory[size] = i.resolveValue(arg[0])
    else:
        print("Error at line "+str(i.line)+" : Invalid memory address allocation [{routine}]".format(routine=i.name))
        sys.exit()

def section(i,arg):
    i.subroutine = True
    i.subroutines[arg[0]] = Interpreter("",routine_name=arg[0],start_line=i.line)


def end(i,arg):
    i.subroutines[arg[0]].code = VirtualFile(i.subroutinecode)
    i.subroutinecode = []
    i.subroutine = False

def dec(i,arg):
    sub(i,[arg[0],1])

def inc(i,arg):
    add(i,[arg[0],1])

def sub(i,arg):
    if arg[0].startswith("@"):
        i.variables[arg[0][1:]] = i.resolveValue(arg[0])-i.resolveValue(arg[1])

def add(i,arg):
    if arg[0].startswith("@"):
        i.variables[arg[0][1:]] = i.resolveValue(arg[0])+i.resolveValue(arg[1])

def extern(i,arg):
    a = []
    for _i in range(1,8):
        if len(i.memory_spaces["M"+str(_i)]) != 0:
            a.append(i.memory_spaces["M"+str(_i)])
    js = arg[0]+"(\"{}\")".format(",".join(a))
    i.wv.evaluate_js(js)

def clearm(i,arg):
    i.memory_spaces["M1"] = []
    i.memory_spaces["M2"] = []
    i.memory_spaces["M3"] = []
    i.memory_spaces["M4"] = []
    i.memory_spaces["M5"] = []
    i.memory_spaces["M6"] = []
    i.memory_spaces["M7"] = []
    i.memory_spaces["M8"] = []

def allocate(i,arg):
    i.variables[arg[1]] = []
    if arg[0] != "%":
        for m in range(i.convertInt(arg[0])):
            i.variables[arg[1]].append(0)
        
def _print(i,arg):
    print(i.memory[0])

def _println(i,arg):
    print(i.memory[0])

def call(i,arg):
    for key in i.subroutines:
        if key != arg[0]:
            i.subroutines[arg[0]].subroutines[key] = i.subroutines[key]
    # print "Calling",arg[0]
    i.subroutines[arg[0]].functions = i.functions
    i.subroutines[arg[0]].variables = i.variables
    i.subroutines[arg[0]].memory_spaces = i.memory_spaces
    i.subroutines[arg[0]].flags = i.flags
    # print(i.subroutines[arg[0]].memory_spaces)
    # i.return_pointer = i.instruction_pointer
    i.subroutines[arg[0]].loop()
    # print "Called", arg[0]
    
def ret(i,arg):
    i.instruction_pointer = i.return_pointer
    # print("[ip]={}".format(i.instruction_pointer))

def push(i,arg):
    a1 = i.resolveValue(arg[0])
    if i.isDefinedSpace(i.variables[arg[1][1:]]):
        print("Error at line "+str(i.line)+" : Cannot push to a defined memory space [{routine}]".format(routine=i.name))
        sys.exit()
    else:
        i.variables[arg[1][1:]].append(a1)

def Set(i,arg):
    a1 = i.resolveValue(arg[1])
    
    i.variables[arg[0][1:]] = a1
    # print(i.variables[arg[0][1:]])



def _cmp(i,arg):
    v1 = i.resolveValue(arg[0])
    v2 = i.resolveValue(arg[1])

    i.flags["cmp"] = True if v1==v2 else False     

def jne(i,arg):
    try:
        # print("[jne] {}".format(i.flags["cmp"] == False))
        if i.flags["cmp"] == False:
            # print("JNE SUCCESS")
            call(i,arg)
            i.instruction_pointer -= 1
    except Exception as e:
        pass

def je(i,arg):
    try:
        if i.flags["cmp"]:
            call(i,arg[0])
    except Exception as e:
        pass

def loop(code,wv):
    i = Interpreter("",routine_name="OWL-PROCESS",wv=wv)
    i.code = VirtualFile(code)
    i.loadFunction("allocate",allocate)
    i.loadFunction("section",section)
    i.loadFunction("println",_println)
    i.loadFunction("callx",extern)
    i.loadFunction("clearm",clearm)
    i.loadFunction("start",start)
    i.loadFunction("print",_print)
    i.loadFunction("push",push)
    i.loadFunction("call",call)
    i.loadFunction("put",put)
    i.loadFunction("add",add)
    i.loadFunction("sub",sub)
    i.loadFunction("dec",dec)
    i.loadFunction("mov",mov)
    i.loadFunction("inc",inc)
    i.loadFunction("end",end)
    i.loadFunction("set",Set)
    i.loadFunction("jne",jne)
    i.loadFunction("ret",ret)
    i.loadFunction("cmp",_cmp)
    i.loadFunction("je",je)
    i.loadFunction("db",db)
    i.loop()