from mersenne import *
from binascii import hexlify,unhexlify
from os import urandom
import hashlib, hmac, os, sys, itertools, time

def main():
    secretkey = "3en"
    initV = urandom(len(secretkey))

    enc = encrypt(secretkey, initV)
    print ''.join(str(a) for a in enc)
    print ''.join(str(a) for a in decrypt(secretkey, initV, enc))
    eavesdrop(initV, enc)

if __name__ == "__main__":
    main()
