# 2015.01.14 22:24:25 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class CrewMeta(DAAPIModule):

    def onShowRecruitWindowClick(self, rendererData, menuEnabled):
        self._printOverrideError('onShowRecruitWindowClick')



    def unloadAllTankman(self):
        self._printOverrideError('unloadAllTankman')



    def equipTankman(self, tankmanID, slot):
        self._printOverrideError('equipTankman')



    def updateTankmen(self):
        self._printOverrideError('updateTankmen')



    def openPersonalCase(self, value, tabNumber):
        self._printOverrideError('openPersonalCase')



    def as_tankmenResponseS(self, roles, tankmen):
        if self._isDAAPIInited():
            return self.flashObject.as_tankmenResponse(roles, tankmen)




+++ okay decompyling crewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:25 CET
