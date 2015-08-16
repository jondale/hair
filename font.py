#!/usr/bin/python

from hair import hair
from PIL import Image, ImageDraw, ImageFont

ih = hair()
ih.text("KNOXMAKERS",10,1,20,(255,255,255),"ttf/MonteCarloFixed12.ttf")
ih.update()
