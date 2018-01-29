#mersenne.py

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

    cipherText = ""

    return cipherText
