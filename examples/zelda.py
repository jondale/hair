#!/usr/bin/python

# Add parent directory to path so we can import the library
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


# sudo apt-get install vlc
#
# Using the python bindings to vlc
# https://wiki.videolan.org/Python_bindings
#
# Some less dependent answer for playing music would be great.
# pyglet failed me


import vlc
mp3file = os.path.dirname(os.path.realpath(__file__)) + "/sounds/zelda.mp3"
p = vlc.MediaPlayer("file://"+mp3file)
p.play()


#############################################################################
# START Really ugly code to make keypress reading non-echo and non-blocking
#############################################################################
import termios, fcntl, sys, os
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
###########################################################################
# END Really ugly code to make keypress reading non-echo and non-blocking
###########################################################################

import sys
from PIL import Image
from hair import *

ih = Hair()
ih.FPS=20

xstep = 5  # big steps for monster link
ystep = 5 

link_width = 16    # 3 fits in map
link_height = 16   

img = Image.open("images/zelda-worldmap.png")
w,h = img.size
zmap = ih.load_image(image=img)
zmap.x = -510
zmap.y = -268
ih.add(zmap)

sprite = Image.open("images/zelda-sprites.png")


link_right = ih.load_sprite(image=sprite,width=link_width,height=link_height,x1=90,y1=0,x2=106,y2=16)
link_right.add_sprite(image=sprite,width=link_width,height=link_height,x1=90,y1=30,x2=106,y2=46)
link_right.FPS=2
link_right.x = (95-link_width)/2
link_right.y = (16 - link_height)/2
link_right.active = False
ih.add(link_right)

link_up = ih.load_sprite(image=sprite,width=link_width,height=link_height,x1=60,y1=0,x2=76,y2=16)
link_up.add_sprite(image=sprite,width=link_width,height=link_height,x1=60,y1=30,x2=76,y2=46)
link_up.FPS=2
link_up.x = (95-link_width)/2
link_up.y = (16 - link_height)/2
link_up.active = False
ih.add(link_up)

link_left = ih.load_sprite(image=sprite,width=link_width,height=link_height,x1=30,y1=0,x2=46,y2=16)
link_left.add_sprite(image=sprite,width=link_width,height=link_height,x1=30,y1=30,x2=46,y2=46)
link_left.FPS=2
link_left.x = (95-link_width)/2
link_left.y = (16 - link_height)/2
link_left.active = False
ih.add(link_left)

link_down = ih.load_sprite(image=sprite,width=link_width,height=link_height,x1=0,y1=0,x2=16,y2=16)
link_down.add_sprite(image=sprite,width=link_width,height=link_height,x1=0,y1=30,x2=16,y2=46)
link_down.FPS=2
link_down.x = (95-link_width)/2
link_down.y = (16 - link_height)/2
link_down.active = True
ih.add(link_down)

try:
    while True:
        try:
            k = sys.stdin.read(3)
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            if k=='\x1b[A':
                link_up.active=True
                link_down.active=False
                link_right.active=False
                link_left.active=False
                zmap.y = min(zmap.y+ystep,0)
                print "up\ty = " + str(zmap.y)
            elif k=='\x1b[B':
                link_up.active=False
                link_down.active=True
                link_right.active=False
                link_left.active=False
                zmap.y = max(0-h+ih.height,zmap.y-ystep)
                print "down\ty = " + str(zmap.y)
            elif k=='\x1b[C':
                link_up.active=False
                link_down.active=False
                link_right.active=True
                link_left.active=False
                zmap.x = max(0-w+ih.width,zmap.x-xstep)
                print "right\tx = " + str(zmap.x)
            elif k=='\x1b[D':
                link_up.active=False
                link_down.active=False
                link_right.active=False
                link_left.active=True
                zmap.x = min(zmap.x+xstep,0)
                print "left\tx = " + str(zmap.x)
            #else:
                #print k
        except IOError: 
            pass
        
        ih.update()
        
except Exception,e:
    print str(e)
    os.system('stty sane')
