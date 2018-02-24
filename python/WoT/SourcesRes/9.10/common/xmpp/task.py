# 2015.01.14 22:42:38 CET
import Event
from debug_utils import *
import Connection

class Task:
    ids = 0
    count = 0
    STANZA_ID_FORMAT = Connection.Connection.RESOURCE + u'_%d_%d'

    @staticmethod
    def nextId():
        Task.ids += 1
        return Task.ids



    def __init__(self, params):
        Task.count += 1
        self.id = Task.nextId()
        self.subId = 0
        self.params = params
        self.connection = None
        self.validation = set()
        self.lastError = ''
        self.eventSucceeded = Event.Event()
        self.eventFailed = Event.Event()
        self.eventError = Event.Event()



    def __del__(self):
        Task.count -= 1



    def __str__(self):
        return u'Task %d: state=%d, params:%s, lastError:%s, ' % (self.id,
         self.subId,
         self.params,
         self.lastError)



    def nextSubId(self):
        self.subId += 1
        return self.subId



    def stanzaId(self):
        return Task.STANZA_ID_FORMAT % (self.id, self.subId)



    def onConnected(self):
        pass



    def onDisconnected(self):
        pass



    def valid(self):
        return set(self.validation).issubset(set(self.params.keys()))



    def connect(self, connection):
        self.connection = connection
        self.onConnected()



    def disconnect(self):
        self.connection = None
        self.onDisconnected()



    def digest(self, stanza, subId):
        pass




+++ okay decompyling task.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:42:38 CET
