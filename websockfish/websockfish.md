The first thing I did was open up Developer tools, and look at the network requests it was sending. It was opening up a websocket, which caught my eye, and I played a couple of moves to inspect it more closely.

![Wow](image.png)

Seems like all of the move validation is happening client-side and the score is being sent to the server. A positive score seemed to mean that the bot was winning, so I assumed a negative score would imply that I was winning.

I read the description where I had to beat the bot "covincingly, so I made sure the evaluation became slightly and slightly more negative, before sending the "mate -1", which I assumed to signal that I won. My exploit didn't, and the bot just kept saying something about never being able to break it's spirit.

I was stuck on this for a while, until I decided to mess around with the numbers. I changed the max negative score to be -99999 (which I thought was a totatly unreasonable eval), and it gave me the flag!

```
Huh???? How can I be losing this badly... I resign... here's your flag: picoCTF{c1i3nt_s1d3_w3b_s0ck3t5}
```

Seems like you just had to send it a really bad eval and it would work...