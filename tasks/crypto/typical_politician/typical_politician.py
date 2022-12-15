from Crypto.Util.number import getPrime, bytes_to_long

flag = b"********"


def hint(p, q, n):
    return (
        pow(p + q, q, n),
        pow(p + q, p, n),
        pow(p + q, p + q, n),
        pow(p + q, p * q, n),
    )


p, q = getPrime(1024), getPrime(1024)
n = p * q
e = 0x10001
m = bytes_to_long(flag)

h1, h2, h3, h4 = hint(p, q, n)
print(f"{h1, h2, h3, h4 = }")

c = pow(m, e, n)
print(f"{c, e, n = }")
