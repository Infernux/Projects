#! /usr/bin/python2
import socket
import struct
import select
import sys

port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))

s.listen(1)
client, addr = s.accept()

print "Someone connected : "+str(addr)

BUFFER_SIZE = 1024

listen_list=[]
listen_list.append(client)

while True:
    ready_to_read, ready_to_write, error = \
            select.select(listen_list, [], [])

    for socket in ready_to_read:
        try:
            b=socket.recv(4)
            if(len(b)==0):
                print "Disconnected"
                listen_list.remove(socket)
                break
            length = int(struct.unpack('i', b)[0])
            b=socket.recv(length)
            print b
        except Exception, e:
            listen_list.remove(socket)
            print e
            pass
