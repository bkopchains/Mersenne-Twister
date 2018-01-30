from mersenne import *
from binascii import hexlify,unhexlify
from os import urandom
import hashlib, hmac, os, sys, itertools, time

def main():
    secretkey = "3en"
    initV = urandom(len(secretkey))

    enc = encrypt(secretkey, initV)
    print "Encrypted message:"
    print ''.join(str(a) for a in enc), "\n"

    print "Decrypted message:"
    print ''.join(str(a) for a in decrypt(secretkey, initV, enc)), "\n"

    raw_input("Press enter to run eavesdrop function")

    eavesdrop(initV, enc)

if __name__ == "__main__":
    main()
