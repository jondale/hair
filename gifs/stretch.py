#!/usr/bin/python

from PIL import Image
import sys

w,h = Image.open(sys.argv[1]).size

w2 = int(h/16.0 * 95.0)
print "gifsicle --resize " + str(w2) + "x" + str(h) + " " + sys.argv[1] 

