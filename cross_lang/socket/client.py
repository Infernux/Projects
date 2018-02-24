#! /usr/bin/python2
import socket
import time
import struct

port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(("127.0.0.1", port))
except:
    print "fail"

for _ in range(0,1):
    print 's'

string = "test long"
string2 = "test short"

time.sleep(1)
a = struct.pack('i', len(string))+string
a += struct.pack('i', len(string2))+string2

s.send(a)
s.close()
