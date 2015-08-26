#!/usr/bin/python

# Add parent directory to path so we can import the library
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from hair import *
from PIL import Image
import sys

try:
    gif = Image.open(sys.argv[1])
    try:
        fps = sys.argv[2]
    except:
        fps = 10
except:
    print sys.argv[0] + " <file.gif>"

ih = Hair()
ih.FPS = fps

x = 0
while x < 95:
    g = ih.load_gif(image=gif,height=16)
    g.FPS=fps
    g.x = x
    ih.add(g)
    x += g[0].width


while True:
    ih.update()

