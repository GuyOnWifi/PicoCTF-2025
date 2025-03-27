Same thing as Bitlocker 1, we have a Bitlocker encrypted drive. Unfortunately, it seems that Jacky has used a better password this time, which makes hash cracking unfeasible. However, we have a RAM dump that we can analyze using tools online.

I found [this Volatility2 Plugin](https://github.com/breppo/Volatility-BitLocker) that is able to analyze a memory dump and dump potential Bitlocker keys. I had to install Python 2 and [the Volatility2 Framework](https://github.com/volatilityfoundation/volatility). After moving the Bitlocker plugin into the plugins folder, and running it, I was able to get a dump of all potential keys.

```
Volatility Foundation Volatility Framework 2.6.1

[FVEK] Address : 0x8087865bead0
[FVEK] Cipher  : AES-XTS 128 bit (Win 10+)
[FVEK] FVEK: 4f79d4a00d5e9b25965b89581a6a599c
[DISL] FVEK for Dislocker dumped to file: ./dislocker/0x8087865bead0-Dislocker.fvek



[FVEK] Address : 0x40d857c90
[FVEK] Cipher  : AES 128-bit (Win 8+)
[FVEK] FVEK: d40582190eb6f067691120bbbe55e511
[DISL] FVEK for Dislocker dumped to file: ./dislocker/0x40d857c90-Dislocker.fvek
```

Trying the first one with Dislocker decrypted the drive, and I was able to extract the flag.