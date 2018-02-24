# 2015.01.14 22:24:32 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class SquadTypeSelectPopoverMeta(DAAPIModule):

    def selectFight(self, actionName):
        self._printOverrideError('selectFight')



    def getTooltipData(self, itemData):
        self._printOverrideError('getTooltipData')



    def as_updateS(self, items):
        if self._isDAAPIInited():
            return self.flashObject.as_update(items)




+++ okay decompyling squadtypeselectpopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:32 CET
