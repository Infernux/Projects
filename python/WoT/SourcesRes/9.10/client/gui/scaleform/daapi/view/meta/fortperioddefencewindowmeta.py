# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortPeriodDefenceWindowMeta(DAAPIModule):

    def onApply(self, data):
        self._printOverrideError('onApply')



    def onCancel(self):
        self._printOverrideError('onCancel')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)



    def as_setTextsS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setTexts(data)




+++ okay decompyling fortperioddefencewindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
