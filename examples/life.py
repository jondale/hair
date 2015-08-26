#!/usr/bin/python

# Add parent directory to path so we can import the library
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from hair import *
import random

MIN_START = 300
MAX_START = 500
ALIVE_COLOR = (0,255,0,255)
DEAD_COLOR = (0,0,0,0)

def randomize_board(gen1,total):
    xy = []
    while len(xy) < total:
        x = random.randint(0,ih.width-1)
        y = random.randint(0,ih.height-1)
        if (x,y) not in xy:
            xy.append((x,y))
            gen1[x,y] = ALIVE_COLOR


def get_neighbors(x,y,width,height):
    xs = [x-1,x-1,x-1,  x,  x,x+1,x+1,x+1]
    ys = [y-1,  y,y+1,y-1,y+1,y-1,  y,y+1]
    xs = [width-1 if i==-1 else i for i in xs]
    xs = [0 if i==width else i for i in xs]
    ys = [height-1 if i==-1 else i for i in ys]
    ys = [0 if i==height else i for i in ys]
    return zip(xs,ys)


ih = Hair()
ih.FPS = 40

#bg = ih.load_gif("images/mermaid.gif",height=16)
#bg.FPS=10
#ih.add(bg)

gen1 = HairyPixels(width=ih.width, height=ih.height)
gen2 = HairyPixels(width=ih.width, height=ih.height)
randomize_board(gen1,random.randint(MIN_START,MAX_START))
ih.add(gen1)

ih.update()


while True:

    gen2.copy(gen1)
    
    for y in xrange(ih.height):
        for x in xrange(ih.width):
            neighbor_count = 0
            for nx,ny in get_neighbors(x, y, ih.width, ih.height):
                if gen1[nx,ny] == ALIVE_COLOR:
                    neighbor_count += 1
            if gen1[x,y] == ALIVE_COLOR and neighbor_count not in (2,3):
                gen2[x,y] = DEAD_COLOR
            elif gen1[x,y] != ALIVE_COLOR and neighbor_count == 3:
                gen2[x,y] = ALIVE_COLOR
                
    gen1.copy(gen2)
    ih.update()

