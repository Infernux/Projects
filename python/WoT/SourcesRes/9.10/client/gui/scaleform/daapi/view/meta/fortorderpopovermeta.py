# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortOrderPopoverMeta(DAAPIModule):

    def requestForCreateOrder(self):
        self._printOverrideError('requestForCreateOrder')



    def requestForUseOrder(self):
        self._printOverrideError('requestForUseOrder')



    def getLeftTime(self):
        self._printOverrideError('getLeftTime')



    def getLeftTimeStr(self):
        self._printOverrideError('getLeftTimeStr')



    def getLeftTimeTooltip(self):
        self._printOverrideError('getLeftTimeTooltip')



    def openQuest(self, questID):
        self._printOverrideError('openQuest')



    def as_setInitDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setInitData(data)



    def as_disableOrderS(self, daisable):
        if self._isDAAPIInited():
            return self.flashObject.as_disableOrder(daisable)




+++ okay decompyling fortorderpopovermeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
