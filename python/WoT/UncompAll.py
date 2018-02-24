#!/usr/bin/python

from os import system
from os import listdir
from os.path import isfile, join

for f in listdir('.'):
    if(isfile(f) and '.pyc' in f):
        system("uncompyler.py "+f+">"+f[:-1])
