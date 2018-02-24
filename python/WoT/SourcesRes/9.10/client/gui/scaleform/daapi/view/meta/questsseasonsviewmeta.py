# 2015.01.14 22:24:30 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class QuestsSeasonsViewMeta(DAAPIModule):

    def onShowAwardsClick(self, seasonID):
        self._printOverrideError('onShowAwardsClick')



    def onTileClick(self, tileID):
        self._printOverrideError('onTileClick')



    def onSlotClick(self, slotID):
        self._printOverrideError('onSlotClick')



    def as_setSeasonsDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setSeasonsData(data)



    def as_setSlotsDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setSlotsData(data)




+++ okay decompyling questsseasonsviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:30 CET
