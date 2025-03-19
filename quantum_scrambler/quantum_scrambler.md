This one was fairly simple, and didn't even require any knowledge of how the Python code actually works. 

Going off of the hint, I passed in the sample string "testing". It's hex representation (returned by get_flag) is 
`[['0x74'], ['0x65'], ['0x73'], ['0x74'], ['0x69'], ['0x6e'], ['0x67']]`
and the returned result was 
`[['0x74', '0x65'], ['0x73', [], '0x74'], ['0x69', [['0x74', '0x65']], '0x6e'], ['0x67', [['0x74', '0x65'], ['0x73', [], '0x74']]]]`

It seems like I just need to take the first and last values of each list, and only process them if they are a hex value and not another list. I wrote a quick implementation.

```py
l = eval("<encoded>")

for x in l:
    if isinstance(x[0], str):
        print(chr(int(x[0], 16)), end="")
    if isinstance(x[-1], str):
        print(chr(int(x[-1], 16)), end="")
```

And it prints the flag! `picoCTF{python_is_weird}}`. With an extra curly brace for some reason, but it works!