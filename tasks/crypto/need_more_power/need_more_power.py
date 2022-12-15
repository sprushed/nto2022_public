from Crypto.Util.number import bytes_to_long
from fastecdsa.curve import Curve
from fastecdsa.point import Point

from params import flag, params
from random import choice

lf = len(flag)
lh, rh = flag[: lf // 2], flag[lf // 2 :]
nbit = max(len(lh), len(rh)) * 8

x = bytes_to_long(lh)
y = bytes_to_long(rh)

p, a, b, q, secret = params

ecurve = Curve(name="AAAAAAAAAAAAAAAAAAA", p=p, a=a, b=b, q=q, gx=x, gy=y)
flag = Point(x, y, curve=ecurve)
g = flag * secret

print(f"a, b, p, x, y = {a}, {b}, {p}, {g.x}, {g.y}")

scalar = int(input("Scalar: "))

if scalar <= 1:
    print("I need more POWER")
    exit()

if scalar.bit_length() < nbit // 2:
    print("Where's your MOTIVATION?")
    exit()

if scalar * flag == g:
    print("Fortunately, our souls are at evens, brother!")
elif scalar < secret:
    print("I've come to retrieve my power. You can't handle it.")
else:
    print("You've come to retrieve your power. You can't handle it.")
