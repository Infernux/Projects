# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortIntelligenceWindowMeta(DAAPIModule):

    def getLevelColumnIcons(self):
        self._printOverrideError('getLevelColumnIcons')



    def requestClanFortInfo(self, index):
        self._printOverrideError('requestClanFortInfo')



    def as_setClanFortInfoS(self, clanFortVO):
        if self._isDAAPIInited():
            return self.flashObject.as_setClanFortInfo(clanFortVO)



    def as_setDataS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(value)



    def as_setStatusTextS(self, statusText):
        if self._isDAAPIInited():
            return self.flashObject.as_setStatusText(statusText)



    def as_getSearchDPS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getSearchDP()



    def as_getCurrentListIndexS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_getCurrentListIndex()



    def as_selectByIndexS(self, index):
        if self._isDAAPIInited():
            return self.flashObject.as_selectByIndex(index)




+++ okay decompyling fortintelligencewindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
