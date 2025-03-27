We are given a disk image that is encrypted using Bitlocker, a Windows feature that encrypts drives.

Searching online for bitlocker cracking tools, [I came across this repo called BitCracker](https://github.com/e-ago/bitcracker). I cloned the repo, built the project, but was unfortunately unable to get the OpenCL cracking built. I was however, able to get the bitcracker_hash module working, so I used that. 

I was able to get the User Password hash `$bitlocker$0$16$89a5bad722db4a729d3c7b9ee8e76a29$1048576$12$304a4ac192a2cf0103000000$60$24de9a6128e8f8ffb97ac72d21de40f63dbc44acf101e68ac0f7e52ecb1be4a8ee30ca1e69fbe98400707ba3977d5f09b14e388c885f312edc5c85c2`

Since one of the hints was "hash cracking", I used [hash_cat](https://hashcat.net/hashcat/) to brute force the passowrds. I downloaded a common passwords list file, rockyou.txt.

I ran `hashcat -m 22100 bitlocker_hash.txt rockyou.txt` (Mode 22100 is for bitlocker). After hashing for a while, it got the passowrd `jacqueline`

I used [Dislocker](https://github.com/Aorimn/dislocker) to decrypt the Windows drive, mounted it onto /mnt and was able to find the flag stored in a file.