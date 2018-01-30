#mersenne.py
from binascii import hexlify,unhexlify
from os import urandom

#global vars
N = 624
M = 397
A = 0x9908b0df
UPPER = 0x80000000
LOWER = 0x7fffffff
m = list(range(0,N))
mi = N

#setSeed function
def setSeed(seed):
    global mi
    m[0] = seed & 0x7fffffff
    for i in range(1,len(m)):
        m[i] = (69069 * m[i-1]) & 0xffffffff
    mi = N

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

def eavesdrop(initV, cipherText):
    t = 1

def demo(secret, initV):
    secret = int(hexlify(secret),16)
    initV = int(hexlify(initV),16)
    seed = secret^initV


def xorS(s1,s2):
    return ''.join(chr(ord(a)^ord(b)) for a,b in zip(s1,s2))

secretkey = "secretkey"
initV = urandom(len(secretkey))

enc = encrypt(secretkey, initV)
print enc
print decrypt(secret, initV, enc)
