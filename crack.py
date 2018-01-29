import hashlib, hmac, binascii, os, sys, itertools, time

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

#brute force method - guesses every posisble password
def brute():

    result = False
    x = 0
    att = 1
    start_time = time.time()
    while(not result):
        for item in itertools.product(chars, repeat = x):
            password = ''.join(item)
            print password + " --- attempt no: " + str(att)
            att += 1
            hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            result = hmac.compare_digest(hash,hashPass)
            if result:
                elapsed_time = time.time() - start_time
                print('password found in %s seconds and %d attempts' % (str(elapsed_time),att-1))
                break
        x += 1

#dictionary method - guesses passwords from a list
def dict():

    dict = open('/usr/share/dict/words')
    result = False
    x = 0
    att = 1
    start_time = time.time()
    while(not result):
        for item in dict:
            password = item.strip()
            print password + " --- attempt no: " + str(att)
            att += 1
            try:
                password.encode('ascii')
            except UnicodeDecodeError:
                print("^skipped non-ascii word")
            else:
                hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
                result = hmac.compare_digest(hash,hashPass)
                if result:
                    elapsed_time = time.time() - start_time
                    print('password found in %s seconds and %d attempts' % (str(elapsed_time),att-1))
                    break
        x += 1

#brute force with prior knowledge - guesses every possible password given knowledge
# of existing letters
def bruteP():

    hintArr = []
    locations = []
    att = 1
    start_time = time.time()
    for char in PWHint:
        hintArr.append(char)
        if char == "*":
            locations.append(len(hintArr)-1)

    for item in itertools.product(chars, repeat = len(locations)):
        rands = ''.join(item)
        for i in range(0,len(locations)):
            hintArr[locations[i]] = rands[i]
        password = ''.join(hintArr)
        print password + " --- attempt no: " + str(att)
        att += 1
        hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        result = hmac.compare_digest(hash,hashPass)
        if result:
            elapsed_time = time.time() - start_time
            print('password found in %s seconds and %d attempts' % (str(elapsed_time),att-1))
            break

main()
