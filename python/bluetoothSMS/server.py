#!/usr/bin/python

import threading
import dbus.mainloop.glib
import dbus.service
try:
    from gi.repository import GObject as gobject
except:
    import gobject
import dbus
import subprocess
import struct
from bluetooth import BluetoothSocket, RFCOMM

PORT=23

class Event(dbus.service.Object):
    def __init__(self, path):
        dbus.service.Object.__init__(self, dbus.SessionBus(), path)

    @dbus.service.signal(dbus_interface='com.mrnux.bluetoothSMS',
                         signature='sss')
    def newEvent(self, typeMsg, handle, folder):
        if debug:
            print "Type : %s, handle : %s" % (typeMsg, handle)

def getBluezPid():
    proc=''
    try:
        proc=subprocess.Popen(['ps','-e'],stdout=subprocess.PIPE)
    except:
        proc=subprocess.Popen(['ps'],stdout=subprocess.PIPE)

    out, err = proc.communicate()
    pos=out.find('bluetoothd') #find bluez daemon
    startline=out.rfind('\n',0,pos)
    return out[startline+1:pos].strip().split(' ')[0]

xml = ' \
<?xml version="1.0" encoding="UTF-8" ?>         \
<record>                                        \
  <attribute id="0x0001">                       \
    <sequence>                                  \
      <uuid value="0x1133"/>                    \
    </sequence>                                 \
  </attribute>                                  \
                                                \
  <attribute id="0x0002">                       \
     <uint32 value="0"/>                        \
  </attribute>                                  \
                                                \
  <attribute id="0x0003">                       \
    <uuid value="00001133-0000-1000-8000-00805f9b34fb"/> \
  </attribute>                                  \
                                                \
  <attribute id="0x0004">                       \
    <sequence>                                  \
      <sequence>                                \
        <uuid value="0x0100"/>                  \
      </sequence>                               \
      <sequence>                                \
        <uuid value="0x0003"/>                  \
        <uint8 value="'+str(PORT)+'"/>                     \
      </sequence>                               \
      <sequence>                                \
        <uuid value="0x0008"/>                  \
      </sequence>                               \
    </sequence>                                 \
  </attribute>                                  \
                                                \
  <attribute id="0x0005">                       \
    <sequence>                                  \
      <uuid value="0x1002"/>                    \
    </sequence>                                 \
  </attribute>                                  \
                                                \
  <attribute id="0x0007">                       \
     <uint32 value="0"/>                        \
  </attribute>                                  \
                                                \
  <attribute id="0x0008">                       \
     <uint8 value="0xff"/>                      \
  </attribute>                                  \
                                                \
  <attribute id="0x0009">                       \
    <sequence>                                  \
      <sequence>                                \
        <uuid value="0x1134"/>                  \
        <uint16 value="0x0102"/>                \
      </sequence>                               \
    </sequence>                                 \
  </attribute>                                  \
                                                \
  <attribute id="0x0100">                       \
    <text value="MAP MNS-mint"/>                \
  </attribute>                                  \
                                                \
  <attribute id="0x0201">                       \
     <uint32 value="0"/>                        \
  </attribute>                                  \
</record>                                       \
'

debug=0

class Server():
    def myThread(self,run_event):
        server_sock=BluetoothSocket(RFCOMM)
        #TODO:allow to change the port
        server_sock.bind(("", PORT))
        server_sock.listen(1)
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from ", client_info)

        success=""
        #success=struct.pack('8B',0xa0,0x00,0x08,0xcb,0x00,0x00,0x00,0x01) #success
        success=struct.pack('3B',0xa0,0x00,0x03) #success

        data = client_sock.recv(1024)
        client_sock.send(success)

        while run_event.is_set():
            print('Waiting')
            data = client_sock.recv(1024)
            if len(data) == 0:
                break
            client_sock.send(success)
            self.decodeMessage(data)

        return

    def run(self):
        bus = dbus.SystemBus()

        path="/org/bluez/"+getBluezPid()+"/hci0"

        service = dbus.Interface(bus.get_object("org.bluez", path),
              "org.bluez.Service")

        handle = service.AddRecord(xml)

        print("Service record with handle 0x%04x added" % (handle))

        print("Press CTRL-C to remove service record")

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.e = Event('/NewEvent')

        try:
            run_event = threading.Event()
            run_event.set()

            myT = threading.Thread(target=self.myThread, args=(run_event,))
            myT.start()

            gobject.threads_init()

            #loop = gobject.MainLoop()
            #loop.run()
        except IOError:
            pass
        except KeyboardInterrupt:
            print("Stopping...")
            stop_advertising(server_sock)
            sys.exit()  

        #service.RemoveRecord(dbus.UInt32(handle))

    def decodeBody(self,m):
        xml=""
        for a in m:
            xml+=chr(a)
        start=xml.find('<event')
        end=xml.find('/>',start)
        event=str(xml[start:end+2])

        #get message type
        start=event.find('type')+len('type=\"')
        end=event.find('\"',start)
        typeMsg=event[start:end]

        #get handle
        start=event.find('handle',end)+len('handle=\"')
        end=event.find('\"',start)
        handle=event[start:end]

        #get folder
        start=event.find('folder',end)+len('folder=\"')
        end=event.find('\"',start)
        folder=event[start:end]

        self.e.newEvent(typeMsg, handle, folder)
        
        if debug:
            print('Type:'+typeMsg)
            print('Handle:'+handle)

    def decodeHeader(self,m):
        headerId=m[0]
        length=m[1]*16+m[2]
        data=m[3:length]
        if(debug):
            print('ID'+str(headerId))
            print('length'+str(length))
            print('data:'+str(data))
        if(headerId==0x48):
            self.decodeBody(data)
        return length

    def decodeOBEXOp(self,m):
        #each element is a byte
        opflag=m[0]
        length=m[1]*16+m[2]
        if(debug):
            print(opflag)
            print(length)
        return length, 3

    def decodeMessage(self,m):
        #find event
        m=struct.unpack(str(len(m))+'B',m)
        l,offset=self.decodeOBEXOp(m)
        while(offset<len(m)-1):
            decoded=self.decodeHeader(m[offset:])
            offset+=decoded
