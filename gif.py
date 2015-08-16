#!/usr/bin/env python

from hair import * 
import random
import sys
from PIL import Image

h = hair()
h.FPS = 40 

giffile = sys.argv[1]

giffps = 10
if len(sys.argv) > 2:
    giffps = int(sys.argv[2])

gifloops = 10
if len(sys.argv) > 3:
    gifloops = int(sys.argv[3])


maxheight = h.ROWS
maxwidth = h.COLS

img = Image.open(sys.argv[1])
width,height = img.size
if height > maxheight:
    width = float(width)/height*maxheight
    height = maxheight
if width > maxwidth:
    height = float(height)/width*maxwidth
    width = maxwidth

# def loadgif(self,gif,x,y,w,h,fps,repeat=0,framejump=0):
tot = int(h.COLS/width)
padding = int((h.COLS - (tot * width)) / (tot+1))

for i in xrange(int(h.COLS/width)):
    frameahead = h.loadgif(Image.open(giffile), 1 + padding + int(i*(width+padding)), 0, width, height, giffps, gifloops, i*10)

last_percent = percent = 100
total_buffers = len(h._BUFFER)
while True:
    buffers_left = h.update()
    if buffers_left > 0:
        percent = int(float(buffers_left)/total_buffers*100.0)
        if percent != last_percent:
            print "[ "+str(buffers_left)+" / "+str(total_buffers)+" ] " + str(percent)+"%"
            last_percent = percent
    else:
        break
