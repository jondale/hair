#!/usr/bin/env python

from hair import * 
import sys
from PIL import Image

ih = hair()
ih.FPS = 15

# This is a silly way to do this.
# I could pre-prepare the gifs together into one gif
# Or I could I could make a function that returns sub-screen 
# pixels that can then be buffered so I only have to load the image once.

print "Buffering background..... "
frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 0, 0, 12, 16, 15, 10 )
frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 12, 0, 12, 16, 15, 10 )
frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 24, 0, 12, 16, 15, 10 )
frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 36, 0, 12, 16, 15, 10 )
frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 48, 0, 12, 16, 15, 10 )
frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 60, 0, 12, 16, 15, 10 )
frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 72, 0, 12, 16, 15, 10 )
frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 83, 0, 12, 16, 15, 10 )
print "Done"

while len(ih._BUFFER)>0:
    ih.ttf("KNOXMAKERS",2,3,10,(255,255,255),"ttf/Minecraft.ttf")
    ih.update()
