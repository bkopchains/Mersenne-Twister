#mersenne.py
from binascii import hexlify,unhexlify
from os import urandom
import hashlib, hmac, os, sys, itertools, time

#global vars
N = 624
M = 397
A = 0x9908b0df
UPPER = 0x80000000
LOWER = 0x7fffffff
m = list(range(0,N))
mi = N

chars = []
for x in range(32, 127):
    chars.append(chr(x))

#setSeed function
def setSeed(seed):
    global mi
    m[0] = seed & 0x7fffffff
    for i in range(1,len(m)):
        m[i] = (69069 * m[i-1]) & 0xffffffff
    mi = N

#nextInt function
def nextInt():
    global mi
    if mi >= N:
        for k in range(0,N-1):
            y = (m[k] & UPPER) | (m[(k+1) % N] & LOWER)
            m[k] = m[(k+M) % N] ^ (y >> 1)
            if y % 2 != 0:
                m[k] = m[k] ^ A
        mi = 0
    y = m[mi]
    mi += 1
    y = y ^ (y >> 11)
    y = y ^ ((y << 7) & 0x9d2c5680)
    y = y ^ ((y << 15) & 0xefc60000)
    y = y ^ (y >> 18)
    return y

def encrypt(secret, initV):

    secret = int(hexlify(secret),16)
    initV = int(hexlify(initV),16)
    seed = secret^initV
    #print "Eseed: ", seed

    cipherText = []
    message = raw_input("Enter your message: ")
    setSeed(seed)
    for char in message:
        char = int(hexlify(char),16)
        newint = nextInt()
        #print char, newint, char^newint
        cipherText.append(char^newint)
    return cipherText

def decrypt(secret, initV, cipherText):

    secret = int(hexlify(secret),16)
    initV = int(hexlify(initV),16)
    seed = secret^initV
    #print "Dseed: ", seed

    newCipherText = []
    setSeed(seed)
    for char in cipherText:
        newint = nextInt()
        #print char, newint, char^newint
        char = (char^newint)
        newCipherText.append(unhexlify(format(char, '02x')))
    return newCipherText

#ascii helper function
def is_ascii(list):
    return all(ord(item) < 128 for item in list)

def eavesdrop(initV, cipherText):

    dict = open('/usr/share/dict/words', 'r')
    result = False
    x = 1
    att = 1
    start_time = time.time()
    while(x < 40 and result == False):
        for item in itertools.product(chars, repeat = x):
            password = ''.join(item)

            try:
                decrypted = decrypt(password, initV, cipherText)
                print password + " --- attempt no: " + str(att)
                if is_ascii(decrypted):
                    out = ''.join(decrypted)
                    out2 = out.split(" ")

                    bool = True
                    for i in out2:
                        if i not in dict:
                            bool == False
                    if bool == True:
                        elapsed_time = time.time() - start_time
                        print "possible message found: ", out
                        print "message found in", elapsed_time, "seconds and", att, "attempts"

                        result = True
                        break

            except TypeError:
                print("TypeError, skipping attempt no " + str(att) + "(" + password + ")")
            # decrypted = ''.join(decrypt).strip().split(" ")

            att += 1
        x += 1
