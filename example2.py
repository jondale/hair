#!/usr/bin/env python

from hair import * 
import sys
from PIL import Image

ih = hair()
ih.FPS = 5 

frameahead = ih.loadgif(Image.open("gifs/fire.gif"), 0, 0, 95, 16, 5, 11 )
frameahead = ih.loadgif(Image.open("gifs/fire3.gif"), 0, 0, 95, 16, 5, 20, frameahead)

frameahead = 0
for j in xrange(5):
    for i in xrange(40):
        frameahead = ih.loadgif(Image.open("gifs/invader.gif"),i*2,0,16,16, 5, 1, frameahead, 100) + 1
        #def loadgif(self,gif,x,y,w,h,fps,loop=1,framejump=0,threshold=None):
        ih.loadgif(Image.open("gifs/goomba.gif"),i*2,0,16,16, 5, 1, frameahead+40, 100) 
while True:
    ih.update()
