# 2015.01.14 22:24:29 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class MinimapLobbyMeta(DAAPIModule):

    def setMap(self, arenaID):
        self._printOverrideError('setMap')



    def as_changeMapS(self, texture):
        if self._isDAAPIInited():
            return self.flashObject.as_changeMap(texture)



    def as_addPointS(self, x, y, type, color, id):
        if self._isDAAPIInited():
            return self.flashObject.as_addPoint(x, y, type, color, id)



    def as_clearS(self):
        if self._isDAAPIInited():
            return self.flashObject.as_clear()




+++ okay decompyling minimaplobbymeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:29 CET
