#@owldoc

'''@
This file contains Exception definitions that are used all over the system
@'''
from time import sleep
from sys import exit

class OWLException(Exception):
    '''
    OWLException:
        Base class for all OWL-OS exceptions
    '''

    def __init__(self,message,webview=None, fatal=False):
        func = "onFatalError" if fatal else "onError"
        if webview:
            webview.evaluate_js("window.OWL.%s(\"%s\");"%(func,message))
        print(message)
        if fatal:
            sleep(10)
            exit()

class OWLObjectInstanceException(OWLException):
    '''
    OWLObjectInstanceException:
        This is thrown when an object is initiated more than it's recommended amount
    '''
    def __init__(self,message,wv=None):
        super().__init__(message,webview=wv)
        self.__doc__ = '''
        OWLObjectInstanceException:
            This is thrown when an object is initiated more than it's recommended amount
        '''

class OWLPathError(OWLException):
    '''
    OWLPathError:
        This error is thrown when a path is invalid or protected
    '''
    def __init__(self,path,reason="Unreachable",wv=None):
        super().__init__("Path['%s'] is %s "%(path,reason),webview=wv)
        self.__doc__ = '''
        OWLPathError:
            This error is thrown when a path is invalid or protected
        '''

class OWLFileModeError(OWLException):
    '''
    OWLFileModeError:
        This error is thrown when a path is invalid or protected
    '''
    def __init__(self,mode,method,wv=None):
        super().__init__("Can't perform '%s', file is open in '%s' mode"%(method,mode),webview=wv)
        self.__doc__ = '''
        OWLFileModeError:
            This error is thrown when a path is invalid or protected
        '''