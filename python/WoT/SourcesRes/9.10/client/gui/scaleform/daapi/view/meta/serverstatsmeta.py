# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class ServerStatsMeta(DAAPIModule):

    def getServers(self):
        self._printOverrideError('getServers')



    def relogin(self, id):
        self._printOverrideError('relogin')



    def isCSISUpdateOnRequest(self):
        self._printOverrideError('isCSISUpdateOnRequest')



    def startListenCsisUpdate(self, startListenCsis):
        self._printOverrideError('startListenCsisUpdate')



    def as_setPeripheryChangingS(self, isChanged):
        if self._isDAAPIInited():
            return self.flashObject.as_setPeripheryChanging(isChanged)



    def as_setServersListS(self, servers):
        if self._isDAAPIInited():
            return self.flashObject.as_setServersList(servers)



    def as_disableRoamingDDS(self, disable):
        if self._isDAAPIInited():
            return self.flashObject.as_disableRoamingDD(disable)



    def as_setServerStatsS(self, stats, tooltipType):
        if self._isDAAPIInited():
            return self.flashObject.as_setServerStats(stats, tooltipType)



    def as_setServerStatsInfoS(self, tooltipFullData):
        if self._isDAAPIInited():
            return self.flashObject.as_setServerStatsInfo(tooltipFullData)




+++ okay decompyling serverstatsmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
