# 2015.01.14 22:24:26 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortBattleResultsWindowMeta(DAAPIModule):

    def getMoreInfo(self, battleID):
        self._printOverrideError('getMoreInfo')



    def getClanEmblem(self):
        self._printOverrideError('getClanEmblem')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_notAvailableInfoS(self, battleID):
        if self._isDAAPIInited():
            return self.flashObject.as_notAvailableInfo(battleID)



    def as_setClanEmblemS(self, iconTag):
        if self._isDAAPIInited():
            return self.flashObject.as_setClanEmblem(iconTag)




+++ okay decompyling fortbattleresultswindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:26 CET
