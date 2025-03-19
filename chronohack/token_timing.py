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
    conn.send(get_random(20))
    print(conn.recvline())

