# ./install.py
This file is used to setup crucial aspects of the virtual operating system
e.g Crypto
-----------------------------
# Variables
`InstallTask.name`: Task name used during logging to keep track of currently executing tasks
`InstallTask.args`: Arguments passed via the command line (in dict form)
# Functions
## InstallTask.__init__
Store task name and arguments
## InstallTask.confirm_path
Utility function for all tasks to use when trying to confirm a file exists outside the sandbox
## InstallTask.get_arg
Utility function that type checks and returns arguments for all tasks to use when retrieving an argument
## InstallTask._run
Entry point wrapper for all tasks
## InstallTask.log
Utility function that logs task message and name for easy debugging
## arguments
Converts sys.argv into a dict of arguments to value of the format `--<option>=<value>`
## sxor
Rudimentry imlementation of xor-ing strings
## run_tasks
Run tasks given as arguments
## main
Entry point for install procedure
# Classes
## InstallTask
Wrapper for all operations to be performed when installing the system
## CryptoTask(InstallTask)
Task to setup crypto values e.g key
## FSTask(InstallTask)
Task to setup filesystem