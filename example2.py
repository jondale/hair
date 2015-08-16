#!/usr/bin/env python

from hair import * 
import sys
from PIL import Image

ih = hair()
ih.FPS = 10 

ih.loadgif(Image.open("gifs/fire.gif"), 0, 0, 95, 16, 5, 200 )

frameahead = 0
for i in xrange(70):
    frameahead = ih.loadgif(Image.open("gifs/zelda-fire.gif"),i,0,18,16, 5, 2, frameahead)
    print frameahead

while True:
    ih.update()
