The hint was that the flag is hidden in an image of the website, and the image was of a country that didn't exist. Using my mediocre geography skills, I googled "Upanzi Network" which seemed like the most suspicious country name. Turns out, it was some initiative by CMU in Africa. 

![Upanzi Network](aw.png)

I downloaded the image, and tried to analyze it using LSB tools, exiftool, etc. I wasn't able to get any meaningful result, and was a little discouraged. However, reading the title again, I realized it gives it all away. I searched up stepic and found [this Python command line tool](https://pypi.org/project/stepic/). Running that tool gave me the flag.