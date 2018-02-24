# 2015.01.14 13:53:27 CET
import BigWorld
import AccountCommands
import cPickle
import os
import base64
from SyncController import SyncController
from PlayerEvents import g_playerEvents as events
from debug_utils import *
from constants import DOSSIER_TYPE

class DossierCache(object):

    def __init__(self, accountName):
        self.__account = None
        self.__syncController = None
        p = os.path
        prefsFilePath = unicode(BigWorld.wg_getPreferencesFilePath(), 'utf-8', errors='ignore')
        self.__cacheDir = p.join(p.dirname(prefsFilePath), 'dossier_cache')
        self.__cacheFileName = p.join(self.__cacheDir, '%s.dat' % base64.b32encode('%s;%s' % (str(BigWorld.server()), accountName)))
        self.__cache = {}
        self.__maxChangeTime = 0
        self.__version = 0
        self.__ignore = True
        self.__isSynchronizing = False
        self.__syncID = 0
        self.__isFirstSync = True
        self.__readCache()



    def onAccountBecomePlayer(self):
        self.__ignore = False
        self.__isFirstSync = True
        self.synchronize()



    def onAccountBecomeNonPlayer(self):
        self.__ignore = True
        self.__isSynchronizing = False



    def setAccount(self, account):
        self.__account = account
        if self.__syncController is not None:
            self.__syncController.destroy()
            self.__syncController = None
        if account is not None:
            self.__syncController = SyncController(account, self.__sendSyncRequest, self.__onSyncResponse, self.__onSyncComplete)



    def synchronize(self):
        if self.__ignore:
            return 
        if self.__isSynchronizing:
            return 
        self.__isSynchronizing = True
        self.__syncController.request(self.__getNextSyncID(), None)



    def resynchronize(self):
        LOG_MX('resynchronize', self.__maxChangeTime)
        if self.__ignore:
            return 
        self.__isSynchronizing = True
        self.__syncController.request(self.__getNextSyncID(), None)



    def waitForSync(self, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            return 
        if not self.__isSynchronizing:
            callback(AccountCommands.RES_CACHE)
            return 
        proxy = lambda resultID, data: callback(resultID)
        self.__syncController.request(self.__syncID, proxy)



    def get(self, dossierType, ownerID, callback = None):
        getter = lambda cache: cache.get((dossierType, ownerID), (0, ''))[1]
        self.__get(getter, '', callback)



    def getCache(self, callback = None):
        getter = lambda cache: cache
        self.__get(getter, None, callback)



    def __get(self, getterFromCache, default, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, default)
            return 
        if not self.__isSynchronizing:
            self.__onGetResponse(AccountCommands.RES_CACHE, getterFromCache, default, callback)
            return 
        proxy = lambda resultID, data: self.__onGetResponse(resultID, getterFromCache, default, callback)
        self.__syncController.request(self.__syncID, proxy)



    def __onSyncResponse(self, syncID, resultID, ext = {}):
        if resultID == AccountCommands.RES_NON_PLAYER:
            return 
        if syncID != self.__syncID:
            return 
        if resultID < 0:
            LOG_ERROR('Dossier synchronization failed. Repeating')
            self.resynchronize()
            return 



    def __onSyncComplete(self, syncID, data):
        if data is None:
            return 
        (actualCacheVersion, dossiersList,) = data
        LOG_MX('__onSyncComplete', actualCacheVersion, len(dossiersList))
        if actualCacheVersion != self.__version:
            self.__cache.clear()
            self.__version = actualCacheVersion
        if syncID == self.__syncID:
            self.__isSynchronizing = False
        for (ownerID, changeTime, dossierCompDescr,) in dossiersList:
            self.__cache[DOSSIER_TYPE.VEHICLE, ownerID] = (changeTime, dossierCompDescr)
            self.__maxChangeTime = max(self.__maxChangeTime, changeTime)

        if self.__isFirstSync:
            self.__isFirstSync = False
        else:
            events.onDossiersResync()
        self.__writeCache()



    def __onGetResponse(self, resultID, getterFromCache, default, callback):
        if resultID < 0:
            if callback is not None:
                callback(resultID, default)
            return 
        if self.__isSynchronizing:
            self.__get(getterFromCache, default, callback)
            return 
        if callback is not None:
            callback(resultID, getterFromCache(self.__cache))



    def __getNextSyncID(self):
        self.__syncID += 1
        if self.__syncID > 30000:
            self.__syncID = 1
        return self.__syncID



    def __sendSyncRequest(self, syncID, proxy):
        if self.__ignore:
            return 
        self.__account._doCmdInt3(AccountCommands.CMD_SYNC_DOSSIERS, self.__version, self.__maxChangeTime, 0, proxy)



    def __readCache(self):
        self.__cache = {}
        self.__version = 0
        self.__maxChangeTime = 0
        fileHandler = None
        try:
            if not os.path.isfile(self.__cacheFileName):
                return 
            fileHandler = open(self.__cacheFileName, 'rb')
            (self.__version, self.__cache,) = cPickle.load(fileHandler)
            for (changeTime, dossierCompDescr,) in self.__cache.itervalues():
                self.__maxChangeTime = max(self.__maxChangeTime, changeTime)

        except:
            LOG_CURRENT_EXCEPTION()
        if fileHandler is not None:
            fileHandler.close()



    def __writeCache(self):
        fileHandler = None
        try:
            if not os.path.isdir(self.__cacheDir):
                os.makedirs(self.__cacheDir)
            fileHandler = open(self.__cacheFileName, 'wb')
            cPickle.dump((self.__version, self.__cache), fileHandler, -1)
        except:
            LOG_CURRENT_EXCEPTION()
        if fileHandler is not None:
            fileHandler.close()




+++ okay decompyling dossiercache.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:53:27 CET
