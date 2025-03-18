from hashlib import sha256

# Open the file and read line by line
with open("cheese_list.txt") as f:
    for l in f.readlines():
        l = l.strip()  # Remove any extra whitespace or newline characters
        
        # Iterate over all possible salt values (0 to 255)
        for i in range(256):
            # Extract the two nibbles of salt
            first_nibble = i >> 4  # Get the first nibble (most significant 4 bits)
            second_nibble = i & 0x0F  # Get the second nibble (least significant 4 bits)
            
            # Try inserting the two nibbles at different positions
            for j in range(len(l) + 1):  # Position for the first nibble
                for k in range(len(l) + 1):  # Position for the second nibble
                    if j == k:  # Don't insert both nibbles at the same position
                        continue
                    
                    # Create the salted text by splitting at positions j and k
                    text = l[:j].encode() + bytes([first_nibble]) + l[j:k].encode() + bytes([second_nibble]) + l[k:].encode()
                    print(text)
                    # Calculate the SHA-256 hash
                    hash = sha256(text).hexdigest()
                    
                    # Check if the hash matches the target hash
                    if hash == "a19e2cc2f29e4c3d988c4cf8622bfd07d4c6944db5d132396b54c32ec3b96c1a":
                        print(f"Match found: {l}")
                        exit(0)  # Exit after finding the match

# If no match was found, print this message
print("No match found.")
