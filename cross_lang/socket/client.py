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

message_to_send = ""

for _ in range(0,10):
    string = "test long"
    message_to_send += struct.pack('i', len(string))+string

s.send(message_to_send)
s.close()
