#!/usr/bin/env python

import opc 
import random
import time
from PIL import Image,ImageDraw,ImageFont

class hair:
    _BUFFER = []
    _CURRENT = []
    FPS = 10 
    ROWS = 16
    COLS = 95
    #SERVER = "192.168.7.2:7890" 
    SERVER = "localhost:22000"
    n_pixels = ROWS*COLS

    def __init__(self):
        self.client = opc.Client(self.SERVER)
        self._CURRENT = [(0,0,0),] * self.n_pixels

    def pixelinit(self):
        return [None,] * self.n_pixels

    def ttf(self,txt,x,y,height,color=(255,255,255),ttf=None):
        img = Image.new("RGBA",(2000,500), (0,0,0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(ttf,100)

        size = draw.textsize(txt, font=font)
        w,h = size
        width = int(w * (float(height)/h))
        img = Image.new("RGBA",size,(0,0,0))
        draw = ImageDraw.Draw(img)
        draw.text((0,0), txt, color, font=font)

        pixels = self.pixelinit()
        pixels = self.img2pixel(pixels,img,x,y,width,height)
        self.put_pixels(pixels,(0,0,0))


    def img2pixel(self,pixels,img,x,y,w,h):
        rgbimg = Image.new("RGBA",img.size,(0,0,0))
        rgbimg.paste(img)
        rgbimg.thumbnail((w,h), Image.ANTIALIAS)
        w,h = rgbimg.size
        ipixels = rgbimg.load()  
        for i in xrange(h):
            for j in xrange(w):
                k = ((y+i)*self.COLS) + ((self.COLS-1) - (j + x))
                pixel = list(ipixels[j,i])
                try:
                    if pixel[3] > 0:
                        pixels[ k ] = (pixel[0],pixel[1],pixel[2])
                    else:
                        pixels[ k ] = (0,0,0) #None
                except:
                    pass
        return pixels

    def loadgif(self,gif,x,y,w,h,fps,loop=1,framejump=0):
        frames = []
        i = 0
        while gif:
            try:
                frames.append(self.img2pixel(self.pixelinit(),gif,x,y,w,h))
                gif.seek( gif.tell()+1 )
                i += 1
            except EOFError:
                break
        frameahead = 0
        for i in xrange(loop):
            numframe = 0
            for frame in frames:
                frameahead = int(self.FPS/fps) * ( (i*len(frames)) + numframe )
                if len(self._BUFFER) > frameahead+framejump:
                    frame = self.overlay_pixels(self._BUFFER[frameahead+framejump], frame, (0,0,0))
                self.buffer_pixels(frame,frameahead+framejump)
                numframe += 1
        return framejump + frameahead

    def pixelbox(self,pixels,x,y,w,h,rgb):
        for i in range(h):
            for j in range(w):
                pixel = ((y+i)*self.COLS) + x + j
                try:
                    pixels[pixel] = rgb
                except:
                    pass
        return pixels

    def overlay_pixels(self,pixels1,pixels2=None,BGCOLOR=None):
        if pixels2 == None:
            pixels = list(self._CURRENT)
            newpixels = list(pixels1)
        else:
            pixels = list(pixels1)
            newpixels = list(pixels2)

        for i in range(self.n_pixels):
            if newpixels[i] and newpixels[i] != BGCOLOR:
                pixels[i] = newpixels[i] 
        return pixels


    def put_pixels(self,pixels,BGCOLOR=None):
        try:
            self._BUFFER[0] = self.overlay_pixels(self._BUFFER[0],pixels,BGCOLOR)
        except:
            self._BUFFER.append(list(pixels))

    def buffer_pixels(self,pixels,frameahead=None):
        if frameahead:
            while len(self._BUFFER) <= frameahead:
                self._BUFFER.append(self.pixelinit())
            self._BUFFER[frameahead] = self.overlay_pixels(self._BUFFER[frameahead],pixels)
        else:
            self._BUFFER.append(list(pixels))

    def clear(self):
        self._BUFFER = []
        self._CURRENT = [(0,0,0),] * n_pixels
        self._BUFFER.append(self._CURRENT)

    def update(self):
        try:
            self._CURRENT = self.overlay_pixels(self._CURRENT,self._BUFFER.pop(0))
            self.client.put_pixels(list(reversed(self._CURRENT)), channel=0)
        except:
            pass

        time.sleep(1.0 / self.FPS)
        return len(self._BUFFER)
