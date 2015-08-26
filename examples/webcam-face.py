#!/usr/bin/python

# This uses opencv for camera capture.
# sudo apt-get install python-opencv

# Add parent directory to path so we can import the library
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from hair import *

from PIL import Image
import cv2

def get_image(cam,faceCascade):
    r,img = cam.read()
    if not r:
        raise Exception("No webcam you dullard.")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    print len(faces)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)

    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


ih = Hair()
cam=cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

c = HairyPixels()
c.load_image(image=get_image(cam,faceCascade), width=95)
ih.add(c,"CENTER")

while True:
    c.load_image(image=get_image(cam,faceCascade), width=95)
    ih.update()
