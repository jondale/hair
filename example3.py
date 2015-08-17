#!/usr/bin/env python

from hair import * 
import sys
from PIL import Image

ih = hair()
ih.FPS = 40 

print "Buffering background..... "

frameahead = ih.loadgif(Image.open("gifs/warp2.gif"), 0, 0, 95, 16, 20, 10, 0 )
frameahead = ih.loadgif(Image.open("gifs/h2o3.gif"), 0, 0, 95, 16, 20, 3, frameahead - 5 )
frameahead = ih.loadgif(Image.open("gifs/fire3.gif"), 0, 0, 95, 16, 20, 3, frameahead - 5)
frameahead = ih.loadgif(Image.open("gifs/m2.gif"), 0, 0, 95, 16, 20, 10, frameahead - 5 )

#frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 12, 0, 12, 16, 15, 10 )
#frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 24, 0, 12, 16, 15, 10 )
#frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 36, 0, 12, 16, 15, 10 )
#frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 48, 0, 12, 16, 15, 10 )
#frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 60, 0, 12, 16, 15, 10 )
#frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 72, 0, 12, 16, 15, 10 )
#frameahead = ih.loadgif(Image.open("gifs/matrix2.gif"), 83, 0, 12, 16, 15, 10 )
print "Done"

while ih.update():
    ih.ttf("KNOXMAKERS",2,3,10,(255,255,255),"ttf/Minecraft.ttf")
