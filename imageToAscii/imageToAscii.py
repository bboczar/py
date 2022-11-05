import argparse
import os
from math import floor
from PIL import Image

# Variables
ascii_scale = " .:-=+*#%@"
ascii_max = len(ascii_scale)
rgb_max = 255

class Config:
    pass

parser = argparse.ArgumentParser(description='Image to ASCII converter')

# Methods

def setup_parser(parser):
    parser.add_argument('-f', type=str, default='photo.png', help='File to convert')
    parser.add_argument('-s', type=int, default='25', help='Downscale of ascii image')
    parser.add_argument('-r', type=int, default=0, help='Rotation by angle (deg)')
    parser.add_argument('-i', action='store_true', help='Inverse ascii scale')

setup_parser(parser)
config = Config()
args = parser.parse_args(namespace=config)

try:
    image = Image.open(config.f)
except Exception as e:
    print("Could not open ", config.f)
    sys.exit()

# Scale according to config
width, height = image.size
scale = 1 / config.s
image = image.resize((floor(width * scale), floor(height * scale / 2)))

# ASCII scale inversion
if (config.i):
    ascii_scale = ascii_scale[::-1]

# Rotation according to config
image = image.rotate(config.r)

# New image dimensions
width, height = image.size

f = open("ascii.txt", "w")

for i in range(height):
    ascii_list = []
    for j in range(width):
        r, g, b = image.getpixel((j, i))
        gray = 0.299*r + 0.587*g + 0.114*b
        ascii_idx = floor(ascii_max * gray / rgb_max)
        if (ascii_idx > ascii_max - 1):
            ascii_idx = ascii_max - 1
        ascii = ascii_scale[ascii_idx]
        ascii_list.append(ascii)
    f.write("".join(ascii_list) + "\n")
f.close()