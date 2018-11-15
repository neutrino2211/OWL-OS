#@owldoc

'''@
This is the gecko mini code interpreter
@'''

import sys
'''@
:class ## VirtualFile
This is an interface for the interpreter to treat lines of instructions as a file
@'''
class VirtualFile:
    '''@
    :function 
    ## VirtualFile.__init__
    store the instructions to convert
    @'''
    '''@
    :variable `VirtualFile.code` instructions to convert
    @'''
    def __init__(self,code):
        self.code = code
    '''@
    :function 
    ## VirtualFile.read
    Return the instructions
    @'''
    def read(self):
        return self.code
    '''@
    :function 
    ## VirtualFile.readlines
    Return the instructions as a list of line-by-line instructions
    @'''
    def readlines(self):
        return self.code.split("\n")
'''@
:class ## Interpreter
Executes the mini code
@'''
class Interpreter:
    '''@
    :function ## Interpreter.__init__
    create the spaces for functions,instruction line, webview
    @'''
    '''@
    :variable 
    `Interpreter.code`: File-like object containing the source code

    `Interpreter.wv`: The pywebview instance

    `Interpreter.name`: Routine name for logging purposes

    `Interpreter.maxm`: Number of 'registers' used to contain temporary values

    `Interpreter.line`: Used to when logging errors

    `Interpreter.memory`: Python list serving as an array of 'registers' to store values

    `Interpreter.flags`: Python dict to store runtime flags like errors,cmp results e.t.c

    `Interpreter.variables`: Values declared by `db`

    `Interpreter.functions`: dict of name to operation

    `Interpreter.subroutine`: `bool` that signifies the state of the interpreter. 
    Used to know when to skip subroutines and define them instead of running them

    `Interpreter.subroutines`: `dict` of name to subroutine code

    `Interpreter.memory_spaces`: `dict` of name to list used for when data is too large for the 'registers'

    `Interpreter.return_pointer`: Used by `jne` `je` `cmp` and more to change the
    instruction pointer after an operation is complete

    `Interpreter.subroutinecode`: Used to store subroutine instructions when __Interpreter.subroutine__ is False

    `Interpreter.instrunction_pointer`: Used to know which instruction is to be executed next
    @'''
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
    '''@
    :function `Interpreter.loop`
    Go through every instruction and execute it
    @'''
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

    '''@
    :function `Interpreter.breakStatement`
    Convert a line of code into `operation` `..args`
    @'''
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

    '''@
    :function `Interpreter.execute`
    Run function assigned to the opcode with the arguments
    @'''
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


    '''@
    :function `Interpreter.loadFunction`
    Assign a python function to an opcode
    @'''
    def loadFunction(self,name,f):
        self.functions[name] = f
        # pass

    '''@
    :function `Interpreter.convertInt`
    Convert string representaion of number to int
    @'''
    def convertInt(self,i):
        r = 0
        try:
            r = int(i,10)
        except Exception as e:
            r = int(1,16)
        return r

    '''@
    :function `Interpreter.resolveValue`
    resolve various representations of values
    @'''
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

    '''@
    :function `Interpreter.isDefinedSpace`
    Check if array is supposed to have a size limit
    @'''
    def isDefinedSpace(self,v):
        # print(v)
        if len(v) == 0:
            return False
        for val in v:
            if val != 0:
                return False
        return True

'''@
## Supported operations
@'''

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
    i.loadFunction("allocate",allocate) '''@__allocate__ -> `allocate ..args`@'''
    i.loadFunction("section",section) '''@__section__ -> `section ..args`@'''
    i.loadFunction("println",_println) '''@___println__ -> `println`@'''
    i.loadFunction("callx",extern) '''@__extern__ -> `callx ..args`@'''
    i.loadFunction("clearm",clearm) '''@__clearm__ -> `clearm ..args`@'''
    i.loadFunction("start",start) '''@__start__ -> `start ..args`@'''
    i.loadFunction("print",_print) '''@__print__ -> `_print`@'''
    i.loadFunction("push",push) '''@__push__ -> `push ..args`@'''
    i.loadFunction("call",call) '''@__call__ -> `call ..args`@'''
    i.loadFunction("put",put) '''@__put__ -> `put ..args`@'''
    i.loadFunction("add",add) '''@__add__ -> `add ..args`@'''
    i.loadFunction("sub",sub) '''@__sub__ -> `sub ..args`@'''
    i.loadFunction("dec",dec) '''@__dec__ -> `dec ..args`@'''
    i.loadFunction("mov",mov) '''@__mov__ -> `mov ..args`@'''
    i.loadFunction("inc",inc) '''@__inc__ -> `inc ..args`@'''
    i.loadFunction("end",end) '''@__end__ -> `end ..args`@'''
    i.loadFunction("set",Set) '''@__Set__ -> `set ..args`@'''
    i.loadFunction("jne",jne) '''@__jne__ -> `jne ..args`@'''
    i.loadFunction("ret",ret) '''@__ret__ -> `ret ..args`@'''
    i.loadFunction("cmp",_cmp) '''@___cmp__ -> `cmp`@'''
    i.loadFunction("je",je) '''@__je__ -> `je`@'''
    i.loadFunction("db",db) '''@__db__ -> `db`@'''
    i.loop()