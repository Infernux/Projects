#!/usr/bin/python

SENT=1
RECEIVED=0

class Conversation():
    def __init__(self,name,num):
        self.msg=[]
        self.name=name
        self.num=num

    def addMsg(self,way,msg):
        self.msg.append([way,msg])

    def getMsg(self):
        return msg
