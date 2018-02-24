# 2015.01.14 22:24:31 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class SmartPopOverViewMeta(DAAPIModule):

    def as_setPositionKeyPointS(self, valX, valY):
        if self._isDAAPIInited():
            return self.flashObject.as_setPositionKeyPoint(valX, valY)




+++ okay decompyling smartpopoverviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:31 CET
