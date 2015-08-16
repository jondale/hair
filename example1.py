#!/usr/bin/env python

padding = 2
gifs = { 
    "gifs/alarm.gif": 10,
    "gifs/banana.gif": 8,
    "gifs/invader.gif": 1,
    "gifs/smw-questionblock.gif": 5,
    "gifs/zelda-fire.gif": 3,
}


from hair import * 
import random
import sys
from PIL import Image

ih = hair()
ih.FPS = 40 

x = padding
for gif in gifs.keys():
    giffps = gifs[gif]
    img = Image.open(gif)
    w,h = img.size
    if h > ih.ROWS:
        w = int(float(w)/h * ih.ROWS)
        h = ih.ROWS
    if w > ih.COLS:
        h = int(float(h)/w * ih.COLS)
        w = ih.COLS
    frameahead = ih.loadgif(Image.open(gif), x, 0, w, h, giffps, 1000) 
    x += w + padding

while True:
    #ih.text("KNOXMAKERS",7,2,12,(0,100,255),"ttf/MonteCarloFixed12.ttf")
    ih.update()
