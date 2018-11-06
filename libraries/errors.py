class OWLObjectInstanceException(Exception):
    '''
    OWLObjectInstanceException:
        This is thrown when an object is initiated more than it's recommended amount
    '''
    def __init__(self,message):
        super().__init__(message)
        self.__doc__ = '''
        OWLObjectInstanceException:
            This is thrown when an object is initiated more than it's recommended amount
        '''

class OWLPathError(Exception):
    '''
    OWLPathError:
        This error is thrown when a path is invalid or protected
    '''
    def __init__(self,path,reason="Unreachable"):
        super().__init__("Path['%s'] is %s "%(path,reason))
        self.__doc__ = '''
        OWLPathError:
            This error is thrown when a path is invalid or protected
        '''

class OWLFileModeError(Exception):
    '''
    OWLPathError:
        This error is thrown when a path is invalid or protected
    '''
    def __init__(self,mode,method):
        super().__init__("Can't perform '%s', file is open in '%s' mode"%(method,mode))
        self.__doc__ = '''
        OWLPathError:
            This error is thrown when a path is invalid or protected
        '''