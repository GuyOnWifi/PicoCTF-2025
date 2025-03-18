from hashlib import sha256

with open("cheese_list.txt") as f:
    for l in f.readlines():
        l = l.strip()
        # salts
        for i in range(256):
            for j in range(len(l) + 1):
                text = l[:j] + hex(i)[2:] + l[j:]
                text = text.encode()
                hash = sha256(text).hexdigest()
                if hash == "a19e2cc2f29e4c3d988c4cf8622bfd07d4c6944db5d132396b54c32ec3b96c1a":
                    print(l)
                    exit(0)
print("none found bruh")
                
                    
                                


#bruh i give up