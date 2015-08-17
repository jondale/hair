#!/usr/bin/env python

from PIL import Image
import sys

try:
    gif = Image.open(sys.argv[1])
except:
    print sys.argv[0] + " file.gif"
    quit()

w,h = gif.size
w = int(16.0/h*w)
h = 16
tiles = 95/w + 1
w,h = gif.size
i = 0

while gif:
    try:
        frame = Image.new("RGB",(w*tiles,h),(0,0,0))
        for j in xrange(tiles):
            frame.paste(gif,(w*j,0))
        frame.save("frame."+str(i).zfill(3)+".gif")
        i += 1
        gif.seek( gif.tell()+1 )
    except EOFError:
        break

