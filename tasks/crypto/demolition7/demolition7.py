from Crypto.Util.number import getPrime, bytes_to_long

flag = b"*******"


def hint(p: int, q: int):
    phi = (p - 1) * (q - 1)
    e = getPrime(17)
    d = pow(e, -1, phi)
    print(d)
    return e, d // 256**2


p = getPrime(1024)
q = getPrime(1024)
n = p * q

eh, dh = hint(p, q)
print(f"eh, dh = {eh}, {dh}")

e = 2**16 + 1
m = bytes_to_long(flag)
c = pow(m, e, n)
print(f"n, e, c = {n}, {e}, {c}")
