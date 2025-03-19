We need to guess a randomly generated token to get the flag. Fortunately for us, it seems like the get_random function uses a seed. A seed is a number used to initialize a random number generator, and the same seed will produce the same random number. 
```py
def get_random(length):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(int(time.time() * 1000))  # seeding with current time 
    s = ""
    for i in range(length):
        s += random.choice(alphabet)
    return s
```

The seed is also really predictable, because it is the current time in seconds. We can easily run a script that brute forces this and hopefully it is fast enough to guess the right random.

```py
from pwnlib.tubes.remote import *
import random 
import time

def get_random(length):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(int(time.time() * 1000))  # seeding with current time 
    s = ""
    for i in range(length):
        s += random.choice(alphabet)
    return s

conn = remote("verbal-sleep.picoctf.net", 50104)
print(conn.recvline())
print(conn.recvline())
print(conn.recvline())

for i in range(50):
    conn.sendline(get_random(20))
    print(conn.recvline())
```