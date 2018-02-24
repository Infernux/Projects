# 2015.01.14 22:24:33 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class WaitingViewMeta(DAAPIModule):

    def showS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.show(data)



    def hideS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.hide(data)




+++ okay decompyling waitingviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:33 CET
