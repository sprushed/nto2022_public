from Crypto.Util.number import getPrime, getRandomNBitInteger, bytes_to_long
from sage.all import EllipticCurve, GF, gcd

flag = b"NTO{4_5m4ll_0v3rfl0w_h45_n07_hur7_4ny0n3_y37}"

lf = len(flag)
lh, rh = flag[:lf//2], flag[lf//2:]
nbit = max(len(lh), len(rh)) * 8
x = bytes_to_long(lh)
y = bytes_to_long(rh)

p = getPrime(nbit)
if not (x < p and y < p):
    continue
a = getRandomNBitInteger(nbit)
b = (y**2 - x**3 - a * x) % p
e = EllipticCurve(GF(p), [a, b])
g = e((x, y))
secret = getRandomNBitInteger(nbit//2 + 78)
d = gcd(secret, g.order())
print(d)
secret //= d
params =[p, a, b, g.order(), secret]
break

with open("params.py", "wt") as f:
    f.write("\n".join([f'flag = {flag}', f'params = {params}']))
