# 2015.01.14 22:38:35 CET
from collections import namedtuple

class _ServerInfo(object):
    __slots__ = ('centerID', 'dbidMin', 'dbidMax', 'regionCode')

    def __init__(self, centerID, dbidMin, dbidMax, regionCode):
        self.centerID = centerID
        self.dbidMin = dbidMin
        self.dbidMax = dbidMax
        self.regionCode = regionCode



    def isPlayerHome(self, playerDBID):
        return self.dbidMin <= playerDBID <= self.dbidMax



_RoamingSettings = namedtuple('_RoamingSettings', 'homeCenterID curCenterID servers')

class ServerSettings(object):

    def __init__(self, serverSettings):
        roamingSettings = serverSettings['roaming']
        self.__roamingSettings = _RoamingSettings(roamingSettings[0], roamingSettings[1], [ _ServerInfo(*s) for s in roamingSettings[2] ])



    def getHomeCenterID(self):
        return self.__roamingSettings.homeCenterID



    def getCurrentCenterID(self):
        return self.__roamingSettings.curCenterID



    def getRoamingServers(self):
        return self.__roamingSettings.servers



    def getPlayerHome(self, playerDBID):
        for s in self.getRoamingServers():
            if s.isPlayerHome(playerDBID):
                return s.centerID





+++ okay decompyling serversettings.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:38:35 CET
