# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class BattleTypeSelectPopoverMeta(DAAPIModule):

    def selectFight(self, actionName):
        self._printOverrideError('selectFight')



    def demoClick(self):
        self._printOverrideError('demoClick')



    def getTooltipData(self, itemData):
        self._printOverrideError('getTooltipData')



    def as_updateS(self, items, isShowDemonstrator, demonstratorEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_update(items, isShowDemonstrator, demonstratorEnabled)



    def as_setDemonstrationEnabledS(self, demonstratorEnabled):
        if self._isDAAPIInited():
            return self.flashObject.as_setDemonstrationEnabled(demonstratorEnabled)




+++ okay decompyling battletypeselectpopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:24 CET
