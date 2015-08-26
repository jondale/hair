#!/usr/bin/python

# Add parent directory to path so we can import the library
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from hair import *


ih = Hair()
ih.FPS = 20

bg = ih.load_gif("images/warp.gif",height=16)
bg.FPS=20
bg.end_time = 18
ih.add(bg)

txt1 = ih.load_text("KNOXMAKERS", height=10, color=(255,255,0), ttf="fonts/Minecraft.ttf")
txt2 = ih.load_text("KNOXMAKERS", height=10, color=(255,0,0), ttf="fonts/Minecraft.ttf")
txt3 = ih.load_text("KNOXMAKERS", height=10, color=(0,255,0), ttf="fonts/Minecraft.ttf")
txt4 = ih.load_text("KNOXMAKERS", height=10, color=(0,0,255), ttf="fonts/Minecraft.ttf")
txt5 = ih.load_text("KNOXMAKERS", height=10, color=(255,255,255), ttf="fonts/Minecraft.ttf")
txt = txt1 + txt2 + txt3 + txt4 + txt5
txt.FPS = 10
txt.end_time = 18
ih.add(txt,align="CENTER")

txt5.start_time = 18
ih.add(txt5, align="CENTER")

banana = ih.load_gif("images/banana.gif",height=16)
banana.start_time = 1
banana.end_time = 17
banana.x = 40
banana.FPS = 8
ih.add(banana)

goomba = ih.load_gif("images/goomba.gif",height=16)
goomba.x = -20
goomba.y = 0
goomba.FPS = 2
goomba.move( x=110, y=0, step=0.5 )
ih.add(goomba)

goomba2 = ih.load_gif("images/goomba.gif",height=12)
goomba2.start_time = 5
goomba2.x = -15
goomba2.y = 4
goomba2.FPS = 4
goomba2.path( x=10, y=4, step=2 )
goomba2.path( x=20, y=4, step=0.5)
goomba2.path( x=20, y=0, step=2, delay=1)
goomba2.path( x=20, y=4, step=2 )
goomba2.path( x=20, y=0, step=2 )
goomba2.path( x=20, y=4, step=2 )
goomba2.path( x=20, y=0, step=2 )
goomba2.path( x=20, y=4, step=2 )
goomba2.path( x=30, y=4, step=2, delay=1 )
goomba2.path( x=40, y=4, step=0.5 )
goomba2.path( x=50, y=4, step=2 )
goomba2.path( x=60, y=4, step=0.5 )
goomba2.path( x=70, y=4, step=2 )
goomba2.path( x=80, y=4, step=0.5 )
goomba2.path( x=-15, y=4, step=3 )
ih.add(goomba2)

while True:
    ih.update()

