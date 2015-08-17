#!/usr/bin/env python

from PIL import Image
import sys

try:
    gif = Image.open(sys.argv[1])
except:
    print sys.argv[0] + " file.gif"
    quit()

w,h = gif.size
crop_w = int(h * (95.0/16.0))
w = int(16.0/h*w)
tiles = 95/w + 1
w,h = gif.size
i = 0

while gif:
    try:
        frame = Image.new(gif.mode,(w*tiles,h),gif.info["transparency"])
        if gif.mode == "P":
            frame.putpalette(gif.getpalette())
        for j in xrange(tiles):
            frame.paste(gif,(w*j,0))
        frame.save("frame."+str(i).zfill(3)+".gif",transparency=gif.info["transparency"])
        i += 1
        gif.seek( gif.tell()+1 )
    except EOFError:
        break

print "NOW DO THIS:"
print "-------------------------"
print "convert -delay 10 -loop 0 frame.*.gif tmp.gif && rm -f frame.*.gif"
print "gifsicle --crop 0,0-"+str(crop_w)+","+str(h)+" tmp.gif > new.gif && rm -f tmp.gif"
