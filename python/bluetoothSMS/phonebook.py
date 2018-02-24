#!/usr/bin/python

import bluetooth
from bluetooth import *
from PyOBEX import client, headers, responses, common, requests

class PhoneBook():
    def __init__(self,host):
        #super(PhoneBook,self).__init__()

        d=bluetooth.find_service(address=host, uuid='1130')
        port = d[0]['port']
        #print port

        uuidPB='\x79\x61\x35\xf0\xf0\xc5\x11\xd8\x09\x66\x08\x00\x20\x0c\x9a\x66'

        c=client.Client(host,port)
        response = c.connect(header_list=[headers.Target(uuidPB)])

        self.client=c
        #connid=int(response.header_data[0].data) #ID
        #print connid
        #connId,l=c.get('telecom/pb', header_list=[headers.Type('x-bt/vcard-listing')])
        connId,l=c.get('telecom/pb', header_list=[headers.Type('x-bt/vcard-listing')])
        c.setpath('telecom/pb',header_list=[headers.Connection_ID(1)])
        self.pb=self.parseList(l)
        #print c.setpath('SIM',header_list=[headers.Connection_ID(1),headers.Type('x-bt/vcard-listing')])

    def getPhoneBook(self):
        return self.pb

    def parseList(self,l):
        offset=0
        allCards=[]
        while(offset<(len(l)-len('</vCard-listing>'))):
            newoffset,card=self.parseCards(l[offset:])
            offset+=newoffset
            allCards.append(self.parseCard(card))

        detailCards=[]
        for card in allCards:
            detailCards.append(self.getDetailVCard(card[0]))

        return detailCards

    def getDetailVCard(self,handle):
        try:
            vcard=self.client.get(handle, header_list=[headers.Type('x-bt/vcard')])[1]
        except:
            return #not_found

        #print vcard
        version=vcard.find('VERSION')
        #name
        infos=dict()
        infos['TEL']=[]

        interestingFields=['N','FN','TEL']

        for line in vcard.split('\r\n'):
            datas=line.split(':')
            fieldType=datas[0].split(';')[0]
            try:
                try:
                    fieldDetail=datas[0].split(';')[1]
                except:
                    fieldDetail=''

                info=datas[1]

                if fieldType in interestingFields:
                    if fieldType=='TEL':
                        number=info
                        infos[fieldType].append([fieldDetail,number])
                    else:
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
                #print e
                pass #nothing in the field

        return infos

    def decodeEqualsFormated(self,tab):
        allNames=[]
        for el in tab:
            new=''

            if(el[0]=='='):
                for char in el.split('='):
                    if(len(char)):
                        new+=char.decode('hex')
            else:
                new=el
            allNames.append(new)
        return allNames

    def parseCard(self,card):
        start=card.find('handle')+len('handle=\"')
        end=card.find('\"',start)
        handle=card[start:end]
        
        start=card.find('name',start)+len('name=\"')
        end=card.find('\"',start)
        name=card[start:end]

        return handle,name

    def parseCards(self,l):
        start=l.find('<card')
        end=l.find('/>',start)
        card=l[start:end+2]
        return end+2, card
