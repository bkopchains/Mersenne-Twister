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

#sets up list of all ascii letters
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

#nextInt function for stepping through the stream
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

#encrypt function takes in a key and initialization vector
# -> uses the XOR function to encrypt a chosen message
def encrypt(secret, initV):

    secret = int(hexlify(secret),16)
    initV = int(hexlify(initV),16)
    seed = secret^initV

    cipherText = []
    message = raw_input("Enter your message: ")
    setSeed(seed)
    for char in message:
        char = int(hexlify(char),16)
        newint = nextInt()
        cipherText.append(char^newint)
    return cipherText

#decrypt function takes in a key, initialization vector, and the resulting
#ciphertext list from the encrypt function
#-> uses the XOR function to decrypt a cyphertext given by the encrypt function
def decrypt(secret, initV, cipherText):

    secret = int(hexlify(secret),16)
    initV = int(hexlify(initV),16)
    seed = secret^initV

    newCipherText = []
    setSeed(seed)
    for char in cipherText:
        newint = nextInt()
        char = (char^newint)
        newCipherText.append(unhexlify(format(char, '02x')))
    return newCipherText

#ascii helper function (looked online for how to write this)
def is_ascii(list):
    return all(ord(item) < 128 for item in list)

#given an intialization vector and a ciphertext, brute forces possible secret
#keys until it finds a possible decrypted english message
def eavesdrop(initV, cipherText):

    dict = open('/usr/share/dict/words', 'r')
    result = False
    x = 1
    att = 1
    start_time = time.time()
    while(x < 40 and result == False):
        for item in itertools.product(chars, repeat = x):
            password = ''.join(item)

            #my method caused some incorrect guesses to return errors, so
            #I needed to format the function like this (try/except)
            try:
                decrypted = decrypt(password, initV, cipherText)
                print password + " --- attempt no: " + str(att)
                #checks if the decrypted message is made up of ascii letters
                if is_ascii(decrypted):
                    out = ''.join(decrypted)
                    out2 = out.split(" ")

                    #checks if the concatenated letters make up english words
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
                print("Bad guess / TypeError, skipping attempt no " + str(att) + "(" + password + ")")

            att += 1
        x += 1
