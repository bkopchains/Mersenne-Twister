import hashlib, hmac, binascii, os, sys, itertools

f = open(str(sys.argv[1]), 'r')

method = int(f.readline().strip())
PWHint = f.readline().strip()
salt = f.readline().strip()
salt = binascii.unhexlify(salt)
#print "SALT TYPE:     " + salt + str(type(salt))
hashPass = binascii.unhexlify(f.readline().strip().encode())
#print(hashPass)
f.close()

chars = []
for x in range(32, 127):
    chars.append(chr(x))

def main():
    if method == 1:
        brute()
    elif method == 2:
        dict()
    elif method == 3:
        bruteP()
    else:
        print("invalid method")

def brute():

    result = False
    out = ''
    x = 0
    while(not result):
        for item in itertools.product(chars, repeat = x):
            password = ''.join(item)
            print password
            hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            result = hmac.compare_digest(hash,hashPass)
            if result:
                print('password found')
                out = password
                break
        x += 1


def dict():

    dict = open('/usr/share/dict/words')
    result = False
    out = ''
    x = 0
    while(not result):
        for item in dict:
            password = item.strip()
            print password
            hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            result = hmac.compare_digest(hash,hashPass)
            if result:
                print('password found')
                out = password
                break
        x += 1

def bruteP():

    hintArr = []
    locations = []
    for char in PWHint:
        hintArr.append(char)
        if char == "*":
            locations.append(len(hintArr)-1)

    for item in itertools.product(chars, repeat = len(locations)):
        rands = ''.join(item)
        for i in range(0,len(locations)):
            hintArr[locations[i]] = rands[i]
        password = ''.join(hintArr)
        print password
        hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        result = hmac.compare_digest(hash,hashPass)
        if result:
            print('password found')
            out = password
            break

main()
