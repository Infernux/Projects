#!/usr/bin/python

import os
import subprocess
import sys
import argparse

class argReader():
    knownArgs=['-ip4', '-ip6']

    def __init__(self):
        print 'yop argreader is in da place'
        args=self.readArgs()
        self.setFlags(args)

    def readArgs(self):
        p = argparse.ArgumentParser()

        for kA in self.knownArgs:
            p.add_argument(kA, action='store_true')
        for i in range(0,len(sys.argv)): #p.add_argument('arg%d' % i)
            args = p.parse_args(sys.argv[1:])
        return args

    def setFlags(self,args):
        return None

ar=argReader()

ipinfos = subprocess.Popen("adb shell ip a s wlan0", shell=True, stdout=subprocess.PIPE).stdout.read()

for lineinfo in ipinfos.split('\n'):
    lineinfo=lineinfo.strip()
    b=lineinfo.split(' ')
    if b[0]=='inet':
        ip=b[1].split('/')[0]

print 'Trying to connect...'

print subprocess.Popen("adb tcpip 5555; adb connect "+ip, shell=True, stdout=subprocess.PIPE).stdout.read()
