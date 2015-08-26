#!/usr/bin/python

# This uses opencv for camera capture.
# sudo apt-get install python-opencv

# Add parent directory to path so we can import the library
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from hair import *

from PIL import Image
import cv2

def get_image(cam):
    r,img = cam.read()
    if not r:
        raise Exception("No webcam you dullard.")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)

ih = Hair()
cam=cv2.VideoCapture(0)


c = HairyPixels()
c.load_image(image=get_image(cam), width=95)
ih.add(c,"CENTER")

while True:
    c.load_image(image=get_image(cam), width=95)
    c.flip_horizontal()
    ih.update()
