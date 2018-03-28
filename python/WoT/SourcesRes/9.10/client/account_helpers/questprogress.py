# 2015.01.14 13:53:28 CET
import AccountCommands
from functools import partial
from diff_utils import synchronizeDicts
from debug_utils import *

class QuestProgress(object):

    def __init__(self, syncData):
        self.__account = None
        self.__syncData = syncData
        self.__cache = {}
        self.__ignore = True



    def onAccountBecomePlayer(self):
        self.__ignore = False



    def onAccountBecomeNonPlayer(self):
        self.__ignore = True



    def setAccount(self, account):
        self.__account = account



    def synchronize(self, isFullSync, diff):
        if isFullSync:
            self.__cache.clear()
        for item in ('quests', 'tokens', 'potapovQuests'):
            itemDiff = diff.get(item, None)
            if itemDiff is not None:
                synchronizeDicts(itemDiff, self.__cache.setdefault(item, {}))




    def getCache(self, callback = None):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            return 
        self.__syncData.waitForSync(partial(self.__onGetCacheResponse, callback))



    def getItems(self, itemsType, callback):
        if self.__ignore:
            if callback is not None:
                callback(AccountCommands.RES_NON_PLAYER, None)
            return 
        self.__syncData.waitForSync(partial(self.__onGetItemsResponse, itemsType, callback))



    def __onGetCacheResponse(self, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if callback is not None:
            callback(resultID, self.__cache)



    def __onGetItemsResponse(self, itemsType, callback, resultID):
        if resultID < 0:
            if callback is not None:
                callback(resultID, None)
            return 
        if callback is not None:
            callback(resultID, self.__cache.get(itemsType, None))




+++ okay decompyling questprogress.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 13:53:28 CET
