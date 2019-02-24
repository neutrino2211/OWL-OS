# ./libraries/gecko_byte_code.py
This is the gecko mini code interpreter
## Supported operations
__allocate__ -> `allocate ..args`
__section__ -> `section ..args`
___println__ -> `println`
__extern__ -> `callx ..args`
__clearm__ -> `clearm ..args`
__start__ -> `start ..args`
__print__ -> `_print`
__push__ -> `push ..args`
__call__ -> `call ..args`
__put__ -> `put ..args`
__add__ -> `add ..args`
__sub__ -> `sub ..args`
__dec__ -> `dec ..args`
__mov__ -> `mov ..args`
__inc__ -> `inc ..args`
__end__ -> `end ..args`
__Set__ -> `set ..args`
__jne__ -> `jne ..args`
__ret__ -> `ret ..args`
___cmp__ -> `cmp`
__je__ -> `je`
__db__ -> `db`
-----------------------------
# Variables
`VirtualFile.code` instructions to convert
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
# Functions
## VirtualFile.__init__
store the instructions to convert
## VirtualFile.read
Return the instructions
## VirtualFile.readlines
Return the instructions as a list of line-by-line instructions
## Interpreter.__init__
create the spaces for functions,instruction line, webview
`Interpreter.loop`
Go through every instruction and execute it
`Interpreter.breakStatement`
Convert a line of code into `operation` `..args`
`Interpreter.execute`
Run function assigned to the opcode with the arguments
`Interpreter.loadFunction`
Assign a python function to an opcode
`Interpreter.convertInt`
Convert string representaion of number to int
`Interpreter.resolveValue`
resolve various representations of values
`Interpreter.isDefinedSpace`
Check if array is supposed to have a size limit
# Classes
## VirtualFile
This is an interface for the interpreter to treat lines of instructions as a file
## Interpreter
Executes the mini code