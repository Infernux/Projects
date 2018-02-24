# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class BattleSessionListMeta(DAAPIModule):

    def requestToJoinTeam(self, prbID, prbType):
        self._printOverrideError('requestToJoinTeam')



    def getClientID(self):
        self._printOverrideError('getClientID')



    def as_refreshListS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_refreshList(data)




+++ okay decompyling battlesessionlistmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:24 CET
