from Crypto.Util.number import getPrime, bytes_to_long, getRandomNBitInteger

flag = b"********"


def gen_params(nbit):
    p = getPrime(nbit)
    q = pow(getRandomNBitInteger(nbit), p - 1, p)
    return p, q


p, q = gen_params(1024)
n = p * q
m = bytes_to_long(flag)
e = 0x10001

c = pow(m, e, n)
print(f"c, e, n = {c}, {e}, {n}")
