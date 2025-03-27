We are given a disk image that is encrypted using Bitlocker, a Windows feature that encrypts drives.

Searching online for bitlocker cracking tools, [I came across this repo called BitCracker](https://github.com/e-ago/bitcracker). I cloned the repo, built the project, but was unfortunately unable to get the OpenCL cracking built. I was however, able to get the bitcracker_hash module working, so I used that. 

I was able to get the User Password hash `$bitlocker$0$16$cb4809fe9628471a411f8380e0f668db$1048576$12$d04d9c58eed6da010a000000$60$68156e51e53f0a01c076a32ba2b2999afffce8530fbe5d84b4c19ac71f6c79375b87d40c2d871ed2b7b5559d71ba31b6779c6f41412fd6869442d66d`

Since one of the hints was "hash cracking", I used [hash_cat](https://hashcat.net/hashcat/) to brute force the passowrds. I downloaded a common passwords list file, rockyou.txt.

I ran `hashcat -m 22100 bitlocker_hash.txt rockyou.txt` (Mode 22100 is for bitlocker). After hashing for a while, it got the passowrd `jacqueline`

I used [Dislocker](https://github.com/Aorimn/dislocker) to decrypt the Windows drive, mounted it onto /mnt and was able to find the flag stored in a file: `picoCTF{us3_b3tt3r_p4ssw0rd5_pl5!}`