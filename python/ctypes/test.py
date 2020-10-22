#!/usr/bin/python3

from ctypes import *
#print(cdll.test) #windows

class POINT(Structure):
    _fields_ = [("x", c_uint),
                ("y", c_uint)]

#lib = cdll.LoadLibrary("libtest.so")
lib = CDLL("./libtest.so")

lib.printme()
print(lib.doublenum(3))

p = (POINT * 5)()
p[0].x = 3
p[0].y = 7
lib.sum_val.argtypes = [POINT*5]
print(lib.sum_val(p))
