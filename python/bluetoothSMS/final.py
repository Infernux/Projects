#!/usr/bin/python

import sys
import signal
import time

import dbus, dbus.service, dbus.mainloop.glib
try:
    from gi.repository import GObject as gobject
except:
    import gobject

import struct
import bluetooth
from inspect    import getargspec
import threading
from PyOBEX     import client, headers, responses, common, requests

from phonebook  import PhoneBook
from server     import Server

class MAPThread(threading.Thread):
    def handler(self,typeMsg,handle,folder):
        #peut etre gerer les messages sent et delivered
        folder=folder.upper()
        if(typeMsg=='NewMessage' and folder.find('INBOX')!=-1):
            #faire gaffe aux messages dans l outbox/sent
            try:
                connId,msg=self.c.get(handle,header_list=[headers.Connection_ID(1),headers.Type('x-bt/message'),headers.App_Parameters('\x14\x01\x01\x0A\x01\x00')]) #get message
                self.decodeSMS(msg)
            except :
                print "EXCEPT"
        else:
            print typeMsg

    def setHost(self,host):
        self.host=host

    def __init__(self):
        super(MAPThread, self).__init__()
        self.NSN=self.NewSMSNotification('/SMSBluetooth')
        pass

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        d=bluetooth.find_service(address=self.host, uuid='1134')
        port = d[0]['port']

        print 'registration'
        uuidmas='\xbb\x58\x2b\x40\x42\x0c\x11\xdb\xb0\xde\x08\x00\x20\x0c\x9a\x66'

        self.c=client.Client(self.host,port)

        response = self.c.connect(header_list=[headers.Target(uuidmas)])

        try:
            #TODO:encodage des caracteres accentues
            self.c.setpath('telecom',header_list=[headers.Connection_ID(1)])
            self.c.setpath('msg',header_list=[headers.Connection_ID(1)])
            #self.c.setpath('inbox',header_list=[headers.Connection_ID(1)])
            #res=self.c.get(header_list=[headers.Connection_ID(1),headers.Type('x-obex/folder-listing')]) #get folder list
            #print res

            res=self.c.put('\x30','\x30',header_list=[headers.Connection_ID(1),headers.Type('x-bt/MAP-NotificationRegistration'),headers.App_Parameters('\x0E\x01\x01'),headers.Body('\x30')]) #activate notifications
            
            #print self.c.get('inbox',header_list=[headers.Connection_ID(1),headers.Type('x-bt/MAP-msg-listing')]) #get listing

            bus = dbus.SessionBus()
            bus.add_signal_receiver(self.handler, dbus_interface="com.mrnux.bluetoothSMS",
                signal_name="newEvent")
        except Exception,e:
            print e
            pass
        loop = gobject.MainLoop()
        loop.run()

    def sendSMS(self,number,message):
        status='READ'
        folder='telecom/msg/outbox'
        vcard='BEGIN:VCARD\r\nVERSION:3.0\r\nTEL:'+number+'\r\nEND:VCARD\r\n'

        message=message.encode('utf-8')
        
        body='BEGIN:BMSG\r\nVERSION:1.0\r\nSTATUS:'+status+'\r\nTYPE:SMS_GSM\r\nFOLDER:'+folder+'\r\nBEGIN:BENV\r\n'+vcard+'BEGIN:BBODY\r\nCHARSET:UTF-8\r\nLENGTH:'+str(len('BEGIN:MSG\r\n'+message+'\r\nEND:MSG\r\n'))+'\r\nBEGIN:MSG\r\n'+message+'\r\nEND:MSG\r\nEND:BBODY\r\nEND:BENV\r\nEND:BMSG\r\n'
        #print self.c.setpath('telecom/msg',header_list=[headers.Connection_ID(1)])
        print self.c.put('outbox',body,header_list=[headers.Connection_ID(1),headers.Type('x-bt/message'),headers.App_Parameters('\x14\x01\x01'),headers.End_Of_Body('')]) #send message

    class NewSMSNotification(dbus.service.Object):
        def __init__(self, path):
            dbus.service.Object.__init__(self, dbus.SessionBus(), path)

        @dbus.service.signal(dbus_interface='com.mrnux.bluetoothSMS',
                             signature='s')
        def newSMS(self, content):
            #print "new SMS %s " % (content)
            pass

    def getLength(self,msg):
        length=0
        for c in msg:
            if c=='\xc3' or c=='\xc2':
                pass
            elif c=='\xe3': #smiley == 4\xoo
                length=length-2
            elif c=='\xe2': #smiley == 4\xoo
                length=length-1
            elif c=='\xf0': #smiley le retour
                length=length-2
            else:
                length=length+1
        return length 

    def sendToDBus(self,infos):
        #could be better, but dbus prevents me from using pack
        packed=str(self.getLength(infos['MSG']))+'\r\n'+infos['MSG']
        packed+=str(self.getLength(infos['FN'][0]))+'\r\n'+infos['FN'][0]
        packed+=str(self.getLength(infos['N'][0]))+'\r\n'+infos['N'][0]
        packed+=str(len(infos['TEL'][0][1]))+'\r\n'+infos['TEL'][0][1]
        self.NSN.newSMS(packed)

    #get MSG content by searching for BEGIN:MSG from start
    #and END:MSG from end
    #then parse the rest
    def extractMSG(self,m):
        start   = m.find('BEGIN:MSG',0) 
        end     = m.rfind('END:MSG')-2 #remove \r\n
        msg     = m[start+len('BEGIN:MSG\r\n'):end]
        newM    = m[:start]+m[end+len('\r\nEND:MSG'):]
        return newM,msg

    def decodeSMS(self,m):
        infos=dict()
        m,infos['MSG']=self.extractMSG(m)

        infos['TEL']=[]
        interestingFields = ['FN','N','TEL','BEGIN','END']

        MSG=False
        msg=''

        for line in m.split('\r\n'):
            datas=line.split(':')
            if MSG and (len(datas)==1 or datas[0]!='END'):
                msg+=line
                continue

            fieldType=datas[0].split(';')[0]

            try:
                try:
                    fieldDetail=datas[0].split(';')[1]
                except:
                    fieldDetail='Originator'
                info=datas[1]
                if fieldType in interestingFields:
                    if fieldType=='TEL':
                        number=info
                        infos[fieldType].append([fieldDetail,number])
                    elif info=='MSG': #message
                        if fieldType=='BEGIN':
                            MSG=True
                        elif fieldType=='END':
                            MSG=False
                            infos['MSG']=msg    
                    elif fieldType=='FN' or fieldType=='N':
                        if(fieldDetail.find('UTF-8')==-1):
                            names=[]
                            for n in info.split(';'):
                                names.append(n)
                        else:
                            names=[]
                            for n in info.split(';'):
                                names.append(n)
                            names=self.decodeEqualsFormated(names)
                        infos[fieldType]=names
            except Exception, e:
                pass #nothing in the field
        self.sendToDBus(infos);
        print infos

class MAP():
    def signal_handler(self,signal, frame):
        print('You pressed Ctrl+C!')
        self.serverThread._Thread__stop()
        self.MAPThread._Thread__stop()
        sys.exit(0)

    def unpackMsg(self,msg):
        #print msg
        infos=[]
        for i in range(0,4):
            end     = msg.find('\r\n')
            length  = int(msg[0:end])
            infos.append(msg[end+2:end+length+2])
            msg     = msg[end+length+2:]
        return infos

    def initPhonebook(self):
        pb=PhoneBook(self.host)
        return pb.getPhoneBook()


    def getPhoneBook(self):
        return self.pb

    def sendSMS(self,number,message):
        self.MAPThread.sendSMS(number,message)

    def __init__(self,host):
        self.host=host
        signal.signal(signal.SIGINT, self.signal_handler)

        self.serverThread=Server()
        self.serverThread.run()

        self.MAPThread=MAPThread()
        self.MAPThread.setHost(host)
        self.MAPThread.start()
