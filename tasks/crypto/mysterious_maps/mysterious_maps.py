from itertools import permutations
from math import gcd

from Crypto.Util.number import bytes_to_long
from gmpy2 import mpz, next_prime

flag = b"********"


def number_of_mysterious_maps(n, k):
    identity = [_ for _ in range(n)]
    maps = permutations(identity)
    n = 0
    for m in maps:
        x = sum([1 if _ == m[_] else 0 for _ in range(len(m))])
        if x == k:
            n += 1
    return n


num = 100
k = 51

p = int(next_prime(mpz(number_of_mysterious_maps(num, k))))
q = int(next_prime(mpz(number_of_mysterious_maps(num, num - k))))
n = p * q

m = bytes_to_long(flag)

e = 0x10001

assert gcd(e, (p - 1) * (q - 1)) == 1
c = pow(m, e, n)

print(f"num, k, n, e, c = {num}, {k}, {n}, {e}, {c}")
