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
