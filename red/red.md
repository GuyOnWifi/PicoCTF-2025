One of the hints was "Check whatever Facebook is called now" (Meta), so I immediately used exiftool to look at the metadata (data that describes the image). It's very common for information to be hidden in file metadata.

The metadata had an attribute, Poem:

```
Crimson heart, vibrant and bold,.Hearts flutter at your sight..Evenings glow softly red,.Cherries burst with sweet life..Kisses linger with your warmth..Love deep as merlot..Scarlet leaves falling softly,.Bold in every stroke.
```

The first letters of each line spell out `CHECKLSB`, giving us a hint that the image was likely using LSB stenography, where information is hidden in the last bits of the pixel values. Using a simple Python script I stole online, I was able to decode it. I originally got a bit suck because I didn't realize I had to use all 4 channels (including the alpha/transparency channel!)

```py
from PIL import Image

image = Image.open("red.png")
image = image.convert("RGBA")

width, height = image.size

file = open("out.txt", "w")

for y in range(height):
    for x in range(width):
        channel = image.getpixel((x, y))
        print(channel[0] & 1, end="", file=file)
        print(channel[1] & 1, end="", file=file)
        print(channel[2] & 1, end="", file=file)
        print(channel[3] & 1, end="", file=file)
```

Converting the output binary to ASCII, we get repetitions of `cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==`. which looks like base64. Running it through base64 decode, we get `picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}`