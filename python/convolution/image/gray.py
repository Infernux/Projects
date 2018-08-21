#!/usr/bin/python3

import numpy as np
import time

import sys

from skimage import io, viewer, color

Kr = 0.299
Kg = 0.587
Kb = 0.114

def RGB_to_YCbCr(img):
    img2 = []
    for y in range(img.shape[1]):
        for x in range(img.shape[0]):
            r = float(img[x,y,0])
            g = float(img[x,y,1])
            b = float(img[x,y,2])

            if y == 0 and x < 10:
                print(r,g,b)
                print(Kr*r + Kg*g + Kb*b)

            img2.append(float(Kr*r + Kg*g + Kb*b))

    return img2

def YCbCr_to_RGB(rgb, img, w, h):
    for y in range(h):
        for x in range(w):
            gray = img[x + y*w]
            rgb[x,y,0] = gray
            rgb[x,y,1] = gray
            rgb[x,y,2] = gray

def grayme(img):
    img2 = RGB_to_YCbCr(img)
    YCbCr_to_RGB(img, img2, img.shape[0], img.shape[1])

def img():
    img = io.imread(sys.argv[1])  # load the image as grayscale
    print('image matrix size: ', img.shape)      # print the size of image
    grayme(img)
    io.imsave('output.bmp', img)

img()
