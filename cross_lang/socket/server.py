#! /usr/bin/python2
import socket
import struct
import select
import sys
import threading
import signal

port = 8080

clients = []
listen_list=[]

class ConnectionListener(threading.Thread):
    def __init__(self):
        super(ConnectionListener, self).__init__()
        self.running = False

    def run(self):
        self.running = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))
        self.s.settimeout(1)

        while(self.running):
            self.s.listen(0)
            try:
                client, addr = self.s.accept()

                clients.append(client)
                listen_list.append(client)

                print "Someone connected : "+str(addr)
            except:
                pass

    def stop(self):
        self.running = False
        self.s.close()

c = ConnectionListener()

def handler(signum, frame):
    print "signal received"
    c.stop()
    #join ?

signal.signal(signal.SIGINT, handler)
c.start()

BUFFER_SIZE = 1024

while True:
    try:
        ready_to_read, ready_to_write, error = \
                select.select(listen_list, [], [], 0)
    except:
        sys.exit(1)

    for socket in ready_to_read:
        try:
            b=socket.recv(4)
            if(len(b)==0):
                print "Disconnected"
                listen_list.remove(socket)
                clients.remove(socket)
                socket.close()
                break
            length = int(struct.unpack('i', b)[0])
            b=socket.recv(length)
            print b
        except Exception, e:
            listen_list.remove(socket)
            print e
            pass
