import onetimepad
from os import path

class OWLCrypto(object):
    __key = None
    def __init__(self,key):
        init = True
        self.__key = key
        try:
            with open("config/crypto","w") as tf:
                tf.write("")
        except Exception as e:
            print(e)
            path.sys.exit(0)

    
    def encrypt(self,m):
        return onetimepad.encrypt(m,self.__key.decode("ISO-8859-5"))

    def decrypt(self,m):
        return onetimepad.decrypt(m,self.__key.decode("ISO-8859-5"))

    def restore_key(self):
        with open("config/crypto","wb") as f:
            f.write(self.__key)