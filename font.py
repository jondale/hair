#!/usr/bin/python

from hair import hair
from PIL import Image, ImageDraw, ImageFont
import sys

try:
    ttf = sys.argv[1]
    x = int(sys.argv[2])
    y = int(sys.argv[3])
    height = int(sys.argv[4])
    r = int(sys.argv[5])
    g = int(sys.argv[6])
    b = int(sys.argv[7])
    color = (r,g,b)
except:
    print sys.argv[0] + " font.tff x y height r g b"
    print
    print "Example: ./font.py ttf/V5PRC___.TTF 2 3 9 0 255 255"
    quit()

ih = hair()
ih.ttf("KNOXMAKERS",x,y,height,color,ttf) #,1,20,(255,255,255),"ttf/MonteCarloFixed12.ttf")
ih.update()
