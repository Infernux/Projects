# 2015.01.14 22:24:27 CET
from gui.Scaleform.framework.entities.DAAPIModule import DAAPIModule

class FortDisconnectViewMeta(DAAPIModule):

    def as_setWarningTextsS(self, warningTxt, warningDescTxt):
        if self._isDAAPIInited():
            return self.flashObject.as_setWarningTexts(warningTxt, warningDescTxt)




+++ okay decompyling fortdisconnectviewmeta.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:24:27 CET
