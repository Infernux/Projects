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

            img2.append(float(Kr*r + Kg*g + Kb*b))

    return img2

def grayme(img):
    r = float(img[0,0,0])
    g = float(img[0,0,1])
    b = float(img[0,0,2])
    img2 = RGB_to_YCbCr(img)

    for y in range(img.shape[1]):
        for x in range(img.shape[0]):
            y2 = img2[x + y*img.shape[0]]
            img[x,y,0] = y2
            img[x,y,1] = y2
            img[x,y,2] = y2


def img():
    img = io.imread(sys.argv[1])  # load the image as grayscale
    print('image matrix size: ', img.shape)      # print the size of image
    grayme(img)
    io.imsave('output.bmp', img)

img()
