from Crypto.Cipher import AES
from os import path

class OWLCrypto(object):
    __key = None
    __cry = None
    def __init__(self,key):
        with open("config/crypto","w") as tf:
            tf.write("")
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