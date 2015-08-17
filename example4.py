#!/usr/bin/env python

from hair import * 
import sys
from PIL import Image
import random

ih = hair()
ih.FPS = 20 

colors = [ (255,255,255), (0,0,255), (255,255,0), (255,0,0), (0,0,255), (255,0,255) ]
frameahead = ih.loadgif(Image.open("gifs/warp2.gif"), 0, 0, 95, 16, 20, 100, 0 )

i = j = 0
while True: 
    i += 1
    j += 1
    
    if i > 40:
        i = 1
        j = 1
    elif i > 10:
        j = 10

    ih.ttf("KNOXMAKERS",47 - int(j*4.5),random.choice([2,3,4]),j,random.choice(colors),"ttf/Minecraft.ttf")
    ih.update()
