# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class SkillDropMeta(DAAPIModule):

    def calcDropSkillsParams(self, tmanCompDescr, xpReuseFraction):
        self._printOverrideError('calcDropSkillsParams')



    def dropSkills(self, dropSkillCostIdx):
        self._printOverrideError('dropSkills')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_setGoldS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setGold(value)



    def as_setCreditsS(self, value):
        if self._isDAAPIInited():
            return self.flashObject.as_setCredits(value)




+++ okay decompyling skilldropmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
