# 2015.01.14 22:24:24 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class AwardWindowMeta(DAAPIModule):

    def onOKClick(self):
        self._printOverrideError('onOKClick')



    def as_setDataS(self, data):
        if self._isDAAPIInited():
            return self.flashObject.as_setData(data)




+++ okay decompyling awardwindowmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:24 CET
