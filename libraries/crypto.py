from Crypto.Cipher import AES
from .errors import OWLObjectInstanceException
from os import path

init = False

class OWLCrypto(object):
    __key = None
    __cry = None
    def __init__(self,key):
        global init
        with open("config/crypto","w") as tf:
            tf.write("")
        if init:
            raise OWLObjectInstanceException("OWLCrypto should have only one instance")
        init = True
        self.__key = key
        self.__cry = AES.new(self.__key)

    
    def encrypt(self,m):
        return self.__cry.encrypt(m)

    def decrypt(self,m):
        return self.__cry.decrypt(m)

    def restore_key(self):
        with open("config/crypto","wb") as f:
            f.write(self.__key)