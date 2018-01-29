import hashlib, binascii, os

f = open("test_pass.txt","w")

password = "Clifford"
salt = os.urandom(16)

hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

f.write("2\n")
f.write("Cliff*rd\n")
f.write(binascii.hexlify(salt).decode() + "\n")
f.write(binascii.hexlify(hash).decode() + "\n")

print(binascii.unhexlify(binascii.hexlify(salt).decode()))
