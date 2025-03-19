I was originally discouraged by this question due to the difficulty of reversing the blockchain, but turns out, the flag is not hidden that well!

```py
if __name__ == "__main__":
    text = sys.argv[1]
    main(text)
```

It's calling the main function with the first argument, which likely is the flag.

```py
def main(token):
    key = bytes.fromhex(random_string)

    print("Key:", key)

    genesis_block = Block(0, "0", int(time.time()), "EncodedGenesisBlock", 0)
    blockchain = [genesis_block]

    for i in range(1, 5):
        encoded_transactions = base64.b64encode(
            f"Transaction_{i}".encode()).decode('utf-8')
        new_block = proof_of_work(blockchain[-1], encoded_transactions)
        blockchain.append(new_block)

    all_blocks = get_all_blocks(blockchain)

    blockchain_string = blockchain_to_string(all_blocks)
    encrypted_blockchain = encrypt(blockchain_string, token, key)

    print("Encrypted Blockchain:", encrypted_blockchain)
```

The actual block chain part we can ignore, since it doesn't use the `token` at all. In the final step, it converts the blockchain to a string and encrypts it using a key (that we are given) and the flag.

```py
def encrypt(plaintext, inner_txt, key):
    midpoint = len(plaintext) // 2

    first_part = plaintext[:midpoint]
    second_part = plaintext[midpoint:]
    modified_plaintext = first_part + inner_txt + second_part
    block_size = 16
    plaintext = pad(modified_plaintext, block_size)
    key_hash = hashlib.sha256(key).digest()

    ciphertext = b''

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        cipher_block = xor_bytes(block, key_hash)
        ciphertext += cipher_block

    return ciphertext
```

All the encrypt function does is inserts the flag, pads the blockchain, and then XOR encrypts it using the key's hash. 

We are given the key (so we can find key hash) and we are given the cipher text, so we can write a python script to reverse it for us.

```py
import hashlib

key = bytes.fromhex("1b72093b0fb59faad127af865bf0e6d92744f98d1767eb3e5f67472ed4c3dc83")
bc = b'o\x14>\xda\x16\xc7\xce\xd784,.\x8f2\x80@cD?\xd3L\x90\x9f\x87l0yy\xdam\x85J1\x139\x88\x10\x95\x9f\x82ke*.\xda>\xd3\x195O?\xd3\x10\xc4\x94\x83kd| \x882\x86IzFk\xd2@\x95\xcd\x83:by{\x8c3\x81\x1e6E8\xdaC\xc2\xcf\xd087||\x8em\xd0\x1c3Cj\xde\x10\xc0\x99\x89;4+{\x8fn\x84\x1abN9\xdc\x16\xc5\xc8\xd0mc}+\x81o\xd7J1[k\xda\x12\x94\xce\x89m3}(\xdbh\x84KeDh\x8fF\x9e\xc9\x84i1.*\x8f2\x87\x1d4\x15+\x83\x17\xc9\xef\xe5Iz*t\xd7h\xd9\'d%\t\x82"\xcf\xfe\xd3[09{\xe0T\xea-=;k\x98@\x9f\xcf\xf9Pp\x0bb\xd5A\xe8\x02\x15=\x04\x8eL\x96\x9f\x86n0ze\x89m\x81A6Bi\x88B\x91\xce\x8279q~\x8d:\x84OfAn\x8fA\x95\xc9\xd76d|}\x95;\x82@oFb\xddE\x93\x98\xd2jdz/\x88h\xd7\x1a6@o\xdd\x12\x94\x94\xd2m`}y\x8c>\x82LaCm\x8f\x10\x9f\x9f\xd3>0py\xde2\x87AoGh\x88\x11\x91\x9a\x84=3z*\xde&\x82Hb@n\xddM\xc3\xce\x89me.(\x808\xd0KaGo\x8bG\x91\x9b\x81?`.|\xde=\xd6@b\x17m\x8e\x11\x9f\x95\x80>d+.\x88>\x80\x1d4\x14m\xdd\x12\x96\xcf\x85m1q-\x8ao\xb0z'

print(bc.hex())
print(key.hex())

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def decrypt(ciphertext):
    key_hash = hashlib.sha256(key).digest()

    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        plain_block = xor_bytes(block, key_hash)
        plaintext += plain_block
    return plaintext

print(decrypt(bc))
```

It computes the key hash, loops through every 16-length block, decrypts it (by running XOR encrypt again)

```
b'8be0babf75d6792842d98636c11abf72febbd333ddb6b5aab9d9db82de480941-00843a25c1c483fa3c07dca764d6fbdd514df5845cc7e6b58b6bcdabb539de2f-00f2b8b250cc63223e28e5f0f2795eccpicoCTF{block}1f39a42b67b3889f5167175e53ef9e4e-0088097154cee270ceba647f28cba5a4504656ed93b118af959813be7652222f-0056579eb8bdf083b3614a37700afdf6d85a6de9911ec6052ecb67f0c4b0952d\x02\x02'
```

And the flag is right in the middle!
`picoCTF{block}`