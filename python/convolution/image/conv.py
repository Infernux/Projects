#!/usr/bin/python3

import numpy as np
import time

import sys

from skimage import io, viewer, color

def img():
    img = io.imread(sys.argv[1], as_gray=True)  # load the image as grayscale
    print('image matrix size: ', img.shape)      # print the size of image
    io.imsave('orig.bmp', img)
    img = naive_np(img)
    img = img.clip(0, 1)
    print(np.max(img))
    io.imsave('output.bmp', img)

def create_sharpening_filter():
    filtering = [[0,-1,0], [-1,5,-1], [0,-1,0]]
    return filtering

def add_padding(mat):
    el_size = len(mat[0])+2
    for x in mat:
        x.insert(0,0)
        x.append(0)

    mat.append([0]*el_size)
    mat.insert(0, [0]*el_size)
    return mat

def add_padding_np(mat):
    shape = mat.shape
    new_mat = np.zeros((shape[0] + 2, shape[1] + 2))
    new_mat[1:mat.shape[0]+1, 1:mat.shape[1]+1] = mat

    return new_mat

def base_conv(mat, x, y, filtering):
    val = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            filt = filtering[i+1][j+1]
            val += mat[x+i][y+j] * filt

    return val

def naive(ex):
    filtering = create_sharpening_filter()

    ex = [[105,102,100],[103,99,103],[101,98,104]]
    ex = add_padding(ex)

    start = time.time()

    for x in range(1, len(ex)+1 -2):
        for y in range(1, len(ex[x])+1 -2):
            res = base_conv(ex, x, y, filtering)

    end = time.time()
    return end - start

def np_conv(mat, x, y, filtering):
    a = mat[np.ix_([x-1, x, x+1],[y-1, y, y+1])]
    return np.sum(a*filtering)

def naive_np(ex):
    filtering = create_sharpening_filter()
    filtering = np.array(filtering)

    out = np.zeros_like(ex)

    ex = np.array(ex)
    ex = add_padding_np(ex)

    start = time.time()

    for x in range(1, len(ex)+1 -2):
        for y in range(1, len(ex[x])+1 -2):
            out[x-1, y-1] = np_conv(ex, x, y, filtering)

        if not x % 10:
            print(x)

    end = time.time()
    print(end - start)
    return out

ex = [[105,102,100],[103,99,103],[101,98,104]]

#print("naive py :", naive(ex))
#print("naive numpy:", naive_np(ex))

img()
