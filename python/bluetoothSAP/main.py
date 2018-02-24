#!/usr/bin/python

from SAP import * 

from time import sleep

import bluetooth
import time
import sys

host=sys.argv[1]

d=bluetooth.find_service(address=host, uuid='112d')
port = d[0]['port']

print port

socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.connect((host,port))
#header=SAP.CONNECT_REQ+'\x01\x00\x00'
#payload='\x00\x00\x00\x02\x00\xff'
#socket.send(header+payload)

#c.changeLen(20)
sleep(2)
print 'Connecting ...'
res=[]

print 'Connect Req'
c=Connect_Req()
socket.send(c.get())
res.append(socket.recv(1024))
res.append(socket.recv(1024))

#print 'APDU'
#apdu=APDU_Req()
#socket.send(apdu.get())
#res.append(socket.recv(1024))

print 'ATR'
atr=ATR_Req()
socket.send(atr.get())
res.append(socket.recv(1024))
print res
sleep(20)
socket.close()
print 'closing connection'
