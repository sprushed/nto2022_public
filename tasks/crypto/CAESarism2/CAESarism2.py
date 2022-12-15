from os import urandom

from Crypto.Cipher import AES

from secret import flag

key = urandom(16)
IV = urandom(16)
flag = b"As long as I'm breathing no one will know the contents of this flag: " + flag

lf = len(flag)
lp = 16 - (len(flag) % 16)
flag += b" " * lp
cipher = AES.new(key=key, iv=IV, mode=AES.MODE_CBC)
enc_flag = cipher.encrypt(flag)

cipher = AES.new(key=key, iv=IV, mode=AES.MODE_CBC)

while True:
    option = input("Option: ")

    if option == "encrypt_flag":
        print(hex(lf)[2:].zfill(2) + enc_flag.hex())

    elif option == "encrypt_message":
        message = input("Message: ")
        m = bytes.fromhex(message)
        pad = 16 - (len(m) % 16)
        m += b" " * pad
        c = cipher.encrypt(m)
        print(c.hex())

    elif option == "check":
        message = input("Message: ")
        mlen = int(message[:2], 16)
        message = message[2:]

        message = bytes.fromhex(message)
        if len(message) % 16 != 0:
            print("Invalid message len")
            continue

        c = cipher.decrypt(message)
        c = c.rstrip(b" ")

        if len(c) != mlen:
            print("You won't fool me :)")
            continue

        print(
            "Someone who smiles too much with you can sometime frown too much with you at your back"
        )
    else:
        print("Private Joker, I don't believe I heard you correctly!")
