from os import urandom

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from secret import flag

key = urandom(16)
cipher = AES.new(key=key, mode=AES.MODE_ECB)

enc_flag = cipher.encrypt(pad(flag, 16))
print("I am very proud of my secure cipher. I will not give you any part of the flag.")
while True:
    option = input("Option: ")
    if option == "encrypt_flag":
        print(enc_flag.hex())

    elif option == "encrypt_message":
        message = input("Message: ")
        m = bytes.fromhex(message)
        if len(m) % 16 != 0:
            print("Invalid message length")
            continue

        c = cipher.encrypt(m)
        print(c.hex())

    elif option == "decrypt_message":
        c = input("Encrypted message: ")
        c = bytes.fromhex(c)
        if len(c) % 16 != 0:
            print("Invlid message length")
            continue

        m = cipher.decrypt(c)
        if c in enc_flag or m in flag:
            print("You shall not pass!")
            continue

        print(m.hex())
    else:
        print("Kept you waing huh?")
